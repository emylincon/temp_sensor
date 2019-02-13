# This is a property of London South Bank University developed by EMEKA UGWUANYI

import os
import glob
import time
from matplotlib import pyplot as plt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

cel_x = []
fer_x = []


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
    fig1 = plt.figure('Temperature Readings in Celsius')

    fig1 = plt.clf()
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot(cel_x, linewidth=5, label='Temp C')
    fig1 = plt.plot(calculate_mov_avg(cel_x), linewidth=5, label='Moving Temp')
    fig1 = plt.title('Temperature graph')
    fig1 = plt.ylabel('Temperature')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)

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
    fig1 = plt.figure('Moving Average Temperature in Fahrenheit')

    fig1 = plt.clf()
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot(fer_x, linewidth=5, label='Temp in F')
    fig1 = plt.plot(calculate_mov_avg(fer_x), linewidth=5, label='Moving Temp')
    fig1 = plt.title('Moving Average Temperature graph')
    fig1 = plt.ylabel('Temperature')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)


def plot_graphs():
    read_temp()
    plot_normal_graph()
    plot_moving_graph()
    plt.show()


while True:
    plot_graphs()
    time.sleep(1)
