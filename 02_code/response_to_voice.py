import os
from pathlib import Path
import pygame
import time
from dotenv import load_dotenv
from openai import OpenAI


class ResponseToVoice:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.output_file = "speech_output.mp3"
        pygame.mixer.init()

    def read_text(self, text):
        """Convert text to speech using OpenAI's Nova voice"""
        try:
            print("\nConverting text to speech using Nova voice...")

            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="nova",
                input=text,
            )

            if os.path.exists(self.output_file):
                os.remove(self.output_file)

            response.stream_to_file(self.output_file)

            print("Playing audio...")
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            if os.path.exists(self.output_file):
                os.remove(self.output_file)

            return True
        except Exception as e:
            print(f"Error in text-to-speech conversion: {str(e)}")
            return False
