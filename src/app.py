from recorder import Recorder
from player import Player
from time import sleep

r = Recorder()
r.subscribe(Player())
r._start()
sleep(5)
r._terminate()