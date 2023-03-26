from recorder import Recorder
from time import sleep

r = Recorder()
r._start()

sleep(5)

r._terminate()