# Gemini Live API - Hebrew STS Doll Prototype

A real-time speech-to-speech conversational AI prototype in Hebrew using Google's Gemini Live API. Perfect for creating interactive smart dolls, educational toys, or voice assistants.

## Features

- ✅ **Real-time speech-to-speech** - No intermediate text processing
- ✅ **Hebrew language support** - Native Hebrew conversation
- ✅ **Low latency** - Fast response times
- ✅ **Customizable personality** - Easy to modify AI behavior
- ✅ **Simple setup** - Few dependencies, easy to run

## Prerequisites

- Python 3.8 or higher
- Google AI API key ([Get one here](https://aistudio.google.com/app/apikey))
- Microphone and speakers
- Working audio drivers (PortAudio)

## Installation

### 1. Clone or Download the Project

```bash
# If using git
git clone <your-repo>
cd gemini-hebrew-doll

# Or just download the files to a folder
```

### 2. Install System Dependencies

**macOS:**
```bash
brew install portaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Windows:**
PyAudio will be installed with pip. If you encounter issues, download the wheel from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### 3. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Configure API Key

**Option A: Environment Variable**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# Then load it:
export GOOGLE_API_KEY="your_api_key_here"
```

**Option B: Direct Input**
The program will prompt for your API key if not found in environment.

## Usage

### Basic Usage

```bash
python3 gemini_live_hebrew.py
```

The program will:
1. Initialize audio streams
2. Connect to Gemini Live API
3. Start listening for your voice
4. Respond in real-time with voice

### Custom Personality

Create a file called `custom_personality.py`:

```python
import asyncio
from gemini_live_hebrew import HebrewDollPrototype

CUSTOM_INSTRUCTION = """
אתה בובה של נסיכה קסומה שמדברת עברית.
את חיה בטירה קסומה ואוהבת לספר סיפורים על הרפתקאות.
דברי בצורה נלהבת ושמחה, והשתמשי בדימיון רב.

You are a magical princess doll that speaks Hebrew.
You live in a magical castle and love to tell adventure stories.
Speak enthusiastically and happily, and use lots of imagination.
"""

async def main():
    doll = HebrewDollPrototype(
        api_key="your_key_here",
        system_instruction=CUSTOM_INSTRUCTION
    )
    await doll.run()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python3 custom_personality.py
```

## Audio Configuration

The default configuration is:
- **Sample Rate:** 16000 Hz
- **Channels:** Mono (1)
- **Format:** 16-bit PCM

To modify, edit these constants in `gemini_live_hebrew.py`:

```python
CHUNK_SIZE = 1024      # Buffer size
SAMPLE_RATE = 16000    # Sample rate in Hz
CHANNELS = 1           # Mono audio
```

## Voice Selection

The default voice is "Puck". To change it, modify the voice configuration:

```python
config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Aoede"  # Try: Puck, Charon, Kore, Fenrir, Aoede
            )
        )
    )
)
```

Available voices:
- **Puck** - Neutral, friendly
- **Charon** - Deep, calm
- **Kore** - Warm, expressive
- **Fenrir** - Energetic
- **Aoede** - Smooth, melodic

## Troubleshooting

### Audio Issues

**No audio input/output:**
```bash
# List available audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

**Permission denied on macOS:**
- Go to System Settings > Privacy & Security > Microphone
- Enable access for Terminal/your IDE

### API Issues

**Rate limits:**
- Gemini Live API has rate limits
- Check your quota at https://aistudio.google.com/

**Connection errors:**
- Ensure stable internet connection
- Check if API key is valid
- Try again in a few moments

### Hebrew Text Display

If Hebrew text doesn't display correctly in your terminal:
- Use a terminal that supports RTL (Right-to-Left) text
- Or run with: `LANG=he_IL.UTF-8 python gemini_live_hebrew.py`

## Architecture

```
┌─────────────┐
│  Microphone │
└──────┬──────┘
       │ Audio Stream (PCM)
       ▼
┌──────────────────┐
│  PyAudio Input   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      WebSocket      ┌─────────────────┐
│ Gemini Live API  │◄──────────────────►│  Google Cloud   │
└──────┬───────────┘                     └─────────────────┘
       │
       ▼
┌──────────────────┐
│  PyAudio Output  │
└──────┬───────────┘
       │ Audio Stream (PCM)
       ▼
┌──────────────┐
│   Speakers   │
└──────────────┘
```

## Performance Tips

1. **Reduce latency:** Use smaller CHUNK_SIZE (512 or 1024)
2. **Better quality:** Increase SAMPLE_RATE to 24000 Hz
3. **Stability:** Add error recovery and reconnection logic
4. **Production:** Implement voice activity detection (VAD)

## Example Use Cases

- 🧸 **Smart Toys** - Interactive dolls and action figures
- 📚 **Educational Tools** - Language learning companions
- 🤖 **Voice Assistants** - Hebrew-speaking home assistants
- 🎮 **Game Characters** - NPCs with voice interaction
- 👴 **Elderly Care** - Conversational companions

## Security Notes

⚠️ **Important:**
- Never commit your API key to version control
- Use environment variables or secure key management
- Monitor your API usage and costs
- Set up usage limits in Google Cloud Console

## API Costs

Check current pricing at: https://ai.google.dev/pricing

Gemini Live API charges per audio duration. Monitor your usage!

## Limitations

- Requires stable internet connection
- API rate limits apply
- Audio quality depends on microphone
- Hebrew pronunciation may vary
- Response time depends on network latency

## Future Enhancements

- [ ] Voice Activity Detection (VAD)
- [ ] Multi-turn conversation memory
- [ ] Emotion detection in voice
- [ ] Multiple language support
- [ ] Wake word detection
- [ ] Local audio processing
- [ ] WebRTC support for web integration

## License

MIT License - feel free to use in your projects!

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

- 📖 [Gemini API Documentation](https://ai.google.dev/docs)
- 💬 [Google AI Community](https://discuss.ai.google.dev/)
- 🐛 [Report Issues](https://github.com/your-repo/issues)

## Credits

Built with:
- [Google Gemini API](https://ai.google.dev/)
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
- [websockets](https://websockets.readthedocs.io/)

---

Made with ❤️ for Hebrew-speaking AI interactions
