# Latency & Response Tuning Guide

This guide shows you where to tune latency and response behavior in the codebase.

## 📍 Main Configuration Locations

### 1. **`config.py`** (Advanced Version)
The main configuration file for `gemini_live_advanced.py`:

```python
# Audio Configuration - Most important for latency
AUDIO_CONFIG = {
    "sample_rate": 16000,      # Lower = less CPU, higher latency
                              # Higher = more CPU, lower latency
                              # Options: 16000, 24000, 48000
    
    "chunk_size": 1024,        # Smaller = lower latency, less stable
                              # Larger = higher latency, more stable
                              # Options: 512, 1024, 2048, 4096
}

# API Configuration - Affects response behavior
API_CONFIG = {
    "model": "gemini-2.0-flash-exp",  # Model choice affects speed
    "response_modalities": ["AUDIO"],  # Can add "TEXT" for faster feedback
    "voice_name": "Puck",              # Voice selection
}
```

### 2. **`gemini_live_hebrew.py`** (Basic Version)
Direct constants at the top of the file:

```python
# Lines 23-27
CHUNK_SIZE = 1024              # Buffer size - smaller = lower latency
INPUT_SAMPLE_RATE = 16000      # Microphone sample rate
OUTPUT_SAMPLE_RATE = 24000     # Speaker sample rate (Gemini's output)
```

### 3. **Sleep Delays** (Both Files)

#### In `send_audio()` method:
- **Line 118** (`gemini_live_hebrew.py`): `await asyncio.sleep(0.01)`
  - Delay between sending audio chunks
  - **Lower value** = more frequent sends = lower latency but more API calls
  - **Higher value** = less frequent sends = higher latency but fewer API calls
  - Range: `0.001` (very aggressive) to `0.05` (conservative)

#### In `receive_audio()` method:
- **Line 153** (`gemini_live_hebrew.py`): `await asyncio.sleep(0.05)`
  - Delay after turn completion before checking for next response
  - **Lower value** = faster response detection = lower latency
  - Range: `0.01` to `0.1`

- **Line 159** (`gemini_live_hebrew.py`): `await asyncio.sleep(0.1)`
  - Delay on error retry
  - Usually fine to leave as-is

## 🎯 Latency Optimization Strategies

### **For Lowest Latency:**

1. **Reduce chunk size:**
   ```python
   # In config.py or gemini_live_hebrew.py
   CHUNK_SIZE = 512  # or even 256
   ```

2. **Reduce send delay:**
   ```python
   # In send_audio() method
   await asyncio.sleep(0.001)  # Very aggressive
   ```

3. **Reduce turn completion delay:**
   ```python
   # In receive_audio() method
   await asyncio.sleep(0.01)  # Faster response detection
   ```

4. **Use faster model:**
   ```python
   # In config.py API_CONFIG
   "model": "gemini-2.0-flash-exp"  # Flash models are faster
   ```

### **For Stability (Higher Latency but More Reliable):**

1. **Increase chunk size:**
   ```python
   CHUNK_SIZE = 2048  # or 4096
   ```

2. **Increase send delay:**
   ```python
   await asyncio.sleep(0.02)  # More conservative
   ```

3. **Increase turn completion delay:**
   ```python
   await asyncio.sleep(0.1)  # More stable
   ```

## 🔧 Advanced Tuning Options

### **API-Level Configuration** (in `gemini_live_advanced.py`)

You can add generation config to the `LiveConnectConfig`:

```python
config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    # Add these for response tuning:
    temperature=0.7,           # Lower = faster, more deterministic
    top_p=0.95,               # Lower = faster responses
    top_k=40,                 # Lower = faster token selection
    max_output_tokens=1024,   # Limit response length (faster)
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Puck"
            )
        )
    )
)
```

### **Response Modalities**

You can request both TEXT and AUDIO for faster feedback:

```python
"response_modalities": ["TEXT", "AUDIO"]
```

This shows text transcription immediately while audio is being generated.

## 📊 Latency Impact Summary

| Setting | Lower Value | Higher Value |
|---------|-------------|--------------|
| `chunk_size` | ⚡ Lower latency, less stable | 🛡️ Higher latency, more stable |
| `sample_rate` | ⚡ Less CPU, higher latency | 🔥 More CPU, lower latency |
| `send delay` | ⚡ More frequent sends | 🛡️ Less frequent sends |
| `turn delay` | ⚡ Faster response detection | 🛡️ More stable detection |
| `temperature` | ⚡ Faster, deterministic | 🎨 Slower, creative |

## 🎛️ Recommended Settings by Use Case

### **Real-time Conversation (Low Latency)**
```python
CHUNK_SIZE = 512
INPUT_SAMPLE_RATE = 16000
await asyncio.sleep(0.005)  # In send_audio
await asyncio.sleep(0.01)   # After turn_complete
```

### **Stable Production (Balanced)**
```python
CHUNK_SIZE = 1024
INPUT_SAMPLE_RATE = 16000
await asyncio.sleep(0.01)   # In send_audio
await asyncio.sleep(0.05)   # After turn_complete
```

### **High Quality (Higher Latency)**
```python
CHUNK_SIZE = 2048
INPUT_SAMPLE_RATE = 24000
await asyncio.sleep(0.02)   # In send_audio
await asyncio.sleep(0.1)    # After turn_complete
```

## 🔍 Where to Find Each Setting

### **Basic Version (`gemini_live_hebrew.py`):**
- **Line 23**: `CHUNK_SIZE`
- **Line 26**: `INPUT_SAMPLE_RATE`
- **Line 27**: `OUTPUT_SAMPLE_RATE`
- **Line 118**: Send delay in `send_audio()`
- **Line 153**: Turn completion delay in `receive_audio()`
- **Line 183**: Voice name in `run()`

### **Advanced Version (`gemini_live_advanced.py`):**
- **`config.py`**: All audio and API settings
- **Line 187**: Send delay in `send_audio()`
- **Line 232**: Error retry delay in `receive_audio()`
- **Line 248**: API config in `run_session()`

## ⚠️ Important Notes

1. **Too low latency** can cause:
   - Audio glitches
   - Unstable connections
   - Higher CPU usage
   - More API errors

2. **Network latency** is also a factor:
   - Use wired internet when possible
   - Check your ping to Google's servers
   - Consider geographic location

3. **Hardware matters**:
   - USB microphones often have lower latency than built-in
   - Better sound cards = lower latency
   - CPU speed affects processing time

4. **Test incrementally**:
   - Change one setting at a time
   - Test thoroughly before deploying
   - Monitor for errors and stability

