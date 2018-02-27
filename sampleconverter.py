bytesarray = []

with open('./samples.bin', mode='rb') as binfile:
    b = binfile.read(3)
    while b:
        #print(s.encode('utf-8').decode('ascii'))
        bytesarray.append(ord(b))
        b = binfile.read(3)
print("Done reading")

with open('./samples.txt', mode='w') as txtfile:
    for i in range(len(bytesarray)):
        txtfile.write(str(bytesarray[i]) + "\n")
print("Done writing")