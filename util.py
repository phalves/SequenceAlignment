# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np

import subprocess
import os


def memory_usage():
    # return the memory usage in MB
    out = subprocess.Popen(
        ['ps', 'v', '-p', str(os.getpid())],
        stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return mem


def plot(data):
    plt.figure(1)
    plt.plot(data[1])
    plt.ylabel(u"""Tempo (minutos)""")
    plt.xlabel(u"""Iterações""")

    # Iterations X Memory
    plt.figure(2)
    plt.plot(data[2])
    plt.ylabel(u"Consumo médio de Memória (MB)")
    plt.xlabel(u"Iterações")

    mean_time = []
    mean_menm = []
    chain_size = []

    for j in range(len(data[0])/10):
        i = j*10
        chain_size.append(data[0][i])
        mean_time.append(np.median(data[1][i:(i+10)]))
        mean_menm.append(np.median(data[2][i:(i+10)]))

    plt.figure(3)
    # Size X Time
    plt.plot(mean_time, chain_size)
    plt.xlabel(u"Tempo médio (minutos)")
    plt.ylabel(u"Tamanho das cadeias")

    # Size i X Memory
    plt.figure(4)
    plt.plot(mean_menm, chain_size)
    plt.xlabel(u"Consumo médio de Memória (MB)")
    plt.ylabel(u"Tamanho das cadeias")

    plt.show()
