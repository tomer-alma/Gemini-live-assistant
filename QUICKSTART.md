# Quick Start Guide - Hebrew Doll Prototype

## 5-Minute Setup

### Step 1: Get Your API Key (1 minute)
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 2: Install Dependencies (2 minutes)

**macOS:**
```bash
# Install PortAudio
brew install portaudio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

**Linux (Ubuntu/Debian/Raspberry Pi OS):**
```bash
# Update system
sudo apt-get update

# Install dependencies
sudo apt-get install -y portaudio19-dev python3-pyaudio python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

**Linux (Fedora/RHEL/CentOS):**
```bash
# Install dependencies
sudo dnf install -y portaudio-devel python3-pyaudio python3-virtualenv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

**Linux (Arch/Manjaro):**
```bash
# Install dependencies
sudo pacman -S portaudio python-pyaudio

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

**Windows:**
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Note: If PyAudio fails, download wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

**Or use automated setup (Unix/Linux/macOS):**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Set API Key (30 seconds)

**Unix/Linux/macOS:**
```bash
export GOOGLE_API_KEY="your_api_key_here"

# Or permanently:
echo 'export GOOGLE_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (Command Prompt):**
```bash
set GOOGLE_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```bash
$env:GOOGLE_API_KEY="your_api_key_here"
```

### Step 4: Test Everything (1 minute)
```bash
source venv/bin/activate
python3 test_setup.py
```

### Step 5: Run! (30 seconds)
```bash
python3 gemini_live_hebrew.py
```

That's it! Start speaking in Hebrew! 🎤

---

## Audio Setup

### Find Your Audio Devices

**All Platforms:**
```bash
# List audio devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

**Linux/Raspberry Pi:**
```bash
# Test microphone
arecord -d 5 test.wav
aplay test.wav

# List ALSA devices
arecord -l
aplay -l
```

**macOS:**
```bash
# Check audio in System Settings > Sound
```

**Windows:**
```bash
# Check audio in Settings > System > Sound
```

### Configure Audio Device
Edit `config.py`:
```python
AUDIO_CONFIG = {
    "input_device": 1,   # Your mic device number (or None for default)
    "output_device": 2,  # Your speaker device number (or None for default)
}
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pyaudio'"

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install portaudio-devel
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### "No audio input detected"

**Linux:**
```bash
# Check devices
arecord -l

# Test microphone
arecord -d 5 -f cd test.wav
aplay test.wav

# Set correct device in config.py
```

**macOS:**
- Check microphone permissions (Settings > Privacy & Security > Microphone)
- Enable access for Terminal/your IDE

**Windows:**
- Check Settings > Privacy > Microphone
- Ensure microphone permissions are enabled

### "API key invalid"
- Make sure you copied the entire key
- Check if key is from https://aistudio.google.com/app/apikey
- Try creating a new key

### "High CPU usage" (especially on Raspberry Pi)
Edit `config.py`:
```python
AUDIO_CONFIG = {
    "sample_rate": 16000,  # Lower than 24000
    "chunk_size": 1024,    # Increase if unstable
}
```

### "Hebrew text displays incorrectly"
- Use a terminal that supports RTL (Right-to-Left) text
- Set language: `export LANG=he_IL.UTF-8`
- Try a different terminal emulator

---

## Auto-Start on Boot (Linux/Raspberry Pi)

For production deployments, you can set up the doll to start automatically.

Create systemd service:
```bash
sudo nano /etc/systemd/system/hebrew-doll.service
```

Add:
```ini
[Unit]
Description=Hebrew STS Doll
After=network.target

[Service]
Type=simple
User=pi  # Change to your username
WorkingDirectory=/home/pi/gemini-hebrew-doll  # Change to your path
Environment="GOOGLE_API_KEY=your_key_here"
ExecStart=/home/pi/gemini-hebrew-doll/venv/bin/python /home/pi/gemini-hebrew-doll/gemini_live_hebrew.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable hebrew-doll.service
sudo systemctl start hebrew-doll.service
```

---

## Examples

### Basic Usage
```bash
python gemini_live_hebrew.py
```

### Try Different Personalities
```bash
python custom_personalities.py
```

### Test Your Setup
```bash
python test_setup.py
```

---

## Common Commands

**Activate virtual environment:**

Unix/Linux/macOS:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

**Update dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

**Check audio devices:**
```bash
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
```

**Linux/Raspberry Pi specific:**

Check CPU temperature:
```bash
# Raspberry Pi
vcgencmd measure_temp

# Linux with lm-sensors
sensors
```

Monitor system:
```bash
htop
```

View service logs:
```bash
sudo journalctl -u hebrew-doll.service -f
```

---

## Tips

**General:**
✅ Use a good quality microphone
✅ Speak clearly in Hebrew
✅ Wait for response before speaking again
✅ Test in a quiet environment
✅ Check API quota regularly

**For Raspberry Pi:**
✅ Use Raspberry Pi 4 or 5 for best performance
✅ Use Ethernet instead of WiFi for stability
✅ Use USB sound card for better audio quality
✅ Keep CPU temperature under 80°C
✅ Use 16000 Hz sample rate to save CPU
✅ Consider heatsink or fan for continuous use

**For Laptops/Desktops:**
✅ Close unnecessary background applications
✅ Use wired internet when possible
✅ Disable Wi-Fi power saving mode
✅ Use external USB microphone for better quality

---

## Getting Help

- 📖 Complete README: See README.md
- 📖 Project Structure: See PROJECT_STRUCTURE.md
- 🐛 Report issues: Check terminal output
- 💡 Ideas: Modify custom_personalities.py
- 📚 Gemini Docs: https://ai.google.dev/docs

---

Happy prototyping! 🚀
