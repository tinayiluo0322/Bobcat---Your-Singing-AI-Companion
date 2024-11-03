# main.py

from speech_to_text import SpeechToText
from text_to_response import TextToResponse
from response_to_voice import ResponseToVoice
from prompt_engineering import generate_music_details
from song_generator import generate_song_request, poll_song_status
from config import OPENAI_API_KEY, UDIO_KEY
import os
import pygame
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Main function to run the pipeline in exact order:
    1. Speech to Text
    2. Generate music details
    3. Get GPT response
    4. Speak GPT response
    5. Generate and play song
    """
    # Initialize components
    stt = SpeechToText()
    ttr = TextToResponse()
    rtv = ResponseToVoice()

    print("Starting the speech-to-song pipeline system...")
    print("Please speak your message...")

    try:
        # 1. Speech to Text
        user_text = stt.get_user_text()
        if user_text is None:
            print("Could not understand audio. Please try again later.")
            return
        print(f"You said: {user_text}")

        # 2. Generate music details
        generated_prompt, singer_name, music_genre = generate_music_details(
            user_text, OPENAI_API_KEY
        )
        if not all([generated_prompt, singer_name, music_genre]):
            print("Failed to generate music details.")
            return
        print(f"Generated Prompt: {generated_prompt}")
        print(f"Singer Name: {singer_name}")
        print(f"Music genre: {music_genre}")

        # 3. Get GPT response
        gpt_response = ttr.get_gpt_response(user_text)
        if gpt_response is None:
            print("Could not generate GPT response.")
            return
        print(f"GPT Response: {gpt_response}")

        # 4. Speak GPT response
        voice_success = rtv.read_text(gpt_response)
        if not voice_success:
            print("Failed to convert response to speech.")
            return

        # 5. Generate and play song
        gpt_description_prompt = (
            f"The song should feature the singing voice closest to {singer_name} "
            f"in the style of {music_genre}. {generated_prompt}. "
            "Limit the song generated to be as shortest in length as possible."
        )

        work_id = generate_song_request(
            UDIO_KEY, generated_prompt, gpt_description_prompt
        )

        if work_id:
            print("Generating song...")
            audio_url = poll_song_status(UDIO_KEY, work_id)
            if audio_url:
                print(f"Generated Song URL: {audio_url}")
            else:
                print("Failed to generate song.")
        else:
            print("Failed to initiate song generation.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("System ended")


if __name__ == "__main__":
    main()
