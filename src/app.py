import reactivex as rx
import reactivex.operators as ops
from reactivex.scheduler import ThreadPoolScheduler
import speech_recognition as sr
from wasapi_helpers import *
import pyaudiowpatch as pyaudio


#   Hack to swap the pyauio library inside spechrecognition 
# to handle WAPI loopback devices
# https://github.com/s0d3s/PyAudioWPatch
def get_patched_pyaudio(self):
    """
    Imports the pyaudio module and checks its version. Throws exceptions if pyaudio can't be found or a wrong version is installed
    """
    try:
        import pyaudiowpatch as pyaudio
    except ImportError:
        raise AttributeError("Could not find PyAudio; check installation")
    from distutils.version import LooseVersion
    if LooseVersion(pyaudio.__version__) < LooseVersion("0.2.11"):
        raise AttributeError("PyAudio 0.2.11 or later is required (found version {})".format(pyaudio.__version__))
    return pyaudio
    
sr.Microphone.get_pyaudio = get_patched_pyaudio
sys_def_loopback_dev = WASAPIHelpers.get_default_wasapi_device(pyaudio.PyAudio())


def get_speech_sound():
    r = sr.Recognizer()
    with sr.Microphone(device_index=sys_def_loopback_dev['index']) as source:
        while True:
            print('Im listening')
            audio = r.listen(source)
            yield audio


def transcribe_speech_sound(audio):
    r = sr.Recognizer()
    print('start recognising')
    text = r.recognize_whisper(audio, language="english", model='base')
    print(f'Recognized text {text}')
    return text


def ask_gpt(request):
    return 'GPT says: "I am not implemented, but will be soon!"'


def elevenlabs_synthesis(speech):
    return 'Elevenlabs says "I am not implemented!"'


def show_transcription(transcription):
    print(transcription)


if __name__ == '__main__':    
    source = rx.from_iterable(get_speech_sound())
    sched = ThreadPoolScheduler(16)
    
    source.pipe(
        ops.observe_on(sched),
        ops.map(transcribe_speech_sound),
        ops.observe_on(sched),
        ops.map(ask_gpt),
        ops.observe_on(sched),
        ops.map(elevenlabs_synthesis),
        ops.observe_on(sched),
        ops.map(show_transcription)
    ).run()
    
    sched.executor.shutdown()