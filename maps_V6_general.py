#note: Let's keep things simple :)

#initial part

#import libary & function part
#=================================#
import os
import time
from datetime import datetime

import libs.display as oled
import libs.color_text as color

import threading

#import current file's config, by getting the script name with '.py' replace by '_confg'
#ex: import "maps_V6_general.py" > "maps_V6_general_config" as Conf
PATH_OF_CONFIG = str(os.path.basename(__file__)[:-3] + "_config")
Conf = __import__(PATH_OF_CONFIG)

#let's change it to a easier way
#fields = Conf.fields
values = Conf.values




#system check(hardware/internet/time)
#=================================#
'''
check_time()
check_new_version()
check_serial_port()
'''




#use dummy data for now
#=================================#
#notice!! you just need a dummy msg, don't need to make a real function
values["device_id"] = Conf.DEVICE_ID
values["ver_app"] = Conf.Version
pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
values["date"] = pairs[0]
values["time"] = pairs[1]
#values["tick"] = 0
#values["tick"] = float(f.readline().split()[0])
try:
    with open('/proc/uptime', 'r') as f:
        values["tick"] = float(f.readline().split()[0])
except:
    print("Error: reading /proc/uptime")
values["s_t0"] = 26.13
values["s_h0"] = 60.00
values["s_d2"] = 15
values["s_d0"] = 13
values["s_d1"] = 7
values["s_l0"] = 4401
values["s_lr"] = 3250
values["s_lg"] = 3370
values["s_lb"] = 4147
values["s_lc"] = 1003
values["s_gh"] = 600
values["s_gg"] = 1337

msg = ""

for item in values:
    msg = msg + "|" + item + "=" + str(values[item])
msg = msg + "|"

#print("\033[35m%s\033[0m" %("base msg:"))
#print(COLOR_PURPLE + "base msg:" + COLOR_REST)
color.print_p("base msg:")
print(msg)




##data storage
#=================================#
def storage():

    if len(os.listdir("/media/pi")):
        path = "/media/pi/" + os.listdir("/media/pi")[0]

    else:
        path = Conf.FS_SD

    #CSV_items =  ['device_id', 'date', 'time', 'Tmp',  'RH',   'PM2.5','PM10', 'PM1.0','RGB_R','RGB_G','RGB_B','RGB_C','Lux',  'CO2',  'TVOC']
    #CSV_type  =  ['string',    'date', 'time', 'float','float','int',  'int',  'int',  'int',  'int'  ,'int',  'int',  'int',  'int',  'int' ]
    CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
    CSV_msg = ""

    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    values["date"] = pairs[0]
    values["time"] = pairs[1]


    for item in CSV_items:
        if item in values:
            CSV_msg = CSV_msg + str(values[item]) + ','
        else:
            CSV_msg = CSV_msg + "N/A" + ','
    CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

    #print(COLOR_PURPLE + "CSV_MSG:" + COLOR_REST)
    color.print_p("CSV_MSG:")
    print(CSV_msg)

    #remember to add USB drive storage!!
    with open(path + "/" + values["date"] + ".csv", "a") as f:
        f.write(CSV_msg + "\n")




##data upload

def upload():
    restful_str = "wget -O /tmp/last_upload.log \"" + Conf.Restful_URL + "topic=" + Conf.APP_ID + "&device_id=" + Conf.DEVICE_ID + "&key=" + Conf.SecureKey + "&msg=" + msg + "\""

    #print(COLOR_PURPLE + "restful_str:" + COLOR_REST)
    color.print_p("restful_str:")
    print(restful_str)

    os.system(restful_str)




##check connection




##display

def display():
    #oled.clear()
    oled.flush()
    pairs = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    oled.line("ID: " + values["device_id"])
    oled.line("Date: " + str(pairs[0]))
    oled.line("Time: " + str(pairs[1]))
    oled.line("Temp: " + str(values["s_t0"]) + " / " + "RH: " + str(values["s_h0"]))
    oled.line("PM2.5: " + str(values["s_d0"]) + " μm")
    oled.line("CO2: " + str(values["s_gh"]) + " ppm")
    oled.line("IP: " + Conf.DEVICE_IP)
    oled.show()




def show_task():
    while True:
        display()
        time.sleep(0.1)






#main start here

print("START")
#storage()
print("storage OK !!!!!!!")
#upload()
print("upload OK !!!!!!!")
#display()


#start oled displaying
t = threading.Thread(target = show_task)
t.setDaemon(True)
t.start()





count = 0

while True:

    print("loop: " + str(count))
    count = count + 1
    #display()
    storage()
    #time.sleep(Conf.Interval_LCD)
    time.sleep(10)



print("OK")

