import serial

#port = "/dev/ttyACM0"
port = "/dev/ttyS0"


s1 = serial.Serial(port,9600)
#s1.flush()


def get():

    #s1 = serial.Serial(port,9600)
    s1.reset_input_buffer()
    #s1.reset_output_buffer()
    #s1.flushInput()
    s1.flush()

    inputValue = s1.readline().decode('ascii').strip()

    if (inputValue.find("Temp=") == -1):
        #get()
        s1.flush()
        inputValue = s1.readline().decode('ascii').strip()
    #print(inputValue)

    return inputValue


def get_c():

    s1.reset_input_buffer()
    s1.flush()

    inputValue = s1.readline().decode('ascii').split(',')

    for i in range(len(inputValue)):
        item = inputValue[i].split('=')
        print (item[1])

