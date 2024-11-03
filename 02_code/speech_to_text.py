import speech_recognition as sr
import os


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_user_text(self):
        """Get speech input from user and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Please speak now...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio_data = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        except AssertionError as e:
            print(f"Error adjusting ambient noise: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
