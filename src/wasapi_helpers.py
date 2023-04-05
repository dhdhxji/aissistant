import pyaudiowpatch as pyaudio


class ARException(Exception):
    """Base class for AudioRecorder`s exceptions"""

 
class WASAPINotFound(ARException):
    ...


class InvalidDevice(ARException):
    ...

class WASAPIHelpers:
    @staticmethod
    def get_default_wasapi_device(p_audio: pyaudio.PyAudio):        
        
        try: # Get default WASAPI info
            wasapi_info = p_audio.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            raise WASAPINotFound("Looks like WASAPI is not available on the system")
            
        # Get default WASAPI speakers
        sys_default_speakers = p_audio.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not sys_default_speakers["isLoopbackDevice"]:
            for loopback in p_audio.get_loopback_device_info_generator():
                if sys_default_speakers["name"] in loopback["name"]:
                    return loopback
                    break
            else:
                raise InvalidDevice("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices")