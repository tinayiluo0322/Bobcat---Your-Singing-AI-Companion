import openai
import os
from dotenv import load_dotenv


class TextToResponse:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_prompt_for_gpt(self, user_input):
        prompt = (
            f'User Input: "{user_input}"\n\n'
            "Respond as an empathetic and friendly conversational partner. Your response should be engaging, supportive, "
            "and continuous for approximately one minute, speaking as a comforting friend who listens, reassures, and "
            "validates the user's emotions or experience. Make sure to conclude the response with: "
            "'I have written a song for you, here it is.'"
        )
        return prompt

    def get_gpt_response(self, user_input):
        """Generate response from GPT based on user input"""
        try:
            prompt = self.generate_prompt_for_gpt(user_input)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an empathetic and friendly AI that responds thoughtfully to user inputs.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
