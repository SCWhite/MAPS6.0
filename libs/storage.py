import os


#values = []

def storage(path):

    #CSV_items =  ['device_id', 'date', 'time', 'Tmp',  'RH',   'PM2.5','PM10', 'PM1.0','RGB_R','RGB_G','RGB_B','RGB_C','Lux',  'CO2',  'TVOC']
    #CSV_type  =  ['string',    'date', 'time', 'float','float','int',  'int',  'int',  'int',  'int'  ,'int',  'int',  'int',  'int',  'int' ]
    #CSV_items  =  ['device_id', 'date', 'time', 's_t0', 's_h0', 's_d0', 's_d1', 's_d2', 's_lr', 's_lg', 's_lb', 's_lc', 's_l0', 's_gh', 's_gg']
    #values["date"] = "OKOKOKOKOKOKOK"
    name = "OKOKOKOKOOK"
    CSV_msg = "1,ADDISON AV,Celtis australis,Large Tree Routine Prune,10/18/2010"

    #CSV_msg = ""
    #for item in CSV_items:
    #    if item in values:
    #        CSV_msg = CSV_msg + str(values[item]) + ','
    #    else:
    #        CSV_msg = CSV_msg + "N/A" + ','
    #CSV_msg= CSV_msg[:-1] #to get rid  of ',' from last data

    #print(COLOR_PURPLE + "CSV_MSG:" + COLOR_REST)
    #color.print_p("CSV_MSG:")
    print(CSV_msg)

    #remember to add USB drive storage!!
    with open(path + "/" + name + ".csv", "a") as f:
        #f.write(msg_headers + "\n")
        f.write(CSV_msg + "\n")
        f.write(CSV_msg + "\n")
        f.write(CSV_msg + "\n")
        f.write(CSV_msg + "\n")
        f.write(CSV_msg + "\n")



if len(os.listdir("/media/pi")):
    print("OK")

    path = "/media/pi/" + os.listdir("/media/pi")[0]
    print(path)

    storage(path)

else:
    print("NO!!")

