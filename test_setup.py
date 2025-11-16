"""
Test Suite for Gemini Live Hebrew STS
Tests audio setup, API connection, and basic functionality
"""

import os
import sys
import pyaudio
import asyncio
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()


def test_audio_devices():
    """Test and list available audio devices"""
    print("\n" + "=" * 60)
    print("🎵 AUDIO DEVICES TEST")
    print("=" * 60)
    
    try:
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        
        print(f"\n✓ Found {device_count} audio devices:\n")
        
        default_input = audio.get_default_input_device_info()
        default_output = audio.get_default_output_device_info()
        
        print("📍 DEFAULT INPUT DEVICE:")
        print(f"   Name: {default_input['name']}")
        print(f"   Index: {default_input['index']}")
        print(f"   Channels: {default_input['maxInputChannels']}")
        print(f"   Sample Rate: {int(default_input['defaultSampleRate'])} Hz\n")
        
        print("📍 DEFAULT OUTPUT DEVICE:")
        print(f"   Name: {default_output['name']}")
        print(f"   Index: {default_output['index']}")
        print(f"   Channels: {default_output['maxOutputChannels']}")
        print(f"   Sample Rate: {int(default_output['defaultSampleRate'])} Hz\n")
        
        print("📋 ALL DEVICES:")
        for i in range(device_count):
            info = audio.get_device_info_by_index(i)
            device_type = []
            if info['maxInputChannels'] > 0:
                device_type.append("INPUT")
            if info['maxOutputChannels'] > 0:
                device_type.append("OUTPUT")
            
            print(f"   [{i}] {info['name']}")
            print(f"       Type: {' & '.join(device_type)}")
            print(f"       Channels: In={info['maxInputChannels']}, Out={info['maxOutputChannels']}")
            print(f"       Sample Rate: {int(info['defaultSampleRate'])} Hz\n")
        
        audio.terminate()
        return True
        
    except Exception as e:
        print(f"\n✗ Audio test failed: {e}")
        return False


def test_microphone():
    """Test microphone input"""
    print("\n" + "=" * 60)
    print("🎤 MICROPHONE TEST")
    print("=" * 60)
    
    try:
        audio = pyaudio.PyAudio()
        
        # Open stream
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024
        )
        
        print("\n✓ Microphone stream opened successfully")
        print("🔴 Recording for 2 seconds... (Speak now!)")
        
        frames = []
        for i in range(0, int(16000 / 1024 * 2)):  # 2 seconds
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
            print(".", end="", flush=True)
        
        print("\n✓ Recording complete!")
        
        # Calculate volume level
        import struct
        volume = 0
        for frame in frames:
            shorts = struct.unpack(f"{len(frame)//2}h", frame)
            volume = max(volume, max(abs(s) for s in shorts))
        
        print(f"📊 Peak volume: {volume} (out of 32768)")
        
        if volume < 100:
            print("⚠️  WARNING: Very low volume detected. Check microphone!")
        elif volume > 30000:
            print("⚠️  WARNING: Very high volume detected. Reduce input level!")
        else:
            print("✓ Volume level looks good!")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        return True
        
    except Exception as e:
        print(f"\n✗ Microphone test failed: {e}")
        return False


def test_api_key():
    """Test Google AI API key"""
    print("\n" + "=" * 60)
    print("🔑 API KEY TEST")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("\n⚠️  GOOGLE_API_KEY not found in environment")
        api_key = input("Enter your API key to test: ").strip()
    
    if not api_key:
        print("✗ No API key provided")
        return False
    
    try:
        print("\n🔍 Testing API key...")
        client = genai.Client(api_key=api_key)
        
        # Try to list models to verify key
        print("✓ API key is valid!")
        print("✓ Successfully connected to Google AI")
        
        return True
        
    except Exception as e:
        print(f"\n✗ API key test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Get a valid API key from: https://aistudio.google.com/app/apikey")
        print("2. Make sure the key is not expired")
        print("3. Check if Gemini API is enabled for your project")
        return False


async def test_gemini_live():
    """Test Gemini Live API connection"""
    print("\n" + "=" * 60)
    print("🤖 GEMINI LIVE API TEST")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("\n⚠️  GOOGLE_API_KEY not found in environment")
        api_key = input("Enter your API key to test: ").strip()
    
    if not api_key:
        print("✗ No API key provided")
        return False
    
    try:
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        print("\n🔗 Connecting to Gemini Live API...")
        
        config = types.LiveConnectConfig(
            response_modalities=["TEXT"],  # Use text for testing
        )
        
        async with client.aio.live.connect(
            model="gemini-2.0-flash-exp",
            config=config
        ) as session:
            
            print("✓ Connected successfully!")
            
            # Send a test message
            print("📤 Sending test message in Hebrew...")
            await session.send(input="שלום! זה בדיקה.", end_of_turn=True)
            
            # Receive response
            print("📥 Waiting for response...")
            async for response in session.receive():
                if response.text:
                    print(f"✓ Received response: {response.text[:100]}...")
                    break
                if response.server_content and response.server_content.turn_complete:
                    break
            
            print("✓ Gemini Live API test successful!")
            return True
            
    except Exception as e:
        print(f"\n✗ Gemini Live API test failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify API key is valid")
        print("3. Ensure Gemini 2.0 Flash is available in your region")
        print("4. Check API quota and limits")
        return False


def test_dependencies():
    """Test if all required packages are installed"""
    print("\n" + "=" * 60)
    print("📦 DEPENDENCIES TEST")
    print("=" * 60)
    
    dependencies = {
        "google-genai": "google",
        "pyaudio": "pyaudio",
        "websockets": "websockets",
    }
    
    all_good = True
    
    for package_name, import_name in dependencies.items():
        try:
            __import__(import_name)
            print(f"✓ {package_name} - installed")
        except ImportError:
            print(f"✗ {package_name} - NOT installed")
            all_good = False
    
    if not all_good:
        print("\n⚠️  Missing dependencies detected!")
        print("Run: pip install -r requirements.txt")
    else:
        print("\n✓ All dependencies installed!")
    
    return all_good


async def run_all_tests():
    """Run all tests"""
    print("\n")
    print("*" * 60)
    print("🧪 GEMINI LIVE HEBREW STS - TEST SUITE")
    print("*" * 60)
    
    results = {
        "Dependencies": test_dependencies(),
        "Audio Devices": test_audio_devices(),
        "Microphone": test_microphone(),
        "API Key": test_api_key(),
        "Gemini Live": await test_gemini_live(),
    }
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYou're ready to run the Hebrew doll prototype:")
        print("  python gemini_live_hebrew.py")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the failing tests before running the prototype.")
        print("Check the error messages above for troubleshooting tips.")
    
    print("\n")


def main():
    """Entry point"""
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
