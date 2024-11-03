import os
import io
import threading
import requests
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
from libcam_cv import SimpleMoodDetector
from speech_to_text import SpeechToText
from text_to_response import TextToResponse
from response_to_voice import ResponseToVoice
from prompt_engineering import generate_music_details
from song_generator import generate_song_request, poll_song_status
from config import OPENAI_API_KEY, UDIO_KEY

# Load environment variables
load_dotenv()


def play_song(audio_url):
    """Play the generated song from the URL."""
    print("Playing generated song...")
    try:
        # Download the audio data into memory
        audio_data = requests.get(audio_url)
        audio_data.raise_for_status()  # Raise an error for bad responses

        # Load the audio data into an AudioSegment
        audio_segment = AudioSegment.from_file(
            io.BytesIO(audio_data.content), format="mp3"
        )

        # Play the audio
        play(audio_segment)
    except Exception as e:
        print(f"An error occurred while playing the song: {str(e)}")


def generate_song(user_text, detected_mood, audio_url_container):
    """Generate the song and return the audio URL."""
    # Generate music details based on user text and detected mood
    user_context = f"The user looks like they are feeling {detected_mood} by their face. {user_text}"
    generated_prompt, singer_name, music_genre = generate_music_details(
        user_context, OPENAI_API_KEY
    )
    if not all([generated_prompt, singer_name, music_genre]):
        print("Failed to generate music details.")
        audio_url_container.append(None)  # Append None for consistency
        return
    else:
        print("Generated Prompt: ", generated_prompt)
        print("Singer Name:", singer_name)
        print("Music Genre:", music_genre)

    # Prepare the song description prompt
    gpt_description_prompt = (
        f"The song should feature the singing voice closest to {singer_name} "
        f"in the style of {music_genre}. {generated_prompt}. "
        "Limit the song generated to be as short as possible."
    )

    # Start song generation
    work_id = generate_song_request(UDIO_KEY, generated_prompt, gpt_description_prompt)

    if work_id:
        print("Generating song...")
        while True:
            audio_url = poll_song_status(UDIO_KEY, work_id)
            if audio_url:
                print(f"Generated Song URL: {audio_url}")
                audio_url_container.append(audio_url)  # Store the URL in the container
                break  # Exit loop when the URL is obtained
            else:
                print("Waiting for song generation...")
            pygame.time.delay(500)  # Wait for a bit before checking again
    else:
        print("Failed to initiate song generation.")
        audio_url_container.append(None)  # Append None if failed


def main():
    """Main function to run the pipeline."""
    # Initialize components
    stt = SpeechToText()
    ttr = TextToResponse()
    rtv = ResponseToVoice()
    mood_detector = SimpleMoodDetector()

    print("Starting the speech-to-song pipeline system...")
    print("Detecting mood and listening for your message...")

    try:
        # Detect mood
        detected_mood = mood_detector.get_mood()
        if not detected_mood:
            print("Could not detect mood. Defaulting to 'neutral'.")
            detected_mood = "neutral"  # Default mood if detection fails

        # 1. Speech to Text
        user_text = stt.get_user_text()
        if user_text is None:
            print("Could not understand audio. Please try again later.")
            return
        print(f"You said: {user_text}")

        # 2. Prepare a container for the song URL
        audio_url_container = []  # List to hold the audio URL

        # 3. Start song generation in a separate thread with mood input
        song_thread = threading.Thread(
            target=generate_song, args=(user_text, detected_mood, audio_url_container)
        )
        song_thread.start()

        # 4. Get GPT response while song generation is happening
        gpt_response = ttr.get_gpt_response(user_text)
        if gpt_response is None:
            print("Could not generate GPT response.")
            return
        print(f"GPT Response: {gpt_response}")

        # 5. Read text response
        voice_success = rtv.read_text(gpt_response)
        if not voice_success:
            print("Failed to convert response to speech.")
            return

        # 6. Wait for the song thread to finish
        song_thread.join()  # Wait for song generation to complete

        # 7. Retrieve the audio URL after song generation completes
        audio_url = audio_url_container[0] if audio_url_container else None

        if audio_url:
            # Play the generated song from the URL
            play_song(audio_url)
        else:
            print("No song URL was generated.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("System ended")


if __name__ == "__main__":
    main()
