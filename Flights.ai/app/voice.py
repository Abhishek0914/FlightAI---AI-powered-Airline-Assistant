try:
    from gtts import gTTS  # type: ignore
except Exception:  # Fallback if optional dependency isn't installed in the editor env
    gTTS = None  # type: ignore
import tempfile

def text_to_speech(text):
    if gTTS is None:
        raise RuntimeError("gTTS is not installed. Please add 'gtts' to requirements and install dependencies.")
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    temp_file.close()
    return temp_file.name
