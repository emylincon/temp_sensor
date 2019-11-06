from drawnow import *
import matplotlib.pyplot as plt
import random as r
import time

x = [0]
y = [0]


def plot():
    plt.plot(x,y, 'm--*')


while True:
    x.append(r.randrange(20))
    y.append(r.randrange(20))
    drawnow(plot)
    time.sleep(2)


