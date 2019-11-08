"""
This is a property of London South Bank University developed by EMEKA UGWUANYI
This plots a line graph of the temperature in celsius and in Fahrenheit. it also plots the memory and cpu utilization
of the system in the same subplot.
"""


import os
import glob
import time
from drawnow import *
from matplotlib import pyplot as plt
import psutil
from pyfiglet import Figlet
from termcolor import colored, cprint
import sys

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

algo = psutil.Process()
cel_x = []
fer_x = []
memory = []
_cpu = []
prev_t = 0            # variable for cpu util
style = ['g--^', 'r:o', 'b-.s', 'm--*', 'k-.>', 'c-.s']

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.25)


os.system('clear')
print('>> starting...')
delay_print("<========================================================")

os.system('clear')
custom_fig = Figlet(font='graffiti')
cprint(custom_fig.renderText('welcome to LSBU'), 'yellow')
#print(custom_fig.renderText('Welcome To LSBU'))
cprint("                    /********************************\\", 'yellow')
cprint("                    *                                *", 'yellow')
cprint("                    *      Use CTR + C to exit       *", 'red')
cprint("                    *                                *", 'yellow')
cprint("                    \********************************/\n", 'yellow')
time.sleep(1.9)


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


def plot_normal_graph():
    x = list(range(len(calculate_mov_avg(cel_x))))
    ax1.grid(True)
    #ax1.plot(cel_x, linewidth=2, label='Temp C')
    ax1.plot(x, calculate_mov_avg(cel_x), 'm--*', linewidth=2, label='Temp in C')

    ax1.set_ylabel('Temperature')
    ax1.set_xlabel('Time (seconds)')
    #ax1.fill_between(x, calculate_mov_avg(cel_x), 0, alpha=0.5, color='m')
    ax1.legend()
    ax1.set_title('Temperature in Celsius')
    plt.subplot(ax1)

    # plt.show()


def plot_moving_graph():
    x = list(range(len(fer_x)))
    ax2.grid(True)
    # ax2.plot(fer_x, 'g--^', linewidth=2, label='Temp in F')
    #ax2.fill_between(x, fer_x, 0, alpha=0.5, color='g')
    ax2.plot(calculate_mov_avg(fer_x), 'g-->', linewidth=2, label='Temp in F')

    # ax2.set_ylabel('Temperature')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_title('Temperature in Fahrenheit')
    ax2.legend()
    plt.subplot(ax2)
    

def plot_memory():
    global memory

    memory.append(round(algo.memory_percent(), 4))

    ax3.grid(True)
    ax3.plot(list(range(len(calculate_mov_avg(memory)))), calculate_mov_avg(memory), linewidth=2, label='Memory', color='m')
    # ax3.set_title('Moving Memory Utilization')
    ax3.set_ylabel('Moving Memory')
    ax3.set_xlabel('Time (seconds)')
    #cleaax3.set_title('Memory Utilization')
    ax3.fill_between(list(range(len(calculate_mov_avg(memory)))), calculate_mov_avg(memory), 0, alpha=0.3, color='m')
    ax3.legend()
    plt.subplot(ax3)


def plot_cpu():
    global prev_t

    # get cpu
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    _cpu.append(round(delta, 4))

    # plot graph
    ax4.grid(True)
    ax4.plot(list(range(len(calculate_mov_avg(_cpu)))), calculate_mov_avg(_cpu), linewidth=2, label='CPU')
    # ax4.set_title('Moving CPU Utilization')
    # ax4.set_ylabel('Moving CPU')
    ax4.set_xlabel('Time (seconds)')
    #ax3.set_title('CPU Utilization')
    ax4.fill_between(list(range(len(calculate_mov_avg(_cpu)))), calculate_mov_avg(_cpu), 0, alpha=0.2)
    ax4.legend()
    plt.subplot(ax4)


def plot_graphs():
    plot_normal_graph()
    plot_moving_graph()
    plot_memory()
    plot_cpu()
    plt.subplots_adjust(wspace=0.3, hspace=0.2)


while True:
    try:
        read_temp()
        drawnow(plot_graphs)
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgramme Terminated\n")
        break
