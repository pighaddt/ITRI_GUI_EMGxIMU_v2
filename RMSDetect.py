import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def rms_function(data, window):
    rms = np.array(data)

    halfMask = round(window)
    for index in range(len(data)):
        # lower upper setting
        if index < halfMask:
            lower = 1
        else:
            lower = index - halfMask

        if index > len(data) - halfMask:
            upper = len(data)
        else:
            upper = index + halfMask

        current = data[lower:upper]
        power2 = current * current
        mean = power2.mean()
        sqrt = np.sqrt(mean)
        rms[index] = sqrt

    return rms

def startPoint(rms, threshold_start, threshold_stop):
    startPointArray = []
    isStart = False

    for i in range(len(rms)):
        if isStart == False and rms[i] > threshold_start:
            startIndex = i
            isStart = True
        elif isStart == True and rms[i] < threshold_stop:
            stopIndex = i
            isStart = False
            startPointArray.append(startIndex)
            startPointArray.append(stopIndex)

    return startPointArray