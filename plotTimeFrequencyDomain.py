import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft,ifft

def plotTimeFrequencyDomain(LRec):

    ## parameter setting
    LRec = np.array(LRec) #data input
    Fs = 2000  # Sampling frequency
    T = 1 / Fs  # Sampling period

    L = len(LRec)  # Length of signal
    t = np.arange(len(LRec)) * T  # Time vector
    x = np.linspace(0, len(LRec) - 1, len(LRec)) #橫軸長度 0~len(data)-1


    #FFT Transform (double side X、Y label)
    yy = fft(LRec)  # 快速傅立葉變換
    yf = abs(fft(LRec))  # 取絕對值 angle and amplitude

    yf1 = abs(fft(LRec) / len(x))  # 歸一化處理

    #FFT Transform (single side X)
    yf1 = yf1[range(int(len(x) / 2) + 1)] * 2  # 由於對稱性，只取一半區間
    fStop2 = np.arange(len(LRec) / 2) # x label half-range

    f2 = Fs * fStop2 / L # x label frequency setting

    ##FFT median frequency find
    sum = 0
    for i in range(1, 1000): #first 1000 data get sum
        sum = sum + yf1[i]

    halfSum = int(sum / 2) # PSD

    target = 0
    j = 1
    while target < halfSum:
        j = j + 1
        target = target + yf1[j] # j is the median frequency index

    plt.figure()
    plt.vlines(f2[j], 0, 10, colors="r", linestyles='solid') # median frequency line draw
    plt.plot(f2, yf1, 'b')
    plt.xlim([1, 1000]) # X lable range display
    plt.title('FFT of Mixed wave(normalization)', fontsize=9, color='r')
    plt.text(f2[j], 6, "median frequencyHz = " + str(f2[j]))

    plt.show()
    return f2[j]
