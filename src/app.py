from recorder import Recorder
from time import sleep

r = Recorder()
r.subscribe(lambda x: print(x[1]))
r._start()
sleep(5)
r._terminate()