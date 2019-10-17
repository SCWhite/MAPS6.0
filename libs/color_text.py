#set up color code
ESCAPE      = "\033["
COLOR_REST  = "\033[0m"
END         = "m"

#color code
COLOR_BLCAK = 30
COLOR_RED   = 31
COLOR_GREEN = 32
COLOR_YELLO = 33
COLOR_BLUE  = 34
COLOR_PURPLE= 35
COLOR_CYAN  = 36
COLOR_WHITE = 37

#style code
NOEFFECT    = 0
BOLD        = 1
Negative1   = 3
UNDERLINE   = 4
Negative2   = 5
THROUGH     = 9


#notice "B" for black/ "b" for blue
color_dict = {
    "B" : COLOR_BLCAK,
    "r" : COLOR_RED,
    "g" : COLOR_GREEN,
    "y" : COLOR_YELLO,
    "b" : COLOR_BLUE,
    "p" : COLOR_PURPLE,
    "c" : COLOR_CYAN,
    "w" : COLOR_WHITE
}

style_dict = {
    "no": NOEFFECT,
    "B" : BOLD,
    "U" : UNDERLINE,
    "T" : THROUGH,
    "N1": Negative1,
    "N2": Negative2
}

def print_r(text):
    print(ESCAPE + str(COLOR_RED) + END + text + COLOR_REST)

def print_g(text):
    print(ESCAPE + str(COLOR_GREEN) + END + text + COLOR_REST)

def print_b(text):
    print(ESCAPE + str(COLOR_BLUE) + END + text + COLOR_REST)

def print_c(text):
    print(ESCAPE + str(COLOR_CYAN) + END + text + COLOR_REST)

def print_y(text):
    print(ESCAPE + str(COLOR_YELLOW) + END + text + COLOR_REST)

def print_p(text):
    print(ESCAPE + str(COLOR_PURPLE) + END + text + COLOR_REST)


def c_print(text,text_color = "g" ,style = "no" ,background = "B"):
    print(ESCAPE + str(style_dict[style]) + ";" + str(color_dict[text_color]) + ";" + str(color_dict[background]+10) + END + text + COLOR_REST)

if __name__ == '__main__':
    main()
