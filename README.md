# Duke AI Hackathon 2024

# Bobcat: Your Singing AI Companion

Welcome to Bobcat, your personal, artistic, AI-powered friend who listens, responds, and creates music tailored just for you. Bobcat goes beyond traditional gadgets to become a genuine companion, blending empathy and creativity into an interactive experience.

## Project Overview

Bobcat is designed as a portable, interactive AI that fills the gap between technology and human connection. Built with Raspberry Pi and housed in a 3D-printed shell, Bobcat is more than just a chatbot; it’s a friend who understands, sings, and responds to your emotions through personalized songs and conversations.

## Features

- **Real-Time Sentiment Analysis**: Bobcat reads both facial expressions and voice input to understand your mood.
- **Voice Transcription and Sentiment Interpretation**: Powered by Speech Recognition, Bobcat converts your voice to text and gauges emotional tone.
- **Empathetic Conversation**: OpenAI's GPT-3.5 Turbo provides natural, comforting responses.
- **Song and Lyrics Generation**: Using UDIO, Bobcat composes and performs personalized songs that reflect your current mood.
- **Portable and Friendly Design**: Housed in a custom 3D-printed capsule, Bobcat has a cute, approachable look, making it feel like a friendly companion rather than a device.

## Hardware

Bobcat runs on:
- **Raspberry Pi 4B** for processing.
- **Arducam IMX708** for real-time image capture and mood analysis.
- **Audio Core HAT WM8060** for clear, warm sound output.
- **Lithium Battery Module** to keep Bobcat powered and portable.
  
The form factor includes:
- Integrated microphone
- Speaker
- Camera for facial recognition and expression analysis

## Software Stack

Bobcat utilizes:
- **DeepFace** for real-time facial recognition.
- **OpenAI GPT-3.5 Turbo** for generating human-like chat responses.
- **Text-to-Speech (TTS-1-HD)** for expressive vocal output.
- **UDIO** for dynamic song generation with mood-reflective lyrics and melodies.

## Overview Project Pipeline
![CI_CD pipeline llm_RAG (1)](https://github.com/user-attachments/assets/28ea490d-214c-4824-9dc9-b766fe02bc87)

## Use Cases

Bobcat is ideal for:
- **Children**: A playful friend who can provide companionship.
- **Adults**: An empathetic companion offering stress relief through art and music.
- **Seniors**: A companion that provides comfort and engagement.

In future updates, Bobcat will expand to cloud functionalities (AWS Lex and Polly), enabling app-integrated interactions across platforms like Slack and Discord.

## Future Directions

- **Scalable Cloud Integration**: Making Bobcat available on digital platforms for on-the-go companionship.
- **Social Sharing**: Enabling users to share their personalized songs and moments on social media.
- **Enhanced Interactivity**: Adding more personalization and depth to Bobcat’s responses and interactions.

## Development Journey

Bobcat was created within a 48-hour hackathon, involving rapid integration of advanced software and hardware. Achieving real-time operations within these constraints reflects the teamwork and dedication behind Bobcat’s innovation.

## License

This project is licensed under the [MIT License](LICENSE.md).

## Contributors

- Afraa Noureen
- Charles Xie
- Tina Yi
- Bob Zhang

## Acknowledgments

We are deeply grateful to Duke University for organizing such a competitive and wonderfully joyful hackathon. We also extend our heartfelt thanks to the sponsors who made this event possible.

Thank you for exploring Bobcat! We hope it brings you joy, comfort, and inspiration as your singing AI companion. Welcome to a new era of AI companionship!

