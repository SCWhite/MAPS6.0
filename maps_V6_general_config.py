#create by useless_patato

#import lib.pm_g3 as pm_sensor
#import lib.th_htu21d as tmp_sensor
#import lib.light_tcs34725 as light_sensor
#import gas_tvoc_sgp30 as gas_sensor
#import lib.gas_co2_s8 as gas_sensor
#import pyupm_i2clcd as upmLCD

#import libs.serial_port as uno_sensor
#import libs.module_htu21d as  tmp_sensor

Version = "6.0.0" #for next generation PI version

#sencer configure
Sense_PM = 1
Sense_Tmp = 1
Sense_Light = 1
Sense_Co2 = 1
Sense_TVOC = 1
#Use_RTC_DS3231 = 1
Nbiot_Sim7000 = 1

#list every value 
GPS_LAT = 25.1933
GPS_LON = 121.7870
APP_ID = "MAPS6"  #need to change for PI version
DEVICE = "Rsapberry_PI"
DEVICE_ID = "DEVICE_ID1234"
DEVICE_IP = ''
s_t0 = 0.0
s_h0 = 0.0
s_d2 = 0.0
s_d0 = 0
s_d1 = 0
s_l0 = 0
s_lr = 0
s_lg = 0
s_lb = 0
s_lc = 0
s_gh = 400
s_gg = 0
uptime = 0

#changeable interval
Interval_LCD = 5

Restful_URL = "https://data.lass-net.org/Upload/MAPS-secure.php?"
Restful_interval = 300			# 300 seconds

SecureKey = "NoKey"

#FS_SD = "/mnt/mmcblk0p1"  #need to change
FS_SD = "/home/pi/MAPS6.0/data"
#========================#

import uuid
import re
import os
from multiprocessing import Queue

float_re_pattern = re.compile("^-?\d+\.\d+$")
num_re_pattern = re.compile("^-?\d+\.\d+$|^-?\d+$")

mac = open('/sys/class/net/eth0/address').readline().upper().strip()
DEVICE_ID = mac.replace(':','')

#do a '\' before space from "cut -d" to escape ' ' character
f = os.popen('ifconfig eth0 | grep "inet\ " | cut -d \  -f10')
DEVICE_IP=f.read()
if(DEVICE_IP == ''):
        f = os.popen('ifconfig wlan0 | grep "inet\ " | cut -d \  -f10')
        DEVICE_IP=f.read()

print("ID:"+DEVICE_ID)
print("wlan IP:"+DEVICE_IP)

#if Use_RTC_DS3231 == 1:
#	import mraa
#	import hmac
#	import hashlib
#	import base64
#	import urllib
#	import urllib.parse

#	DS3231_I2C_ADDR = 0x68
#need change
#	rtc = mraa.I2c(0)
#	rtc.address(DS3231_I2C_ADDR)
#	SecureKey = chr(rtc.readReg(0x07)) + chr(rtc.readReg(0x08)) + chr(rtc.readReg(0x09)) + chr(rtc.readReg(0x0A)) + chr(rtc.readReg(0x0B)) + chr(rtc.readReg(0x0C)) + chr(rtc.readReg(0x0D))
#	SecureKey = urllib.parse.quote_plus(SecureKey)
#	print("SecureKey = " , SecureKey)

#pm_q = Queue(maxsize=5)
#tmp_q = Queue(maxsize=5)
#light_q = Queue(maxsize=5)
#gas_q = Queue(maxsize=5)
#tvoc_q = Queue(maxsize=5)

#note: honeywell CO2 use "s_gh" instead of  SenseAir S8 "s_g8"

fields ={       "Tmp"   :       "s_t0",
                "RH"    :       "s_h0",
                "PM1.0" :       "s_d2",
                "PM2.5" :       "s_d0",
                "PM10"  :       "s_d1",
                "Lux"   :       "s_l0",
		"RGB_R"	:	"s_lr",
		"RGB_G"	:	"s_lg",
		"RGB_B"	:	"s_lb",
		"RGB_C"	:	"s_lc",
                "CO2"   :       "s_gh",
		"TVOC"	:	"s_gg",
        }
values = {      "app"           :       APP_ID,
                "device_id"     :       DEVICE_ID,
                "device"        :       DEVICE,
                "ver_format"    :       3,
                "fmt_opt"       :       0,
                "gps_lat"       :       GPS_LAT,
                "gps_lon"       :       GPS_LON,
                "FAKE_GPS"      :       1,
                "gps_fix"       :       1,
                "gps_num"       :       100,
                "date"          :       "1900-01-01",
                "time"          :       "00:00:00",
        }

#new version of value
'''
values = {      "app"           :       APP_ID,
                "app_ver"       :       Version,
                "device"        :       DEVICE,
                "device_id"     :       DEVICE_ID,
                "ver_format"    :       3,
                "fmt_opt"       :       0,
                "gps_lat"       :       GPS_LAT,
                "gps_lon"       :       GPS_LON,
                "FAKE_GPS"      :       1,
                "gps_fix"       :       1,
                "gps_num"       :       100,
                "date"          :       "1900-01-01",
                "time"          :       "00:00:00",
                "tick"          :       uptime,
                "Tmp"           :       s_t0,
                "RH"            :       s_h0,
                "PM1.0"         :       s_d2,
                "PM2.5"         :       s_d0,
                "PM10"          :       s_d1,
                "Lux"           :       s_l0,
                "RGB_R"         :       s_lr,
                "RGB_G"         :       s_lg,
                "RGB_B"         :       s_lb,
                "RGB_C"         :       s_lc,
                "CO2"           :       s_gh,
                "TVOC"          :       s_gg,
        }
'''
