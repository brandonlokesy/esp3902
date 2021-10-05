import threading
from legobrick import Lego
import random

lego = Lego()
def get_rand():
    return random.randint(0,100)

def foo():
    print('This is foo running')
    x,y = get_rand(), get_rand()
    lego.update('brightBlue', (x,y))
    print('Coords are x = {x}, y = {y}'.format(x = x, y = y))

def bar():
    print('This is bar running')
    print('The lego coords are {coords}'.format(coords = (lego.get_xy())))
    return

while True:
    t1 = threading.Thread(target = foo)
    t2 = threading.Thread(target = bar)

    t1.start()
    t2.start()

    t1.join()
    t2.join()