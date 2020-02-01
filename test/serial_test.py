import serial
import time

#command code
#AA 55 C8 37 46 41 4E 63 01 46 B9 
#data = [0xAA,0x55,0xB1,0x4E]

fan_on = bytearray([0xAA, 0x55, 0xC8, 0x37, 0x46, 0x41, 0x4E, 0x63, 0x01, 0x46, 0xB9])
fan_off = bytearray([0xAA, 0x55, 0xC8, 0x37, 0x46, 0x41, 0x4E, 0x63, 0x00, 0x47, 0xB8])
get = bytearray([0xAA,0x55,0xB0,0x4F])  

#fan_on = [0xAA, 0x55, 0xC8, 0x37, 0x46, 0x41, 0x4E, 0x63, 0x01, 0x46, 0xB9]
#fan_off = [0xAA, 0x55, 0xC8, 0x37, 0x46, 0x41, 0x4E, 0x63, 0x00, 0x47, 0xB8]


ser=serial.Serial("COM57",115200, timeout=1)
time.sleep(5)

#print(fan_on)
#print(fan_off)

###turn on fan
##ser.write(bytes(fan_on))
##print(type(fan_on))
##recive = ser.read(4)
##print(recive)
##time.sleep(5)
##
###turn off fan
##ser.write(bytes(fan_off))
##recive = ser.read(4)
##print(recive)
##time.sleep(5)


#get temp hum
ser.write(bytes(get))
recive = ser.read(8)
print(recive.hex())

temp = (recive[2]*256 + recive[3])/100
hum  = (recive[4]*256 + recive[5])/100

print(temp)
print(hum)
time.sleep(5)

ser.write(bytes(get))
recive = ser.read(8)
print(recive.hex())

temp = (recive[2]*256 + recive[3])/100
hum  = (recive[4]*256 + recive[5])/100

print(temp)
print(hum)
time.sleep(5)

ser.write(bytes(get))
recive = ser.read(8)
print(recive.hex())

temp = (recive[2]*256 + recive[3])/100
hum  = (recive[4]*256 + recive[5])/100

print(temp)
print(hum)
time.sleep(5)

###turn on fan
##ser.write(fan_on)
##recive = ser.read(4)
##print(recive)
##time.sleep(5)
##
###turn off fan
##ser.write(fan_off)
##recive = ser.read(4)
##print(recive)
##time.sleep(5)


print("OK")

ser.close()
