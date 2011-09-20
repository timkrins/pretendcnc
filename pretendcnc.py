import serial, sys, time
from colorama import Fore, Style, init

def DualWrite(*args):
    time.sleep(0.05)
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
        color = Fore.BLUE
        pass
    sys.stdout.write(color+"  "+second+Fore.RED+"  "+first_printable2+"\n")
    return ""

def YellowTerm(text):
    sys.stdout.write(Style.BRIGHT+Fore.YELLOW+"\t"+text)
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
    DualWrite("$9 =  50.0 (max instant cornering speed change in delta mm/min)\r\n\r\n")
    DualWrite("'$x=value\' to set parameter or just \'$\' to dump current settings\r\n")
    return ""
    
def processline(line):
    if('G01' in line):
        DualWrite("ok\n\r","Sent OK signal, G01 was detected",Fore.BLUE)
    elif('G00' in line):
        DualWrite("ok\n\r","Sent OK signal, G00 was detected",Fore.BLUE)
    elif('X' in line):
        DualWrite("ok\n\r","Sent OK signal, X was detected",Fore.BLUE)
    elif('Y' in line):
        DualWrite("ok\n\r","Sent OK signal, Y was detected",Fore.BLUE)
    elif('Z' in line):
        DualWrite("ok\n\r","Sent OK signal, Z was detected",Fore.BLUE)
    elif(line == "$"):
        DumpSettings()
    else:
        DualWrite("Could not determine command, \""+line+"\"\n\r","ERROR ->", Fore.YELLOW)
    return ""
                    
def processchunk():
    popped = []
    while ("\n" in currentline) or ("\r" in currentline):
        #currentlinestr = "".join(popped)
        currentpop = currentline.pop(0)
        popped.extend(currentpop)
    else:
        if(popped):
            popped.pop()
            processline("".join(popped))
            popped = []
    return ""
   
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
    chunked = ser.readline()
    if(chunked):
        currentline.extend(list(chunked.decode('utf-8').upper()))