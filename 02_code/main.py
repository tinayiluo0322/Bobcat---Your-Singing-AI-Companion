from speech_to_text import SpeechToText
from text_to_response import TextToResponse
from response_to_voice import ResponseToVoice


def main():
    """Main function to coordinate the speech processing chain"""
    # Initialize components
    stt = SpeechToText()
    ttr = TextToResponse()
    rtv = ResponseToVoice()

    print("Starting the conversation system...")
    print("Speak something (or say 'quit' to exit)")

    try:
        while True:
            # Step 1: Speech to Text
            user_text = stt.get_user_text()
            if user_text is None:
                print("Could not understand audio. Please try again.")
                continue

            print(f"You said: {user_text}")

            # Check for exit command
            if user_text.lower() in ["quit", "exit", "stop", "goodbye"]:
                print("Ending conversation...")
                break

            # Step 2: Text to Response
            response = ttr.get_gpt_response(user_text)
            if response is None:
                print("Could not generate response. Please try again.")
                continue

            print("AI Response:", response)

            # Step 3: Response to Voice
            success = rtv.read_text(response)
            if not success:
                print("Failed to convert response to speech. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Conversation system ended")


if __name__ == "__main__":
    main()
