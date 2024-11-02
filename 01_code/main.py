# main.py

from prompt_engineering import generate_music_details
from song_generator import generate_song_request, poll_song_status
from config import OPENAI_API_KEY, UDIO_KEY
import openai

# Set up the API key for OpenAI
openai.api_key = OPENAI_API_KEY
udio_api_key = UDIO_KEY

def main():
    # Set your API token for both OpenAI and song generation services
    openai_api_token = openai.api_key
    udio_token = udio_api_key
    # Define context for generating music details
    context = (
        "Today was just one of those days where everything boiled over. I woke up already feeling off, "
        "and then it hit me—my phone buzzed with messages that made my heart sink. My boyfriend decided to "
        "break up with me, out of nowhere, and the worst part? I found out he’d been seeing someone else behind "
        "my back. The betrayal stung more than I thought it could, so I decided to play some Olivia Rodrigo. I felt "
        "this mix of anger and hurt building up inside, and it was almost impossible to focus on anything else. "
        "I tried talking to a friend, but even that didn’t help much. Every time I replayed it in my mind, the "
        "frustration bubbled up again. I felt like I couldn’t sit still; I wanted to scream, to confront him, to do "
        "anything to get rid of that gnawing feeling. It was just a day where everything felt wrong, and I was left "
        "wondering how someone I trusted could turn out to be so different from what I believed."
    )

    # Generate the prompt, singer name, and music genre based on the context
    generated_prompt, singer_name, music_genre = generate_music_details(context, openai_api_token)
    
    # Display generated details
    if generated_prompt and singer_name and music_genre:
        print("Generated Prompt:", generated_prompt)
        print("Singer Name:", singer_name)
        print("Music Genre:", music_genre)
        
        # Combine details for song generation
        gpt_description_prompt = f"The song should feature {singer_name} in the style of {music_genre}. {generated_prompt}"

        # Step 1: Start the song generation
        workId = generate_song_request(udio_token, generated_prompt, gpt_description_prompt)
        
        if workId:
            # Step 2: Poll the status until the song is ready
            audio_url = poll_song_status(udio_token, workId)
            if audio_url:
                print("Generated Song URL:", audio_url)
    else:
        print("Failed to generate music details.")

if __name__ == "__main__":
    main()
