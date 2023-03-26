import reactivex
import pyaudio

class Player(reactivex.Observer):
    def __init__(self, 
                 format=pyaudio.paInt16, 
                 channels=1,
                 rate=44100,
                 on_error=None) -> None:
        super().__init__(self.play_chunk, on_error, self.deinit)
        
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=format,
                                   channels=channels,
                                   rate=rate,
                                   output=True)
        
        
    def play_chunk(self, stream) -> None:
        self.stream.write(stream[0].tobytes())
    
    
    def deinit(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()