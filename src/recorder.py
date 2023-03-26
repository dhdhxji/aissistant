import reactivex as rx
import pyaudio

class Recorder(rx.Subject):
    def __init__(self,
                 chunk_size_ms=200,
                 format=pyaudio.paInt16, 
                 channels=1,
                 rate=44100):
        super().__init__()
        
        self.chunk_size_ms = chunk_size_ms
        self.format = format
        self.channels = channels
        self.rate = rate
        
        self.audio = None
        self.stream = None
        
        
    def _start(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      rate=self.rate,
                                      channels=self.channels,
                                      input=True,
                                      frames_per_buffer=int(self.rate * self.chunk_size_ms / 1000),
                                      stream_callback=self._on_audio_chunk)  

    def _terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        
        self.on_completed()

    def _on_audio_chunk(self, buffer, frameCount, timeInfo, statusFlags):
        _ = frameCount
        _ = statusFlags
        
        self.on_next((buffer, timeInfo))
        return None, 0