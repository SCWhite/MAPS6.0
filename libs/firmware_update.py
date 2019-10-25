import os

#avrdude -C/home/pi/avrdude.conf -v -patmega328p -carduino -P/dev/ttyACM0 -b115200 -D -Uflash:w:/home/pi/htu21d_serial_send_with_oled.ino.with_bootloader.standard.hex:i

#format for avrdude
#avrdude
#-C/home/pi/avrdude.conf
#-v
#-patmega328p
#-carduino
#-P/dev/ttyACM0
#-b115200
#-D
#-Uflash:w:/home/pi/htu21d_serial_send_with_oled.ino.with_bootloader.standard.hex:i

#defult for UNO
conf_path = "/home/pi/MAPS6.0/firmware/avrdude.conf"
microcontroller_type = "atmega328p"
programmer = "arduino"
port_path = "/dev/ttyACM0"
baud_rate = "115200"
method = "flash"
operation = "w"
hex_path = "/home/pi/MAPS6.0/firmware/htu21d_serial_send_with_oled.ino.with_bootloader.standard.hex"

#config for MEGA2560
#conf_path = "/home/pi/MAPS6.0/firmware/avrdude.conf"
#microcontroller_type = "atmega2560"
#programmer = "wiring"
#port_path = "/dev/ttyACM0"
#baud_rate = "115200"
#method = "flash"
#operation = "w"
#hex_path = "/home/pi/MAPS6.0/firmware/htu21d_serial_send_with_oled.ino.with_bootloader.standard.hex"

#general setting
#conf_path = "/home/pi/MAPS6.0/firmware/avrdude.conf"
#port_path = "/dev/ttyACM0"
#baud_rate = "115200"
#method = "flash"
#operation = "w"
#hex_path = "/home/pi/MAPS6_MCU_with_oled.ino.with_bootloader.mega.hex"




'''
Conf_path_part = " -C" + conf_path
v_part = " -v"
microcontroller_part = " -p" + microcontroller_type
programmer_type_part = " -c" + programmer
port_part = " -P" + port_path
baud_rate_part = " -b" + baud_rate
D_part = " -D"
upload_part = " -U" + method + ":" + operation + ":" + hex_path + ":i"
'''


#command = "avrdude" + Conf_path_part + v_part + microcontroller_part + programmer_type_part + port_part + baud_rate_part + D_part + upload_part



def update(port_path=port_path,hex_path=hex_path,microcontroller_type=microcontroller_type,programmer=programmer,baud_rate=baud_rate,method=method,operation=operation,conf_path=conf_path):

    Conf_path_part = " -C" + conf_path
    v_part = " -v"
    microcontroller_part = " -p" + microcontroller_type
    programmer_type_part = " -c" + programmer
    port_part = " -P" + port_path
    baud_rate_part = " -b" + baud_rate
    D_part = " -D"
    upload_part = " -U" + method + ":" + operation + ":" + hex_path + ":i"

    command = "avrdude" + Conf_path_part + v_part + microcontroller_part + programmer_type_part + port_part + baud_rate_part + D_part + upload_part

    print(command)
    #os.system(command)


def update_v2(mcu_type,port_path=port_path):

    conf_path = "/home/pi/MAPS6.0/firmware/avrdude.conf"
    port_path = "/dev/ttyS0"
    baud_rate = "115200"
    method = "flash"
    operation = "w"
    hex_path = "/home/pi/MAPS6.0/firmware/MAPS6_MCU_with_oled.ino.with_bootloader.mega.hex"

    if(mcu_type=="mega"):
        microcontroller_type = "atmega2560"
        programmer = "wiring"

    elif(mcu_type=="uno"):
        microcontroller_type = "atmega328p"
        programmer = "arduino"

    else:
        print("ERROR Board")
        return


    Conf_path_part = " -C" + conf_path
    v_part = " -v"
    microcontroller_part = " -p" + microcontroller_type
    programmer_type_part = " -c" + programmer
    port_part = " -P" + port_path
    baud_rate_part = " -b" + baud_rate
    D_part = " -D"
    upload_part = " -U" + method + ":" + operation + ":" + hex_path + ":i"

    command = "avrdude" + Conf_path_part + v_part + microcontroller_part + programmer_type_part + port_part + baud_rate_part + D_part + upload_part

    #print(command)
    os.system(command)
