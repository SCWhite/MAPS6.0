import os

def check_time():
    print("TIME")
    #TO DO

def check_new_version():
    print("VERSION")
    #TO DO
    #check git version?

def check_serial():
    print("serial_port")
    #TO DO
    #check for ttyACM0 (but we are changing to PI GPIO)

def check_connection():
    #print("check_connection")
    #os.system return 0 for "OK" / 1 for "error"
    #check_connection return 0 for "no connection" / 2 for "google ok" / 1 for "our server ok"
    #might cause process blocking (because PING)

    if(os.system("ping data.lass-net.org -q -c 1  > /dev/null") == 0):
        return 1
    elif(os.system('ping www.google.com -q -c 1  > /dev/null') == 0):
        return 2
    else:
        return 0


def check_flash_drive():
    #print("check_flash_drive")
    #return 0 if there is "NO flash drive" / 1 for "1 flash drive" / 2 for "more then 1 flash drive"
    if (len(os.listdir("/media/pi")) == 0):
        return 0
    elif (len(os.listdir("/media/pi")) == 1):
        return 1
    else:
        return 2


