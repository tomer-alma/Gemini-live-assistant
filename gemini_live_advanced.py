"""
Gemini Live API - Advanced Speech-to-Speech in Hebrew
Enhanced version with configuration support, error handling, and reconnection
"""

import asyncio
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import pyaudio
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Import configuration
try:
    from config import get_config
    CONFIG = get_config()
except ImportError:
    print("⚠️  config.py not found, using default settings")
    CONFIG = {
        "audio": {
            "sample_rate": 16000,
            "channels": 1,
            "format": "paInt16",
            "chunk_size": 2048,
            "input_device": None,
            "output_device": None,
        },
        "api": {
            "model": "gemini-2.0-flash-exp",
            "response_modalities": ["AUDIO"],
            "voice_name": "Puck",
        },
        "app": {
            "show_transcription": True,
            "debug": False,
            "auto_reconnect": True,
            "max_reconnect_attempts": 3,
            "reconnect_delay": 5,
        },
        "hebrew": {
            "rtl_text": True,
            "greeting": "שלום! אני כאן לדבר איתך בעברית.",
        }
    }


class AdvancedHebrewDoll:
    """
    Advanced real-time speech-to-speech conversational AI in Hebrew
    with configuration support and enhanced error handling
    """
    
    def __init__(self, api_key: str, system_instruction: Optional[str] = None):
        """Initialize the advanced Hebrew doll"""
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.audio = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.is_running = False
        self.connection_attempts = 0
        
        # Load configuration
        self.audio_config = CONFIG["audio"]
        self.api_config = CONFIG["api"]
        self.app_config = CONFIG["app"]
        self.hebrew_config = CONFIG["hebrew"]
        
        # Default system instruction
        self.system_instruction = system_instruction or """
        אתה בובה חכמה וידידותית שמדברת עברית.
        תפקידך להיות חבר טוב, לשוחח בצורה טבעית וחמה.
        דבר בעברית פשוטה וברורה, והיה תמיד חיובי ומעודד.
        
        You are a smart and friendly doll that speaks Hebrew.
        Your role is to be a good friend and chat naturally and warmly.
        Speak in simple and clear Hebrew, and always be positive and encouraging.
        """
        
        # Get PyAudio format
        format_map = {
            "paInt16": pyaudio.paInt16,
            "paInt32": pyaudio.paInt32,
            "paFloat32": pyaudio.paFloat32,
        }
        self.pa_format = format_map.get(self.audio_config["format"], pyaudio.paInt16)
        
        if self.app_config["debug"]:
            print("🔧 Debug mode enabled")
            print(f"Audio config: {self.audio_config}")
            print(f"API config: {self.api_config}")
    
    def setup_audio_streams(self):
        """Initialize audio input and output streams with configuration"""
        try:
            # Input stream (microphone)
            self.input_stream = self.audio.open(
                format=self.pa_format,
                channels=self.audio_config["channels"],
                rate=self.audio_config["sample_rate"],
                input=True,
                input_device_index=self.audio_config["input_device"],
                frames_per_buffer=self.audio_config["chunk_size"]
            )
            
            # Output stream (speaker) - Gemini returns audio at 24kHz
            # Use 24kHz for output even if input is 16kHz
            output_sample_rate = self.audio_config.get("output_sample_rate", 24000)
            if output_sample_rate == self.audio_config["sample_rate"]:
                output_sample_rate = 24000  # Force 24kHz for Gemini audio output
            
            self.output_stream = self.audio.open(
                format=self.pa_format,
                channels=self.audio_config["channels"],
                rate=output_sample_rate,
                output=True,
                output_device_index=self.audio_config["output_device"],
                frames_per_buffer=self.audio_config["chunk_size"]
            )
            
            print("✓ Audio streams initialized")
            if self.app_config["debug"]:
                print(f"  Input sample rate: {self.audio_config['sample_rate']} Hz")
                print(f"  Output sample rate: {output_sample_rate} Hz")
                print(f"  Channels: {self.audio_config['channels']}")
                print(f"  Chunk size: {self.audio_config['chunk_size']}")
            
        except Exception as e:
            print(f"✗ Error initializing audio: {e}")
            raise
    
    def close_audio_streams(self):
        """Close audio streams safely"""
        if self.input_stream:
            try:
                self.input_stream.stop_stream()
                self.input_stream.close()
            except:
                pass
        if self.output_stream:
            try:
                self.output_stream.stop_stream()
                self.output_stream.close()
            except:
                pass
        try:
            self.audio.terminate()
        except:
            pass
    
    async def send_audio(self, session):
        """Capture and send audio from microphone to Gemini"""
        print("🎤 Listening...")
        
        # Use thread pool executor to run blocking audio read in a separate thread
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        try:
            while self.is_running:
                # Run blocking read() in executor to avoid blocking the event loop
                audio_data = await loop.run_in_executor(
                    executor,
                    lambda: self.input_stream.read(
                        self.audio_config["chunk_size"],
                        exception_on_overflow=False
                    )
                )
                
                # Send audio to Gemini using send_realtime_input
                if audio_data:
                    await session.send_realtime_input(
                        audio=types.Blob(
                            data=audio_data,
                            mime_type=f"audio/pcm;rate={self.audio_config['sample_rate']}"
                        )
                    )
                
                # Small delay
                await asyncio.sleep(0.01)
                
        except asyncio.CancelledError:
            if self.app_config["debug"]:
                print("\n🛑 Audio input stopped")
        except Exception as e:
            print(f"✗ Error in audio input: {e}")
            if self.app_config["debug"]:
                import traceback
                traceback.print_exc()
    
    async def receive_audio(self, session):
        """Receive and play audio responses from Gemini"""
        print("🔊 Ready to play responses...")
        
        try:
            # Keep receiving messages continuously - session.receive() stops after turn_complete
            # so we need to call it in a loop to handle multiple conversation turns
            while self.is_running:
                try:
                    async for response in session.receive():
                        # Handle text transcription
                        if response.text and self.app_config["show_transcription"]:
                            print(f"💬 {response.text}")
                        
                        # Handle audio data
                        if response.data:
                            try:
                                self.output_stream.write(response.data)
                            except Exception as e:
                                if self.app_config["debug"]:
                                    print(f"⚠️  Audio playback error: {e}")
                        
                        # Handle server messages
                        if response.server_content:
                            if response.server_content.turn_complete:
                                if self.app_config["debug"]:
                                    print("✓ Turn complete")
                                # Break inner loop to get next turn, but continue outer loop
                                break
                except Exception as e:
                    if self.is_running:
                        if self.app_config["debug"]:
                            print(f"⚠️  Error receiving response: {e}")
                        # Small delay before retrying
                        await asyncio.sleep(0.1)
                    else:
                        break
                        
        except asyncio.CancelledError:
            if self.app_config["debug"]:
                print("\n🛑 Audio output stopped")
        except Exception as e:
            print(f"✗ Error in audio output: {e}")
            if self.app_config["debug"]:
                import traceback
                traceback.print_exc()
    
    async def run_session(self):
        """Run a single session with Gemini Live API"""
        # Configure Gemini Live session
        config = types.LiveConnectConfig(
            response_modalities=self.api_config["response_modalities"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.api_config["voice_name"]
                    )
                )
            )
        )
        
        # Connect to Gemini Live API
        async with self.client.aio.live.connect(
            model=self.api_config["model"],
            config=config
        ) as session:
            
            # Send system instruction
            await session.send(input=self.system_instruction, end_of_turn=True)
            
            print(f"\n✓ Connected to Gemini Live API")
            print(f"💬 {self.hebrew_config['greeting']}")
            print("⚠️  Press Ctrl+C to exit\n")
            
            # Reset connection attempts on successful connection
            self.connection_attempts = 0
            
            # Run send and receive tasks concurrently
            send_task = asyncio.create_task(self.send_audio(session))
            receive_task = asyncio.create_task(self.receive_audio(session))
            
            # Wait for both tasks
            await asyncio.gather(send_task, receive_task)
    
    async def run(self):
        """Main loop with reconnection support"""
        print("=" * 60)
        print("🤖 Advanced Hebrew Doll - Gemini Live API")
        print("=" * 60)
        
        # Setup audio once
        self.setup_audio_streams()
        self.is_running = True
        
        try:
            while self.is_running:
                try:
                    await self.run_session()
                    
                except KeyboardInterrupt:
                    raise  # Re-raise to exit gracefully
                    
                except Exception as e:
                    print(f"\n✗ Connection error: {e}")
                    
                    # Check if we should reconnect
                    if not self.app_config["auto_reconnect"]:
                        raise
                    
                    self.connection_attempts += 1
                    
                    if self.connection_attempts > self.app_config["max_reconnect_attempts"]:
                        print(f"\n✗ Max reconnection attempts ({self.app_config['max_reconnect_attempts']}) reached")
                        raise
                    
                    # Wait before reconnecting
                    delay = self.app_config["reconnect_delay"]
                    print(f"🔄 Reconnecting in {delay} seconds... (Attempt {self.connection_attempts})")
                    await asyncio.sleep(delay)
                    print("🔄 Attempting to reconnect...")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down gracefully...")
        except Exception as e:
            print(f"\n✗ Fatal error: {e}")
            if self.app_config["debug"]:
                import traceback
                traceback.print_exc()
        finally:
            self.is_running = False
            self.close_audio_streams()
            print("✓ Cleanup complete")


async def main():
    """Entry point for the application"""
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not found in environment variables")
        api_key = input("Please enter your Google AI API key: ").strip()
        
        if not api_key:
            print("✗ API key is required. Exiting.")
            sys.exit(1)
    
    # Create and run the doll
    doll = AdvancedHebrewDoll(api_key=api_key)
    await doll.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
