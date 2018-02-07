#!/usr/bin/python3
from math import atan
from math import sqrt
from math import pi
from numpy import random
from numpy import correlate
import numpy as np
import operator

i = 0


def main():
    speedofsound = 34300; #cm/s
    d = 3.5; #cm
    maxDelay = d/speedofsound

    fs = 27700
    timePeriod = 1/fs

    I = 8
    

    xq = [i for i in range(1, 31250)]
    x  = [i for i in range(1, 31250)]
    

    mic1 = random.random_sample((31250))+2046.5
    mic2 = random.random_sample((31250))+2046.5
    mic3 = random.random_sample((31250))+2046.5

   
    kryssKorr1 = correlate(mic2-2047, mic1-2047, "same")
    kryssKorr2 = correlate(mic3-2047, mic1-2047, "same")
    kryssKorr3 = correlate(mic3-2047, mic2-2047, "same")

    maxPosition1 = np.argmax(kryssKorr1)
    max_value1 = kryssKorr1[maxPosition1]
    forsinkelse1 = maxPosition1 - (len(kryssKorr1)+1)/2
    t2_1 = forsinkelse1*timePeriod

    maxPosition2 = np.argmax(kryssKorr2)
    max_value2 = kryssKorr2[maxPosition2]
    forsinkelse2 = maxPosition2 - (len(kryssKorr2)+1)/2
    t3_1 = forsinkelse2*timePeriod

    maxPosition3 = np.argmax(kryssKorr3)
    max_value3 = kryssKorr3[maxPosition3]
    forsinkelse3 = maxPosition3 - (len(kryssKorr3)+1)/2
    t3_2 = forsinkelse3*timePeriod

    print(max_value1)

    #for i in range(0, 10):
    #     print(mic1[i])
    
    tetaRad = atan(sqrt(3)*(t2_1+t3_1)/(t2_1-t3_1-2*t3_2))

    if t3_2>=0:
       tetaDeg = tetaRad*180/pi+90
    else:
        tetaDeg = tetaRad*180/pi+270

    print("Degreees %f" % (tetaDeg))



main()