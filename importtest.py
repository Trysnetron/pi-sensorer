from math import atan
from math import sqrt
from math import pi
from numpy import random

i = 0


def main():

    xq =[i for i in range(31250)]
    x =[i for i in range(31250)]
    

    mic1 = random.random_sample((3, 2))
    # Open a file
    fo = open("foo.txt", "wb")
    print ("Name of the file: ", fo.name)
    print ("Closed or not : ", fo.closed)
    print ("Opening mode : ", fo.mode)
    fo.close()

main()