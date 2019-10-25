import get_serial as mcu
import time


str_a = ""

while True:
    str_a = mcu.get()

    print(str_a)
    time.sleep(1)
