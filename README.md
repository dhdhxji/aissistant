# About
The project is OpenAI GPT-powered home assistant for controlling the smart home components.

# Main flow
The command recognition - action - response flow can be described in the following diagram:

Microphone -> Speech detection -> Hello phrase detection -> Whisper -> GPT -> Taking an action -> ElevenLabs speech synthesis