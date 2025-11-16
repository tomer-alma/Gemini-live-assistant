"""
Advanced Configuration for Gemini Live Hebrew STS
Modify these settings to customize the behavior
"""

# Audio Configuration
AUDIO_CONFIG = {
    # Sample rate in Hz (16000, 24000, 48000)
    "sample_rate": 16000,
    
    # Number of audio channels (1=mono, 2=stereo)
    "channels": 1,
    
    # Audio format (paInt16, paInt32, paFloat32)
    "format": "paInt16",
    
    # Buffer size (smaller = lower latency, larger = more stable)
    # Common values: 512, 1024, 2048
    "chunk_size": 1024,
    
    # Input device index (None = default, or specific device number)
    "input_device": None,
    
    # Output device index (None = default, or specific device number)
    "output_device": None,
}

# Gemini Live API Configuration
API_CONFIG = {
    # Model to use
    "model": "gemini-2.0-flash-exp",
    
    # Response modalities (["AUDIO"] or ["TEXT", "AUDIO"])
    "response_modalities": ["AUDIO"],
    
    # Voice name options: Puck, Charon, Kore, Fenrir, Aoede
    "voice_name": "Puck",
    
    # Speech settings
    "speech_config": {
        # Enable/disable speech output
        "enabled": True,
    },
}

# Application Behavior
APP_CONFIG = {
    # Show transcription of speech (if available)
    "show_transcription": True,
    
    # Enable debug logging
    "debug": False,
    
    # Auto-reconnect on connection loss
    "auto_reconnect": True,
    
    # Maximum reconnection attempts
    "max_reconnect_attempts": 3,
    
    # Delay between reconnection attempts (seconds)
    "reconnect_delay": 5,
}

# Hebrew-specific Settings
HEBREW_CONFIG = {
    # Enable RTL (Right-to-Left) text formatting
    "rtl_text": True,
    
    # Hebrew font preference for logging
    "font_hint": "Try using a terminal with Hebrew support",
    
    # Default greeting message
    "greeting": "שלום! אני כאן לדבר איתך בעברית. במה אוכל לעזור?",
}

# Safety and Content Settings
SAFETY_CONFIG = {
    # Content filtering level (strict, moderate, permissive)
    "content_filter": "moderate",
    
    # Maximum conversation duration (minutes, 0 = unlimited)
    "max_duration": 0,
    
    # Enable parental controls
    "parental_controls": False,
}

# Performance Optimization
PERFORMANCE_CONFIG = {
    # Use asyncio optimizations
    "async_optimizations": True,
    
    # Buffer pre-allocation
    "buffer_prealloc": True,
    
    # Enable audio compression (if supported)
    "audio_compression": False,
}


def get_config():
    """
    Get the complete configuration dictionary
    Returns a merged configuration from all sections
    """
    return {
        "audio": AUDIO_CONFIG,
        "api": API_CONFIG,
        "app": APP_CONFIG,
        "hebrew": HEBREW_CONFIG,
        "safety": SAFETY_CONFIG,
        "performance": PERFORMANCE_CONFIG,
    }


def print_config():
    """Print the current configuration"""
    import json
    config = get_config()
    print("Current Configuration:")
    print(json.dumps(config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    print_config()
