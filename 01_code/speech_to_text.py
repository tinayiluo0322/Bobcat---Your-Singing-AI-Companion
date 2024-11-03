import speech_recognition as sr
import os
import time


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_user_text(self):
        """Get speech input from user and convert to text."""
        try:
            with sr.Microphone() as source:
                print("Please speak now...")
                self.recognizer.adjust_for_ambient_noise(source)

                # Set a limit for how long to listen in total
                total_time_limit = 20  # seconds
                chunks = []  # List to hold chunks of speech
                start_time = time.time()

                while time.time() - start_time < total_time_limit:
                    try:
                        # Listen for a chunk
                        audio_data = self.recognizer.listen(source, timeout=5)
                        chunks.append(audio_data)  # Store the audio chunk
                        print("Chunk recorded. Speak more or stop.")
                    except sr.WaitTimeoutError:
                        # Timeout waiting for user input
                        print("No input detected. Please continue speaking or stop.")
                        break
                    except Exception as e:
                        print(f"An error occurred while listening: {e}")
                        break

                if chunks:
                    # Create a combined audio object from the chunks
                    combined_audio_data = b"".join(
                        chunk.get_raw_data() for chunk in chunks
                    )
                    combined_audio = sr.AudioData(
                        combined_audio_data,
                        sample_rate=chunks[0].sample_rate,
                        sample_width=chunks[0].sample_width,
                    )

                    # Recognize speech in the combined audio
                    text = self.recognizer.recognize_google(combined_audio)
                    return text
                else:
                    print("No audio chunks were recorded.")
                    return None
        except AssertionError as e:
            print(f"Error adjusting ambient noise: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
