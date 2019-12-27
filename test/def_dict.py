'''
values["device_id"] = "AAAAAABBBBBB"
values["ver_app"] = "6.0.0"
values["date"] = "2019-12-08"
values["time"] = "09:30:50"
values["tick"] = "5551"
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



values = {      "app"           :       "abc",
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
                "CO2"           :       s_gh,
                "TVOC"          :       s_gg,
        }


values["device_id"] = "AAAAAABBBBBB"
values["ver_app"] = "6.0.0"
values["date"] = "2019-12-08"
values["time"] = "09:30:50"
values["tick"] = "5551"
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
'''

dict = {'qwea': 1,
        'b': 2,
        'c': 'qweqws3'
}

def check(values):
    print(values)


print("start")
check(dict)
print("OK")
