from math import atan
from math import sqrt
from math import pi

i = 0


def main():
    speedofsound = 34300; #cm/s
    d = 3.5; #cm
    maxDelay = d/speedofsound;



    t4_3 = -1;
    t5_3 = 1;
    t5_4 = 2;

    
    tetaRad = atan(sqrt(3)*(t4_3+t5_3)/(t4_3-t5_3-2*t5_4));

    if t5_4>=0:
        tetaDeg = tetaRad*180/pi+90;
    else:
        tetaDeg = tetaRad*180/pi+270;

    print("Degreees %f" % (tetaDeg))



main()