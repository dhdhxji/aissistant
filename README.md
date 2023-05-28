# About
The project is OpenAI GPT-powered home assistant for controlling the smart home components.

# Main flow
The command recognition - action - response flow can be described in the following diagram:

Microphone -> Speech detection -> Hello phrase detection -> Whisper -> GPT -> Taking an action -> ElevenLabs speech synthesis

# Thoughts
- Automatic reaction for events from smart devices with custom user-defined rules (like a temp raised to 22 -> close the shutters)
- Add devices, protocols, even GPT-generated implementations all over voice commands
- Improve pipeline to allow GPT check is request fulfilled, and invoke commands in some order to do what the user asks