import serial
import time

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
GET_INFO_SENSOR_POR_cmd = 0xB9 # V1.1 (Update)
GET_RTC_DATE_TIME_cmd   = 0xBA
GET_INFO_PIN_STATE_cmd  = 0xBB # V1.1 (New)

SET_STATUS_LED_cmd       = 0xBF # V1.1 (New)
SET_PIN_CO2_CAL_cmd      = 0xC0
SET_PIN_PMS_RESET_cmd    = 0xC1
SET_PIN_PMS_SET_cmd      = 0xC2
SET_PIN_NBIOT_PWRKEY_cmd = 0xC3
SET_PIN_NBIOT_SLEEP_cmd  = 0xC4
SET_PIN_LED_ALL_cmd      = 0xC5
SET_POLLING_SENSOR_cmd   = 0xC6 # V1.1 (Update)
SET_RTC_DATE_TIME_cmd    = 0xC7 # V1.1 (Update)
SET_PIN_FAN_ALL_cmd      = 0xC8 # V1.1 (New)

SET_PIN_CO2_CAL_key      = bytearray([0x53,0x38,0x4C,0x50])
SET_PIN_PMS_RESET_key    = bytearray([0x50,0x4D,0x53,0x33])
SET_PIN_PMS_SET_key      = bytearray([0x33,0x30,0x30,0x33])
SET_PIN_NBIOT_PWRKEY_key = bytearray([0x4E,0x42,0x2D,0x49])
SET_PIN_NBIOT_SLEEP_key  = bytearray([0x2D,0x49,0x4F,0x54])
SET_PIN_LED_ALL_key      = bytearray([0x53,0x4C,0x45,0x44])
SET_PIN_FAN_ALL_key      = bytearray([0x46,0x41,0x4E,0x63]) # V1.1 (New)


PROTOCOL_I2C_WRITE_cmd    = 0xCA
PROTOCOL_I2C_READ_cmd     = 0xCB
PROTOCOL_UART_BEGIN_cmd   = 0xCC
PROTOCOL_UART_TX_RX_cmd   = 0xCD # V1.1 (Update)
PROTOCOL_UART_TXRX_EX_cmd = 0xCE # V1.1 (New)

ENABLE_UART_ACTIVE_RX_cmd = 0xCF # V1.1 (New)
ECHO_UART_ACTIVE_RX_cmd   = 0xCF # V1.1 (New)

#expect receive

GET_TEMP_HUM_resp        = 8
GET_CO2_resp             = 8
GET_TVOC_resp            = 16
GET_LIGHT_resp           = 16
GET_PMS_resp             = 16
GET_SENSOR_ALL_resp      = 48
GET_INFO_VERSION_resp    = 6
GET_INFO_RUNTIME_resp    = 9
GET_INFO_ERROR_LOG_resp  = 16
GET_INFO_SENSOR_POR_resp = 16 # V1.1 (Update)
GET_RTC_DATE_TIME_resp   = 10
GET_INFO_PIN_STATE_resp  = 11 # V1.1 (New)

SET_STATUS_LED_resp       = 4 # V1.1 (New)
SET_PIN_CO2_CAL_resp      = 4
SET_PIN_PMS_RESET_resp    = 4
SET_PIN_PMS_SET_resp      = 4
SET_PIN_NBIOT_PWRKEY_resp = 4
SET_PIN_NBIOT_SLEEP_resp  = 4
SET_PIN_LED_ALL_resp      = 4
SET_POLLING_SENSOR_resp   = 4 # V1.1 (Update)
SET_RTC_DATE_TIME_resp    = 4 # V1.1 (Update)
SET_PIN_FAN_ALL_resp      = 4 # V1.1 (New)

PROTOCOL_I2C_WRITE_resp    = 4
#PROTOCOL_I2C_READ_resp     = 6+n
PROTOCOL_UART_BEGIN_resp   = 4
#PROTOCOL_UART_TX_RX_resp   = 6+n # V1.1 (Update)
#PROTOCOL_UART_TXRX_EX_resp = 8+n # V1.1 (New)

ENABLE_UART_ACTIVE_RX_resp = 4 # V1.1 (New)
#ECHO_UART_ACTIVE_RX_resp   = 7+n # V1.1 (New)

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


#byte formater
#convert 'int' to 'byte'
#and create proper format for multiple byte 

def convert_2_byte(int_value):
    host_send = bytearray()
    host_send.append(int_value // 256)
    host_send.append(int_value % 256)
    
    return host_send


def convert_4_byte(int_value):
    host_send = bytearray()
    byte_0 = int_value // (256 * 256 * 256)
    byte_1 = (int_value % (256 * 256 * 256)) // (256 * 256)
    byte_2 = (int_value % (256 * 256)) // 256
    byte_3 = int_value % 256
    
    host_send.append(byte_0)
    host_send.append(byte_1)
    host_send.append(byte_2)
    host_send.append(byte_3)
    
    return host_send





#==========GENERAL FUNC==========#

def GENERAL_GET(cmd):
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #b_arr = bytearray(host_send)

##    print("****")
##    print(host_send)
##    print(type(host_send))
##    print("****")
    

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


def GENERAL_RESPONSE(cmd,recive_byte):
    data = ser.read(recive_byte)

    return data

    

    


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
    
def LED_SET(cmd,state):
    #command for SET_STATUS_LED, because there is no key
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #state
    # 2 Byte
    state = convert_2_byte(state)
    host_send.extend(state)
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
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_TEMP_HUM_cmd,GET_TEMP_HUM_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


def GET_CO2():

    print("AA 55 B1 4E")
    #print(GENERAL_GET(GET_CO2_cmd))
    data = GENERAL_GET(GET_CO2_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_CO2_cmd,GET_CO2_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_TVOC():

    print("AA 55 B2 4D")
    #print(GENERAL_GET(GET_TVOC_cmd))
    data = GENERAL_GET(GET_TVOC_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_TVOC_cmd,GET_TVOC_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_LIGHT():

    print("AA 55 B3 4C")
    #print(GENERAL_GET(GET_LIGHT_cmd))
    data = GENERAL_GET(GET_LIGHT_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_LIGHT_cmd,GET_LIGHT_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_PMS():

    print("AA 55 B4 4B")
    #print(GENERAL_GET(GET_PMS_cmd))
    data = GENERAL_GET(GET_PMS_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_PMS_cmd,GET_PMS_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())
    
def GET_SENSOR_ALL():

    print("AA 55 B5 4A")
    #print(GENERAL_GET(GET_SENSOR_ALL_cmd))
    data = GENERAL_GET(GET_SENSOR_ALL_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_SENSOR_ALL_cmd,GET_SENSOR_ALL_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_INFO_VERSION():

    print("AA 55 B6 49")
    #print(GENERAL_GET(GET_INFO_VERSION_cmd))
    data = GENERAL_GET(GET_INFO_VERSION_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_VERSION_cmd,GET_INFO_VERSION_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_INFO_RUNTIME():

    print("AA 55 B7 48")
    #print(GENERAL_GET(GET_INFO_RUNTIME_cmd))
    data = GENERAL_GET(GET_INFO_RUNTIME_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_RUNTIME_cmd,GET_INFO_RUNTIME_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_INFO_ERROR_LOG():

    print("AA 55 B8 47")
    #print(GENERAL_GET(GET_INFO_ERROR_LOG_cmd))
    data = GENERAL_GET(GET_INFO_ERROR_LOG_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_ERROR_LOG_cmd,GET_INFO_ERROR_LOG_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())
    
def GET_INFO_SENSOR_POR():

    print("AA 55 B9 46")
    #print(GENERAL_GET(GET_INFO_SENSOR_POR_cmd))
    data = GENERAL_GET(GET_INFO_SENSOR_POR_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_SENSOR_POR_cmd,GET_INFO_SENSOR_POR_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_RTC_DATE_TIME():

    print("AA 55 BA 45")
    #print(GENERAL_GET(GET_RTC_DATE_TIME_cmd))
    data = GENERAL_GET(GET_RTC_DATE_TIME_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_RTC_DATE_TIME_cmd,GET_RTC_DATE_TIME_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def GET_INFO_PIN_STATE():

    print("AA 55 BB 44")
    #print(GENERAL_GET(GET_INFO_PIN_STATE_cmd))
    data = GENERAL_GET(GET_INFO_PIN_STATE_cmd)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(GET_INFO_PIN_STATE_cmd,GET_INFO_PIN_STATE_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


#===============SET COMMAND===============#
#display like 0x00 type
#data = bytearray(b'hello')
#print("".join("\\x%02x" % i for i in data))

def SET_STATUS_LED(state):

    #STATUS_LED state 0: LED off / 1: LED on / 2~65534:Pulse time length (ms)
    print("AA 55 BF 40 00 00 su ~s")
    #print(LED_SET(SET_STATUS_LED_cmd,state)) #there is no key for SET_STATUS_LED 
    data = LED_SET(SET_STATUS_LED_cmd,state)
    print("".join("%02x " % i for i in data).upper())

    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_STATUS_LED_cmd,SET_STATUS_LED_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


def SET_PIN_CO2_CAL(state):

    #CO2_CAL state default:1 / set to 0 to calibrate CO2
    print("AA 55 C0 3F 53 38 4C 50 01 su ~s")
    #print(GENERAL_SET(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_key,state))
    data = GENERAL_SET(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_CO2_CAL_cmd,SET_PIN_CO2_CAL_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


def SET_PIN_PMS_RESET(state):

    #PMS_RESET state default:1 / set to 0 to reset PM_sensor
    print("AA 55 C1 3E 50 4D 53 33 01 su ~s")
    #print(GENERAL_SET(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_key,state))
    data = GENERAL_SET(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_PMS_RESET_cmd,SET_PIN_PMS_RESET_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


def SET_PIN_PMS_SET(state):

    #PMS_SET state default:1 / set to 0 to disable PM_sensor
    print("AA 55 C2 3D 33 30 30 33 01 su ~s")
    #print(GENERAL_SET(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_key,state))
    data = GENERAL_SET(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_PMS_SET_cmd,SET_PIN_PMS_SET_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())
    

def SET_PIN_NBIOT_PWRKEY(state):

    print("AA 55 C3 3C 4E 42 4C 2D 49 su ~s")
    #print(GENERAL_SET(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_key,state))
    data = GENERAL_SET(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_NBIOT_PWRKEY_cmd,SET_PIN_NBIOT_PWRKEY_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


def SET_PIN_NBIOT_SLEEP(state):

    print("AA 55 C4 3B 2D 49 4F 54 01 su ~s")
    #print(GENERAL_SET(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_key,state))
    data = GENERAL_SET(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_NBIOT_SLEEP_cmd,SET_PIN_NBIOT_SLEEP_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


def SET_PIN_LED_ALL(state):

    #PIN_LED state default:1 / set to 0 to turnoff all LED
    print("AA 55 C5 3A 53 4C 45 44 01 su ~s")
    #print(GENERAL_SET(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_key,state))
    data = GENERAL_SET(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_LED_ALL_cmd,SET_PIN_LED_ALL_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def SET_POLLING_SENSOR(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC):

    print("AA 55 C6 39 00 00 00 00 00 00 su ~s")
    #print(POLLING_SET(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC))
    data = POLLING_SET(POLL_TEMP,POLL_CO2,POLL_TVOC,POLL_LIGHT,POLL_PMS,POLL_RTC)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_POLLING_SENSOR_cmd,SET_POLLING_SENSOR_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())
    

def SET_RTC_DATE_TIME(YY,MM,DD,hh,mm,ss):

    print("AA 55 C7 38 00 01 01 00 00 00 su ~s")
    #print(RTC_SET(YY,MM,DD,hh,mm,ss))
    data = RTC_SET(YY,MM,DD,hh,mm,ss)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_RTC_DATE_TIME_cmd,SET_RTC_DATE_TIME_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())

def SET_PIN_FAN_ALL(state):

    print("AA 55 C8 37 46 41 4E 63 01 su ~s")
    #print(GENERAL_SET(SET_PIN_FAN_ALL_cmd,SET_PIN_FAN_ALL_key,state))
    data = GENERAL_SET(SET_PIN_FAN_ALL_cmd,SET_PIN_FAN_ALL_key,state)
    print("".join("%02x " % i for i in data).upper())
    
    ser.write(bytes(data))

    reveive_data = GENERAL_RESPONSE(SET_PIN_FAN_ALL_cmd,SET_PIN_FAN_ALL_resp)
    print(reveive_data)
    print("".join("%02x " % i for i in reveive_data).upper())


#===============PROTOCOL COMMAND===============#


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
    host_send.extend(i2c_data)
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
    #TX_DATA_length : 2 Byte / RX_LENGTH : 2 Byte / TIMEOUT : 2 Byte
    cmd = PROTOCOL_UART_TX_RX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    
    #UART TX data length (TX_DATA is bytearray)
    TX_DATA_length = convert_2_byte(len(TX_DATA))
    host_send.extend(TX_DATA_length)
    
    #recive length of RX data
    RX_LENGTH = convert_2_byte(RX_LENGTH)
    host_send.extend(RX_LENGTH)
    
    #timeout time for RX data
    TIMEOUT = convert_4_byte(TIMEOUT)
    host_send.extend(TIMEOUT)

    #UART TX data 
    host_send.extend(TX_DATA)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))
    
    return host_send


def PROTOCOL_UART_TXRX_EX(UART_PORT,TX_DATA,BYTE_TIMEOUT,WAIT_TIMEOUT):
    #TX_DATA_length : 2 Byte / BYTE_TIMEOUT : 1 Byte / WAIT_TIMEOUT : 2 Byte
    cmd = PROTOCOL_UART_TXRX_EX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #UART TX data length (TX_DATA is bytearray)
    TX_DATA_length = convert_2_byte(len(TX_DATA))
    host_send.extend(TX_DATA_length)
    #BYTE_TIMEOUT :相鄰BYTE間隔時間的最大值 數值設為0 定義為 0.5ms
    host_send.append(BYTE_TIMEOUT)
    #WAIT_TIMEOUT :接收RX_DATA 的TIMEOUT 數值範圍 0~600000ms
    WAIT_TIMEOUT = convert_4_byte(WAIT_TIMEOUT)
    host_send.extend(WAIT_TIMEOUT)
    
    #UART TX data 
    host_send.extend(TX_DATA)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))

    return host_send


def ENABLE_UART_ACTIVE_RX(UART_PORT,ENABLE,POLLING_TIME,BYTE_TIMEOUT,RCV_TIMEOUT):
    #TRCV_TIMEOUT : 2 Byte
    cmd = ENABLE_UART_ACTIVE_RX_cmd
    host_send = bytearray()
    host_send.append(leading_cmd)
    host_send.append(bit_reverse(leading_cmd))
    host_send.append(cmd)
    host_send.append(bit_reverse(cmd))
    #choose UART port (0~2) (0:NB-IOT/1:Hardware UART/2:Software UART)
    host_send.append(UART_PORT)
    #UART ENABLE
    host_send.append(ENABLE)
    #POLLING_TIME
    host_send.append(POLLING_TIME)
    #BYTE_TIMEOUT :相鄰BYTE間隔時間的最大值 數值設為0 定義為 0.5ms
    host_send.append(BYTE_TIMEOUT)
    #RCV_TIMEOUT 
    RCV_TIMEOUT = convert_2_byte(RCV_TIMEOUT)
    host_send.extend(RCV_TIMEOUT)
    #checksum
    sum_byte = crc_calc(host_send)
    host_send.append(sum_byte)
    host_send.append(bit_reverse(sum_byte))


    return host_send




#===============TEST ALL ===============#
print("START")
ser=serial.Serial("COM57",115200,timeout=1)
time.sleep(5)

#===============TEST GET===============#

print("===============TEST GET===============\n")

print("GET_TEMP_HUM:")
GET_TEMP_HUM()
print("\n")

print("GET_CO2:")
GET_CO2()
print("\n")

print("GET_TVOC:")
GET_TVOC()
print("\n")

print("GET_LIGHT:")
GET_LIGHT()
print("\n")

print("GET_PMS:")
GET_PMS()
print("\n")

print("GET_SENSOR_ALL:")
GET_SENSOR_ALL()
print("\n")

print("GET_INFO_VERSION:")
GET_INFO_VERSION()
print("\n")

print("GET_INFO_RUNTIME:")
GET_INFO_RUNTIME()
print("\n")

print("GET_INFO_ERROR_LOG:")
GET_INFO_ERROR_LOG()
print("\n")

print("GET_INFO_SENSOR_POR:")
GET_INFO_SENSOR_POR()
print("\n")

print("GET_RTC_DATE_TIME:")
GET_RTC_DATE_TIME()
print("\n")

print("GET_INFO_PIN_STATE:")
GET_INFO_PIN_STATE()
print("\n")

#===============TEST SET===============#

print("===============TEST SET===============\n")

print("SET_STATUS_LED:")
SET_STATUS_LED(0)
SET_STATUS_LED(1)
#SET_STATUS_LED(2567)
print("\n")

print("SET_PIN_CO2_CAL:")
SET_PIN_CO2_CAL(0)
SET_PIN_CO2_CAL(1)
print("\n")

print("SET_PIN_PMS_RESET:")
SET_PIN_PMS_RESET(0)
SET_PIN_PMS_RESET(1)
print("\n")

print("SET_PIN_PMS_SET:")
SET_PIN_PMS_SET(0)
SET_PIN_PMS_SET(1)
print("\n")

print("SET_PIN_NBIOT_PWRKEY:")
SET_PIN_NBIOT_PWRKEY(0)
SET_PIN_NBIOT_PWRKEY(1)
print("\n")

print("SET_PIN_NBIOT_SLEEP:")
SET_PIN_NBIOT_SLEEP(0)
SET_PIN_NBIOT_SLEEP(1)
print("\n")

print("SET_PIN_LED_ALL:")
SET_PIN_LED_ALL(0)
SET_PIN_LED_ALL(1)
print("\n")

print("SET_POLLING_SENSOR:")
SET_POLLING_SENSOR(1,1,1,1,1,1)
print("\n")

print("SET_RTC_DATE_TIME:")
SET_RTC_DATE_TIME(0,1,1,0,0,0)
print("\n")

print("SET_PIN_FAN_ALL:")
SET_PIN_FAN_ALL(0)
SET_PIN_FAN_ALL(1)
print("\n")

#===============TEST PROTOCOL===============#

print("===============TEST PROTOCOL===============\n")

#i2c_address,i2c_data
i2c_address = 0X3C

UART_PORT = 0
BAUD = 0
i2c_data = bytearray([0X01,0X02,0X03,0X04])
TX_DATA = bytearray([0X01,0X02,0X03,0X04])

i2c_read_length = len(i2c_data)
RX_LENGTH = 5
TIMEOUT = 0
WAIT_TIMEOUT = 5
ENABLE = 1
POLLING_TIME = 0
BYTE_TIMEOUT = 10
RCV_TIMEOUT = 15

print("PROTOCOL_I2C_WRITE:")
print("AA 55 CA 35 00 3C 04 01 02 03 04 su ~s")
data = PROTOCOL_I2C_WRITE(i2c_address,i2c_data)
print("".join("%02x " % i for i in data).upper())
print("\n")


print("PROTOCOL_I2C_READ:")
print("AA 55 CB 34 00 3C 04 su ~s")
data = PROTOCOL_I2C_READ(i2c_address,i2c_read_length)
print("".join("%02x " % i for i in data).upper())
print("\n")


print("PROTOCOL_UART_BEGIN:")
print("AA 55 CC 33 00 00 00 su ~s")
data = PROTOCOL_UART_BEGIN(UART_PORT,BAUD)
print("".join("%02x " % i for i in data).upper())
print("\n")


print("PROTOCOL_UART_TX_RX:")
print("AA 55 CD 32 00 00 04 00 05 00 00 00 00 01 02 03 04 su ~s")
data = PROTOCOL_UART_TX_RX(UART_PORT,TX_DATA,RX_LENGTH,TIMEOUT)
print("".join("%02x " % i for i in data).upper())
print("\n")


print("PROTOCOL_UART_TXRX_EX:")
print("AA 55 CE 31 00 00 04 0A 00 00 00 05 01 02 03 04 su ~s")
data = PROTOCOL_UART_TXRX_EX(UART_PORT,TX_DATA,BYTE_TIMEOUT,WAIT_TIMEOUT)
print("".join("%02x " % i for i in data).upper())
print("\n")


print("ENABLE_UART_ACTIVE_RX:")
print("AA 55 CF 30 00 01 00 0A 00 0F su ~s")
data = ENABLE_UART_ACTIVE_RX(UART_PORT,ENABLE,POLLING_TIME,BYTE_TIMEOUT,RCV_TIMEOUT)
print("".join("%02x " % i for i in data).upper())
print("\n")


#ser=serial.Serial("COM11",115200,timeout=0.5)

ser.close()
print("OK")




























