import reactivex as rx
import reactivex.operators as ops
from reactivex.scheduler import ThreadPoolScheduler
import speech_recognition as sr
#from wasapi_helpers import *
from elevenlabs import generate, play
from time import time
import openai
import os
import json
from utils import *
import logging as log


log.basicConfig(level=log.INFO)

#   Hack to swap the pyauio library inside spechrecognition 
# to handle WAPI loopback devices
# https://github.com/s0d3s/PyAudioWPatch
# def get_patched_pyaudio(self):
#     """
#     Imports the pyaudio module and checks its version. Throws exceptions if pyaudio can't be found or a wrong version is installed
#     """
#     try:
#         import pyaudiowpatch as pyaudio
#     except ImportError:
#         raise AttributeError("Could not find PyAudio; check installation")
#     from distutils.version import LooseVersion
#     if LooseVersion(pyaudio.__version__) < LooseVersion("0.2.11"):
#         raise AttributeError("PyAudio 0.2.11 or later is required (found version {})".format(pyaudio.__version__))
#     return pyaudio
    
#sr.Microphone.get_pyaudio = get_patched_pyaudio
#sys_def_loopback_dev = WASAPIHelpers.get_default_wasapi_device(pyaudio.PyAudio())

WHISPER_MODEL = 'base'
r = sr.Recognizer()

# Just to load the model
log.info('Loading model...')
r.recognize_whisper(sr.AudioData(b'\0', 16000, 2), language="english", model=WHISPER_MODEL)
log.info('...done!')



# Init the gpt
openai.api_key = os.getenv("OPENAI_API_KEY")
setup_prompt = ''
with open("src/setup_prompt.txt") as f:
    setup_prompt = f.read()

log.info(f'setup prompt is: {setup_prompt}')


def get_speech_sound():
    #with sr.Microphone(device_index=sys_def_loopback_dev['index']) as source:
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source)
            log.info('Im listening')
            audio = r.listen(source)
            yield audio


def transcribe_speech_sound(audio):
    t = time()
    text = r.recognize_whisper(audio, language="english", model=WHISPER_MODEL)
    log.info(f'[{time() - t}s]: {text}')
    
    return {'transcription': text}


def ask_gpt(request):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
             "content": f"{setup_prompt}\n\nThe request is: {request}"}
        ]
    )
    
    #log.info(completion)
    
    return completion.choices[0].message.content

def process_command(gpt_response):
    log.info(gpt_response)
    
    try:
        object = json.loads(gpt_response)
    except Exception as e:
        log.warning(f"Can not parse GPT response: {gpt_response}, exception {e.with_traceback()}")
        return "Error happened"
        
    if 'payload' in object.keys():
        result = exec_command(object['payload'])
        result['answer'] = object['answer']
    # For test purposes I assusme that it always requires interpreteation
    return json.dumps(result)
        
    
def gpt_result_interpretation(command_result):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", 
             "content": f'Fullfill the gaps in "answer" field of this message {command_result}'}
        ]
    )
    
    return completion.choices[0].message.content


def elevenlabs_synthesis(speech):
    log.info(speech)
    
    audio = generate(
        text=speech,
        voice="Bella",
        model="eleven_monolingual_v1"
    )
    
    play(audio)
    
    return speech


if __name__ == '__main__':    
    source = rx.from_iterable(get_speech_sound())
    sched = ThreadPoolScheduler(16)
    
    source.pipe(
        ops.observe_on(sched),
        ops.map(transcribe_speech_sound),
        ops.observe_on(sched),
        ops.map(ask_gpt),
        ops.observe_on(sched),
        ops.map(process_command),
        ops.observe_on(sched),
        ops.map(gpt_result_interpretation),
        ops.observe_on(sched),
        ops.map(elevenlabs_synthesis),
    ).run()
    
    sched.executor.shutdown()