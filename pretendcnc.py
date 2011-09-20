import serial, sys, time
try:
    from colorama import Fore, Style, init
    colorama = True
except:
    colorama = False
    sys.stdout.write("[no colorama module]\n")

def DualWrite(*args):
    ser.write(args[0].encode('utf-8'))
    first_printable1 = args[0].replace("\r", ":")
    first_printable2 = first_printable1.replace("\n", ":")
    try:
        second = args[1]
        pass
    except:
        second = "->"
        pass
    try:
        color = args[2]
        pass
    except:
        try:
            color = Fore.BLUE
        except:
            pass
        pass
    if(colorama):
        sys.stdout.write(color+"  "+second+Fore.RED+"  "+first_printable2+"\n")
    else:
        sys.stdout.write("  "+second+"  "+first_printable2+"\n")
    return ""

def YellowTerm(text):
    if(colorama):
        sys.stdout.write(Style.BRIGHT+Fore.YELLOW)
    sys.stdout.write("\t"+text)
    return ""

def SerialSetup():
    ser = serial.Serial('COM11',9600,8,'N',1,0.01)
    return ser

def DumpSettings():
    DualWrite("$0 =  493.00 (steps/mm x)\r\n")
    DualWrite("$1 =  493.00 (steps/mm y)\r\n")
    DualWrite("$2 =  493.00 (steps/mm z)\r\n")
    DualWrite("$3 =  15 (microseconds step pulse)\r\n")
    DualWrite("$4 =  480.0 (mm/min default feed rate)\r\n")
    DualWrite("$5 =  600.0 (mm/min default seek rate)\r\n")
    DualWrite("$6 =  0.1 (mm/arc segment)\r\n")
    DualWrite("$7 =  11 (step port invert mask. binary = 3)\r\n")
    DualWrite("$8 =  1 (acceleration in mm/sec^2)\r\n")
    DualWrite("$9 =  50.0 (max instant cornering speed change in delta mm/min)\r\n")
    DualWrite("\r\n\'$x=value\' to set parameter or just \'$\' to dump current settings\r\n")
    return ""
    
def processline(line):
    if('G01' in line):
        if(colorama):
            DualWrite("ok\n\r","Sent OK signal, G01 was detected",Fore.BLUE)
        else:
            DualWrite("ok\n\r","Sent OK signal, G01 was detected")
    else:
        if(colorama):
            DualWrite("ok,"+line+"\n\r","Sent OK signal",Fore.YELLOW)
        else:
            DualWrite("ok,"+line+"\n\r","Sent OK signal")
                    
def processchunk():
    popped = []
    while ("\n" in currentline) or ("\r" in currentline):
            #currentlinestr = "".join(popped)
        currentpop = currentline.pop(0)
        popped.extend(currentpop)
    else:
        if(popped):
            processline("".join(popped))
            popped = []
        

if(colorama):
    init()
ser = SerialSetup()


YellowTerm("pretendcnc.py, hackmelbourne CNC simulator.\n\n")
#raw_input("Press Enter to start simulation.")
DualWrite("\n\rGrbl 0.6b\n\r","Sent Grbl version.")
time.sleep(0.5)
DumpSettings()
currentline = []
while True:  
    processchunk()
    #time.sleep(0.5)
    chunked = ser.readline()
    if(chunked):
        currentline.extend(list(chunked.decode('utf-8')))