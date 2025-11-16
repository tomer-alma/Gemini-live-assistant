"""
Gemini Live API - Real-time Speech-to-Speech in Hebrew
A prototype for conversational AI doll using Google's Gemini Live API
"""

import asyncio
import base64
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
import pyaudio
import websockets
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Audio configuration
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
INPUT_SAMPLE_RATE = 16000  # Input (microphone) sample rate
OUTPUT_SAMPLE_RATE = 24000  # Output (speaker) sample rate - Gemini returns audio at 24kHz

class HebrewDollPrototype:
    """Real-time speech-to-speech conversational AI in Hebrew"""
    
    def __init__(self, api_key: str, system_instruction: Optional[str] = None):
        """
        Initialize the Hebrew Doll prototype
        
        Args:
            api_key: Google AI API key
            system_instruction: Custom system instruction for the AI personality
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.audio = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.is_running = False
        
        # Default Hebrew doll personality
        self.system_instruction = system_instruction or """
        אתה בובה חכמה וידידותית שמדברת עברית.
        תפקידך להיות חבר טוב, לשוחח בצורה טבעית וחמה, ולעזור לילדים ללמוד.
        דבר בעברית פשוטה וברורה, השתמש בהומור מתאים לילדים, והיה תמיד חיובי ומעודד.
        
        You are a smart and friendly doll that speaks Hebrew.
        Your role is to be a good friend, chat naturally and warmly, and help children learn.
        Speak in simple and clear Hebrew, use child-appropriate humor, and always be positive and encouraging.
        """
        
    def setup_audio_streams(self):
        """Initialize audio input and output streams"""
        try:
            # Input stream (microphone) - 16kHz for input
            self.input_stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=INPUT_SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE
            )
            
            # Output stream (speaker) - 24kHz for Gemini's audio output
            self.output_stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=OUTPUT_SAMPLE_RATE,
                output=True,
                frames_per_buffer=CHUNK_SIZE
            )
            
            print("✓ Audio streams initialized")
        except Exception as e:
            print(f"✗ Error initializing audio: {e}")
            raise
    
    def close_audio_streams(self):
        """Close audio streams safely"""
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        self.audio.terminate()
    
    async def send_audio(self, session):
        """Capture and send audio from microphone to Gemini"""
        print("🎤 Listening... (Press Ctrl+C to stop)")
        
        # Use thread pool executor to run blocking audio read in a separate thread
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=1)
        
        try:
            while self.is_running:
                # Run blocking read() in executor to avoid blocking the event loop
                audio_data = await loop.run_in_executor(
                    executor,
                    lambda: self.input_stream.read(CHUNK_SIZE, exception_on_overflow=False)
                )
                
                # Only send if we have data
                if audio_data:
                    # Send audio to Gemini using send_realtime_input
                    await session.send_realtime_input(
                        audio=types.Blob(data=audio_data, mime_type="audio/pcm;rate=16000")
                    )
                
                # Small delay to prevent overwhelming the API
                await asyncio.sleep(0.01)
                
        except asyncio.CancelledError:
            print("\n🛑 Stopping audio input...")
        except Exception as e:
            print(f"✗ Error in audio input: {e}")
    
    async def receive_audio(self, session):
        """Receive and play audio responses from Gemini"""
        print("🔊 Ready to play responses...")
        
        try:
            # Keep receiving messages continuously - session.receive() stops after turn_complete
            # so we need to call it in a loop to handle multiple conversation turns
            while self.is_running:
                try:
                    # Use a timeout to prevent indefinite blocking
                    # This allows the send_audio task to continue sending
                    async for response in session.receive():
                        # Handle different response types
                        if response.text:
                            print(f"💬 Text: {response.text}")
                        
                        if response.data:
                            # Play received audio
                            audio_data = response.data
                            if audio_data:
                                self.output_stream.write(audio_data)
                        
                        if response.server_content:
                            # Handle turn completion - but continue listening for more turns
                            if response.server_content.turn_complete:
                                print("✓ Turn complete")
                                # Break inner loop to get next turn, but continue outer loop
                                # Small delay to allow audio input to be processed
                                await asyncio.sleep(0.05)
                                break
                except Exception as e:
                    if self.is_running:
                        print(f"⚠️  Error receiving response: {e}")
                        # Small delay before retrying
                        await asyncio.sleep(0.1)
                    else:
                        break
                        
        except asyncio.CancelledError:
            print("\n🛑 Stopping audio output...")
        except Exception as e:
            print(f"✗ Error in audio output: {e}")
    
    async def run(self):
        """Main loop for real-time speech-to-speech interaction"""
        print("=" * 60)
        print("🤖 Hebrew Doll Prototype - Gemini Live API")
        print("=" * 60)
        
        # Setup audio
        self.setup_audio_streams()
        
        # Configure Gemini Live session
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Puck"  # You can change this to other voices
                    )
                )
            )
        )
        
        self.is_running = True
        
        try:
            # Connect to Gemini Live API
            async with self.client.aio.live.connect(
                model="gemini-2.0-flash-exp",
                config=config
            ) as session:
                
                # Send system instruction
                await session.send(
                    input=self.system_instruction,
                    end_of_turn=True
                )
                
                print("\n✓ Connected to Gemini Live API")
                print("💡 Speak in Hebrew to interact with the doll")
                print("⚠️  Press Ctrl+C to exit\n")
                
                # Run send and receive tasks concurrently
                send_task = asyncio.create_task(self.send_audio(session))
                receive_task = asyncio.create_task(self.receive_audio(session))
                
                # Wait for both tasks
                await asyncio.gather(send_task, receive_task)
                
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down gracefully...")
        except Exception as e:
            print(f"\n✗ Error: {e}")
        finally:
            self.is_running = False
            self.close_audio_streams()
            print("✓ Cleanup complete")


async def main():
    """Entry point for the application"""
    
    # Get API key from environment or prompt user
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not found in environment variables")
        api_key = input("Please enter your Google AI API key: ").strip()
        
        if not api_key:
            print("✗ API key is required. Exiting.")
            sys.exit(1)
    
    # Create and run the doll prototype
    doll = HebrewDollPrototype(api_key=api_key)
    await doll.run()


if __name__ == "__main__":
    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
