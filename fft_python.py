# importa o modulo para tratar o cliente mqtt
import paho.mqtt.client as mqttClient 
import numpy
from matplotlib import pyplot as plt
from scipy import fft, signal
import csv
import math

with open('current_signal_0.csv') as csv_file:

    # Abre arquivo CSV
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    data=[]
    time=[]
    correction_factor = 1.4

    # Dados osciloscopio
    csv_osc_file = open('dados_osc.csv')
    csv_reader_osc = csv.reader(csv_osc_file, delimiter=',')
    line_count_osc = 0
    data_osc_0=[]
    time_osc=[]
    for row in csv_reader_osc:
        time_osc.append(float(row[0]))
        data_osc_0.append(float(row[1]))
        line_count_osc +=1

    i = 0
    data_osc=[]
    while i < (line_count_osc-170):
        data_osc.append(float(data_osc_0[i+170]))
        i+=1
    total_time = 0.05
    csv_osc_file.close()
    time_step = 0.05/len(data_osc_0)
    Fs_osc = 1/time_step
    data_osc = data_osc - numpy.mean(data_osc)
    
    count = 0
    # Dados aquisição
    for row in csv_reader:
        data.append(row)
        count += 1
    i = 0
    rec_data = []
    data = numpy.array(data)
    while i < (count-150):
        rec_data.append(float(data[i+150]))
        i+=1

    recv_data = rec_data - numpy.mean(rec_data)
    recv_data *= correction_factor
    time_step = 1/9835
    Fs = 9835

    time_scale = Fs_osc/Fs
    
    # Plot sinal
    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    fig.suptitle('Sinal MIT')
    axs[0].plot(recv_data)
    axs[0].set_xlim([0,450])
    axs[0].set_title('Sinal Placa')
    axs[0].set_ylabel('Corrente [A]')
    axs[0].set_xlabel('Amostra [n]')
    axs[1].plot(data_osc)
    axs[1].set_xlim([0,int(450*time_scale)])
    axs[1].set_title('Sinal Osciloscópio')
    axs[1].set_ylabel('Corrente [A]')
    axs[1].set_xlabel('Amostra [n]')
    plt.show()
    # FFT
    plt.magnitude_spectrum(recv_data, Fs, sides='onesided', linewidth=0.5, scale='dB', label="Placa Aquisição")
    plt.xlim([0,1000])
    plt.title('FFT', fontsize=16)
    plt.ylabel('Amplitude', fontsize=16)
    plt.xlabel('Frequência [Hz]', fontsize=16)
    plt.magnitude_spectrum(data_osc, 50000, sides='onesided', scale='dB', linewidth=0.5, label="Osciloscópio")
    plt.legend(['Sistema Proposto', 'Osciloscópio'])
    # axs[1].set_xlim([0,500])
    plt.show()
    
