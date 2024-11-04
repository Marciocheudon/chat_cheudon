# gui/text_to_speech.py

import pyttsx3
import threading

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 205)  # Velocidade da fala
        self.engine.setProperty('volume', 1.0)  # Volume
        voices = self.engine.getProperty('voices')
        self.voices_pt = [voice for voice in voices if 'pt_BR' in voice.id or 'Portuguese' in voice.name]
        if self.voices_pt:
            self.engine.setProperty('voice', self.voices_pt[0].id)
        else:
            print("Voz em Português (Brasil) não encontrada. Usando a voz padrão.")

    def speak(self, text):
        # Executa o TTS em uma thread separada para não bloquear a GUI
        threading.Thread(target=self._speak_thread, args=(text,)).start()

    def _speak_thread(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Erro ao falar o texto: {e}")
