import os
import tempfile
import pygame
import time
from dotenv import load_dotenv
from openai import OpenAI


class ResponseToVoice:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

            # Create a temporary file to avoid access issues
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                self.output_file = tmp_file.name
                response.stream_to_file(self.output_file)

            print("Playing audio...")
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # Delay to ensure the file is no longer in use
            time.sleep(1)  # Adjust as needed

            # No file deletion logic since we want to keep the file
            print(f"Audio file is kept at: {self.output_file}")

            return True
        except Exception as e:
            print(f"Error in text-to-speech conversion: {str(e)}")
            return False
