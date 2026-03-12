import os
from gtts import gTTS

def generate_audio(text, lang_code='en', filename='output.mp3'):
    """
    Given text and a language code (te, hi, en), creates an mp3 audio file
    mimicking the Assistant's voice.
    """
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        output_dir = os.path.join(os.getcwd(), 'static', 'audio')
        
        # Ensure audio directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        file_path = os.path.join(output_dir, filename)
        tts.save(file_path)
        print(f"[Voice] Saved audio to {file_path}")
        return file_path
        
    except Exception as e:
        print(f"[Voice] Error generating audio: {e}")
        return None

if __name__ == '__main__':
    # Generate some test audio scripts
    generate_audio("Hello, I am your interior design buddy.", 'en', 'test_en.mp3')
    generate_audio("नमस्ते, मैं आपका इंटीरियर डिजाइन बडी हूँ।", 'hi', 'test_hi.mp3')
    generate_audio("నమస్కారం, నేను మీ ఇంటీరియర్ డిజైన్ బడ్డీని.", 'te', 'test_te.mp3')
