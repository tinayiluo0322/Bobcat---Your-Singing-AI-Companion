# prompt_engineering.py

import openai
import json
import requests

# Set up your OpenAI API key
openai.api_key = "your_openai_api_key"

def generate_music_details(context, open_ai_key):

    openai.api_key = open_ai_key

    # Define the prompt to send to the API
    prompt = (
        "Analyze the following context to generate a music prompt 2-3 sentences in length that reflects the emotional experience described. "
        "Extract the singer's name if mentioned; "
        "if not mentioned, use a popular singer's name that fits the style of the music and sentiment of the song. "
        "Determine a suitable music genre or style based on the emotions conveyed.\n\n"
        f"Context: {context}\n\n"
        "Output Format:\n"
        "Prompt: {Insert Prompt here}\n"
        "Singer_Name: {Insert Singer_Name here} (if not mentioned, use a popular singer's name that is suitable)\n"
        "Music_genre: {Insert Music_genre here}"
    )

    # Define the API endpoint
    url = "https://api.openai.com/v1/chat/completions"

    # Define the data for the POST request
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        response_content = response_data['choices'][0]['message']['content']
        
        # Extract the values from the response content
        prompt_line = next(line for line in response_content.split('\n') if line.startswith('Prompt:')).replace('Prompt: ', '').strip()
        singer_name_line = next(line for line in response_content.split('\n') if line.startswith('Singer_Name:')).replace('Singer_Name: ', '').strip()
        music_genre_line = next(line for line in response_content.split('\n') if line.startswith('Music_genre:')).replace('Music_genre: ', '').strip()
        
        # Return the extracted values
        return prompt_line, singer_name_line, music_genre_line
    else:
        print("Error:", response.status_code, response.text)
        return None, None, None
