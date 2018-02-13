#!/usr/bin/python3
from math import atan
from math import sqrt
from math import pi
from numpy import random
from numpy import correlate
from numpy import interp

def main():
    speedofsound = 34300 #cm/s
    d = 3.5 #cm
    maxDelay = d/speedofsound

    fs = 27700
    timePeriod = 1/fs
    numSamples = 30
    I = 8

    x = [i/I for i in range(0, numSamples*I)]
    xp  = [i for i in range(0, numSamples)]

    mic1 = random.random_sample((numSamples))+2046.5
    mic1 = interp(x,xp,mic1)
    mic2 = random.random_sample((numSamples))+2046.5
    mic2 = interp(x,xp,mic2)
    mic3 = random.random_sample((numSamples))+2046.5
    mic3 = interp(x,xp,mic3)

    #for i in range(0, 10):
    #    print(mic1[i])

   
    kryssKorr1 = correlate(mic2-2047, mic1-2047, "same")
    kryssKorr2 = correlate(mic3-2047, mic1-2047, "same")
    kryssKorr3 = correlate(mic3-2047, mic2-2047, "same")

    maxPosition1 = numpy.argmax(kryssKorr1)
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

    #print(max_value1)

    #for i in range(0, 10):
    #     print(mic1[i])
    
    tetaRad = atan(sqrt(3)*(t2_1+t3_1)/(t2_1-t3_1-2*t3_2))

    if t3_2>=0:
       tetaDeg = tetaRad*180/pi+90
    else:
        tetaDeg = tetaRad*180/pi+270

    print("Degreees %f" % (tetaDeg))



main()