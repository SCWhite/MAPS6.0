import serial

#command code
leading_cmd             = 0xAA
GET_TEMP_HUM_cmd        = 0xB0
GET_CO2_cmd             = 0xB1
GET_TVOC_cmd            = 0xB2
GET_LIGHT_cmd           = 0xB3
GET_PMS_cmd             = 0xB4
GET_SENSOR_ALL_cmd      = 0xB5
GET_INFO_VERSION_cmd    = 0xB6
GET_INFO_RUNTIME_cmd    = 0xB7
GET_INFO_ERROR_LOG_cmd  = 0xB8
GET_INFO_SENSOR_POR_cmd = 0xB9
GET_RTC_DATE_TIME_cmd   = 0xBA

SET_PIN_CO2_CAL_cmd      = 0xC0
SET_PIN_PMS_RESET_cmd    = 0xC1
SET_PIN_PMS_SET_cmd      = 0xC2
SET_PIN_NBIOT_PWRKEY_cmd = 0xC3
SET_PIN_NBIOT_SLEEP_cmd  = 0xC4
SET_PIN_LED_ALL_cmd      = 0xC5
SET_POLLING_SENSOR_cmd   = 0xC6
SET_RTC_DATE_TIME_cmd    = 0xC7

SET_PIN_CO2_CAL_key      = bytearray([0x53,0x38,0x4C,0x50])
SET_PIN_PMS_RESET_key    = bytearray([0x50,0x4D,0x53,0x33])
SET_PIN_PMS_SET_key      = bytearray([0x33,0x30,0x30,0x33])
SET_PIN_NBIOT_PWRKEY_key = bytearray([0x4E,0x42,0x2D,0x49])
SET_PIN_NBIOT_SLEEP_key  = bytearray([0x2D,0x49,0x4F,0x54])
SET_PIN_LED_ALL_key      = bytearray([0x53,0x4C,0x45,0x44])


PROTOCOL_I2C_WRITE_cmd   = 0xCA
PROTOCOL_I2C_READ_cmd    = 0xCB
PROTOCOL_UART_BEGIN_cmd  = 0xCC
PROTOCOL_UART_TX_RX_cmd  = 0xCD


#==========CONVERT FUNC==========#

#Bit_not
#therer is 2 ways to do
#1. (N xor 0xFF...) / any digit xor with (len(n) of 1) will be reverse / 
#2. use (~N & 0xFF) / this will limit output to just 1byte  <- choose this one

def bit_reverse(byte_command):
    rev_command = (~byte_command & 0xFF)

    return rev_command

#crc_calc
#checksum = ∑( Byte n xor (n%256) )
# so in loop of len(Byte), every Byte do xor with n 
# and sum every thing, do a AND with 0xFF limit to 1 Byte

def crc_calc(byte_arr):
    checksum = 0x00    
    for i in range(len(byte_arr)):
        checksum = checksum + (byte_arr[i] ^ ((i+1)%256))
        #print(hex(byte_arr[i]).upper() + ' ^ ' + hex(((i+1)%256)).upper() + ' = ' + hex(byte_arr[i] ^ ((i+1)%256)).upper()) 
    checksum = (checksum & 0xFF)

    return checksum


#==========GENERAL FUNC==========#

def GENERAL_GET(cmd):
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #b_arr = bytearray(host_send)

    return host_send

def GENERAL_SET(cmd,key,state):
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #key
    host_send.append(key[0])
    host_send.append(key[1])
    host_send.append(key[2])
    host_send.append(key[3])
    #state
    host_send.append(state)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def POLLING_SET(temp_sw,co2_sw,tvoc_sw,light_sw,pms_sw,rtc_sw):
    #command for SET_POLLING_SENSOR
    cmd = SET_POLLING_SENSOR_cmd
    
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #state for 6 sensor
    host_send.append(temp_sw)
    host_send.append(co2_sw)
    host_send.append(tvoc_sw)
    host_send.append(light_sw)
    host_send.append(pms_sw)
    host_send.append(rtc_sw)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def RTC_SET(YY,MM,DD,hh,mm,ss):
    #command for SET_RTC_DATE_TIME
    cmd = SET_RTC_DATE_TIME_cmd
    
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #state for 6 sensor
    host_send.append(YY)
    host_send.append(MM)
    host_send.append(DD)
    host_send.append(hh)
    host_send.append(mm)
    host_send.append(ss)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send
    

    

#===============GET COMMAND===============#
def GET_TEMP_HUM():

    #ser.write()
    print("AA 55 B0 4F")
    #print(GENERAL_GET(GET_TEMP_HUM_cmd))
    data = GENERAL_GET(GET_TEMP_HUM_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_CO2():

    print("AA 55 B1 4E")
    #print(GENERAL_GET(GET_CO2_cmd))
    data = GENERAL_GET(GET_CO2_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_TVOC():

    print("AA 55 B2 4D")
    #print(GENERAL_GET(GET_TVOC_cmd))
    data = GENERAL_GET(GET_TVOC_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_LIGHT():

    print("AA 55 B3 4C")
    #print(GENERAL_GET(GET_LIGHT_cmd))
    data = GENERAL_GET(GET_LIGHT_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_PMS():

    print("AA 55 B4 4B")
    #print(GENERAL_GET(GET_PMS_cmd))
    data = GENERAL_GET(GET_PMS_cmd)
    print("".join("%02x " % i for i in data).upper())
    
def GET_SENSOR_ALL():

    print("AA 55 B5 4A")
    #print(GENERAL_GET(GET_SENSOR_ALL_cmd))
    data = GENERAL_GET(GET_SENSOR_ALL_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_INFO_VERSION():

    print("AA 55 B6 49")
    #print(GENERAL_GET(GET_INFO_VERSION_cmd))
    data = GENERAL_GET(GET_INFO_VERSION_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_INFO_RUNTIME():

    print("AA 55 B7 48")
    #print(GENERAL_GET(GET_INFO_RUNTIME_cmd))
    data = GENERAL_GET(GET_INFO_RUNTIME_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_INFO_ERROR_LOG():

    print("AA 55 B8 47")
    #print(GENERAL_GET(GET_INFO_ERROR_LOG_cmd))
    data = GENERAL_GET(GET_INFO_ERROR_LOG_cmd)
    print("".join("%02x " % i for i in data).upper())
    
def GET_INFO_SENSOR_POR():

    print("AA 55 B9 46")
    #print(GENERAL_GET(GET_INFO_SENSOR_POR_cmd))
    data = GENERAL_GET(GET_INFO_SENSOR_POR_cmd)
    print("".join("%02x " % i for i in data).upper())

def GET_RTC_DATE_TIME():

    print("AA 55 BA 45")
    #print(GENERAL_GET(GET_RTC_DATE_TIME_cmd))
    data = GENERAL_GET(GET_RTC_DATE_TIME_cmd)
    print("".join("%02x " % i for i in data).upper())



#===============SET COMMAND===============#
#display like 0x00 type
#data = bytearray(b'hello')
#print("".join("\\x%02x" % i for i in data))
    
def SET_PIN_CO2_CAL(state):

    print("AA 55 C0 3F 53 38 4C 50 01 su ~s")
    #print(GENERAL_SET(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_key,state))
    data = GENERAL_SET(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_key,state)
    print("".join("%02x " % i for i in data).upper())


def SET_PIN_PMS_RESET(state):

    print("AA 55 C1 3E 50 4D 53 33 01 su ~s")
    #print(GENERAL_SET(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_key,state))
    data = GENERAL_SET(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_key,state)
    print("".join("%02x " % i for i in data).upper())


def SET_PIN_PMS_SET(state):

    print("AA 55 C2 3D 33 30 30 33 01 su ~s")
    #print(GENERAL_SET(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_key,state))
    data = GENERAL_SET(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_key,state)
    print("".join("%02x " % i for i in data).upper())
    

def SET_PIN_NBIOT_PWRKEY(state):

    print("AA 55 C3 3C 4E 42 4C 2D 49 su ~s")
    #print(GENERAL_SET(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_key,state))
    data = GENERAL_SET(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_key,state)
    print("".join("%02x " % i for i in data).upper())


def SET_PIN_NBIOT_SLEEP(state):

    print("AA 55 C4 3B 2D 49 4F 54 01 su ~s")
    #print(GENERAL_SET(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_key,state))
    data = GENERAL_SET(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_key,state)
    print("".join("%02x " % i for i in data).upper())


def SET_PIN_LED_ALL(state):

    print("AA 55 C5 3A 53 4C 45 44 01 su ~s")
    #print(GENERAL_SET(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_key,state))
    data = GENERAL_SET(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_key,state)
    print("".join("%02x " % i for i in data).upper())

def SET_POLLING_SENSOR(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC):

    print("AA 55 C6 39 00 00 00 00 00 00 00 su ~s")
    #print(POLLING_SET(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC))
    data = POLLING_SET(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC)
    print("".join("%02x " % i for i in data).upper())
    

def SET_RTC_DATE_TIME(YY,MM,DD,hh,mm,ss):

    print("AA 55 C7 38 00 01 01 00 00 00 00 su ~s")
    #print(RTC_SET(YY,MM,DD,hh,mm,ss))
    data = RTC_SET(YY,MM,DD,hh,mm,ss)
    print("".join("%02x " % i for i in data).upper())



#===============PROTOCOL COMMAND===============#

# TO DO

def PROTOCOL_I2C_WRITE(i2c_address,i2c_data,freq = 0):
    cmd = PROTOCOL_I2C_WRITE_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #i2c frequency (0~4) (0:no change/1:400Khz/2:200Khz/3:100Khz/4:50Khz)
    host_send.append(freq)
    #i2c address(0~127)
    host_send.append(i2c_address)
    #i2c data length
    host_send.append(len(i2c_data))
    #i2c data(N-byte bytearray)
    host_send.append(i2c_data)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send

def PROTOCOL_I2C_READ(i2c_address,i2c_read_length,freq = 0):
    cmd = PROTOCOL_I2C_READ_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose i2c frequency (0~4) (0:no change/1:400Khz/2:200Khz/3:100Khz/4:50Khz)
    host_send.append(freq)
    #set i2c address(0~127)
    host_send.append(i2c_address)
    #set i2c data read length(1~32)
    host_send.append(i2c_read_length)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def PROTOCOL_UART_BEGIN(UART_PORT,BAUD = 0,FORMAT = 0):
    cmd = PROTOCOL_UART_BEGIN_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #set baudrate (0~4) (0:9600/1:19200/2:38400/3:57600/4:115200)
    host_send.append(BAUD)
    #set UART format (0~5) (0:N81/1:N71/2:E81/3:E71/4:O81/5:O71)
    host_send.append(FORMAT)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send

    
def PROTOCOL_UART_TX_RX(UART_PORT,TX_DATA,RX_LENGTH,TIMEOUT):
    cmd = PROTOCOL_UART_TX_RX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #UART TX data length (TX_DATA is bytearray)
    host_send.append(TX_DATA_length[0])
    host_send.append(TX_DATA_length[1])
    #recive length of RX data
    host_send.append(RX_LENGTH[0])
    host_send.append(RX_LENGTH[1])
    #timeout time for RX data
    host_send.append(TIMEOUT[0])
    host_send.append(TIMEOUT[1])
    #UART TX data 
    host_send.append(TX_DATA)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


#===============TEST ALL ===============#
print("START")



#===============TEST GET===============#
GET_TEMP_HUM()
print("\n")
GET_CO2()
print("\n")
GET_TVOC()
print("\n")
GET_LIGHT()
print("\n")
GET_PMS()
print("\n")
GET_SENSOR_ALL()
print("\n")
GET_INFO_VERSION()
print("\n")
GET_INFO_RUNTIME()
print("\n")
GET_INFO_ERROR_LOG()
print("\n")
GET_INFO_SENSOR_POR()
print("\n")
GET_RTC_DATE_TIME()
print("\n")

#===============TEST SET===============#
SET_PIN_CO2_CAL(0)
SET_PIN_CO2_CAL(1)
print("\n")
SET_PIN_PMS_RESET(0)
SET_PIN_PMS_RESET(1)
print("\n")
SET_PIN_PMS_SET(0)
SET_PIN_PMS_SET(1)
print("\n")
SET_PIN_NBIOT_PWRKEY(0)
SET_PIN_NBIOT_PWRKEY(1)
print("\n")
SET_PIN_NBIOT_SLEEP(0)
SET_PIN_NBIOT_SLEEP(1)
print("\n")
SET_PIN_LED_ALL(0)
SET_PIN_LED_ALL(1)
print("\n")
SET_POLLING_SENSOR(1,1,1,1,1,1)
print("\n")
SET_RTC_DATE_TIME(19,12,8,12,30,31)
print("\n")

#===============TEST PROTOCOL===============#

# TO DO




#ser=serial.Serial("COM11",115200,timeout=0.5)


print("OK")




























