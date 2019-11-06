# This is a property of London South Bank University developed by EMEKA UGWUANYI

import os
import glob
import time
from drawnow import *
from matplotlib import pyplot as plt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

cel_x = []
fer_x = []
style = ['g--^', 'r:o', 'b-.s', 'm--*', 'k-.>', 'c-.s']

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        cel_x.append(temp_c)
        fer_x.append(temp_f)


def plot_normal_graph():
    x = list(range(len(calculate_mov_avg(cel_x))))
    ax1.grid(True)
    # ax1.plot(x, cel_x, linewidth=2, label='Temp C')
    ax1.plot(x, calculate_mov_avg(cel_x), 'm--*', linewidth=2, label='Moving Temp')

    ax1.set_ylabel('Temperature')
    ax1.set_xlabel('Time (seconds)')
    #ax1.fill_between(x, calculate_mov_avg(cel_x), 0, alpha=0.5, color='m')
    ax1.legend()
    ax1.set_title('Temperature graph')
    plt.subplot(ax1)

    # plt.show()


def calculate_mov_avg(a1):
    ma1 = []  # moving average list
    avg1 = 0  # moving average point-wise
    count = 0
    for i in range(len(a1)):
        count += 1
        avg1 = ((count-1)*avg1+a1[i])/count
        ma1.append(avg1)  # cumulative average formula
        # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return ma1


def plot_moving_graph():
    x = list(range(len(fer_x)))
    ax2.grid(True)
    ax2.plot(x, fer_x, 'g--^', linewidth=2, label='Temp in F')
    #ax2.fill_between(x, fer_x, 0, alpha=0.5, color='g')
    #ax2.plot(calculate_mov_avg(fer_x), linewidth=5, label='Moving Temp')
    ax2.set_title('Temperature in Fahrenheit')
    ax2.set_ylabel('Temperature')
    ax2.set_xlabel('Time (seconds)')
    ax2.legend()
    plt.subplot(ax2)


def plot_graphs():
    plot_normal_graph()
    plot_moving_graph()
    plt.show()


while True:
    try:
        read_temp()
        drawnow(plot_graphs)
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgramme Terminated\n")
        break
