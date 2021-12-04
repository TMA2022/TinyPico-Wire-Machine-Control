import time
import math
import machine
from machine import Pin, Timer
from time import sleep
from time import sleep_ms, ticks_ms
from machine import SoftI2C

from i2c_lcd import I2cLcd
DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

 # CONSTANTS
KEY_UP   = const(0)
KEY_DOWN = const(1)
lastkey = ''
mynext = 0

aa = 0 #remember wires for display function
bb = 0 #remember inches for display function
wires = 1
inches = 3.5

#Designate Input Pin for Run
myinput = Pin(32, Pin.IN)
myinput.value()

keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['.', '0', '#', 'D']]

# Pin names for Pico
rows = [23, 19, 18, 5]
cols = [15, 27, 26, 25]

# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

def initNow():
    for row in range(0,4):
        for col in range(0,4):
            row_pins[row].value(0)

def scanNow(row, col):
    row_pins[row].value(1)
    key = None
    if col_pins[col].value() == KEY_DOWN:
        key = KEY_DOWN
    if col_pins[col].value() == KEY_UP:
        key = KEY_UP
        row_pins[row].value(0)
    return key
 
def getKey():
    global lastkey
    global mynext
    for row in range(4):
        for col in range(4):
            key = scanNow(row, col)
            if key == KEY_DOWN:
                #print("Key Pressed", keys[row][col])
                lastkey = keys[row][col]
                a = lastkey
                print(lastkey)
                mynext = 1
                sleep_ms(500)
                if a == 'A':
                    getWireCount()
                elif a == 'D':
                    getLength()
                else:
                    pass

def getLength():
    global lcd
    global inches
    global lastkey
    global mynext
    inches = 0
    a = ''
    b = ''
    c = '.'
    d = ''
    mynext = 0
    while mynext == 0: #get number one
        sleep_ms(50)
        getKey()
    a = lastkey
    sleep_ms(100)
    mynext = 0
    while mynext == 0: #get number two
        sleep_ms(50)
        getKey()
    b = lastkey
    sleep_ms(100)
    mynext = 0
    while mynext == 0: #get number three
        sleep_ms(50)
        getKey()
    d = lastkey
    sleep_ms(100)
    mynext = 0
    
    e = str(a + b + c + d) #build number 12.3 up to 99.9 Inches
    print(e)
    
    inches = float(e)
    sleep_ms(20)
    
    print('You Entered = ', inches)
    sleep_ms(200)

def getWireCount():
    global lastkey
    global wires
    wires = 0
    while lastkey == 'A':
        sleep_ms(100)
        print(lastkey)
        getKey()  
    if lastkey == '1':
        wires = 1
        print('Wire Count = ', wires)
    if lastkey == '2':
        wires = 2
        print('Wire Count = ', wires)
    if lastkey == '3':
        wires = 3
        print('Wire Count = ', wires)
    if lastkey == '4':
        wires = 4
        print('Wire Count = ', wires)
    if lastkey == '5':
        wires = 20
        print('Wire Count = ', wires)
    sleep_ms(100)
        
def setDisplay():
    global aa
    global wires
    global bb
    global inches
    
    if wires != aa or inches != bb:
        aa = wires
        bb = inches
        lcd.clear()    
        lcd.move_to(5, 0)
        lcd.putstr("Wire Count")
        lcd.move_to(7, 1)
        lcd.putstr("Inches")
        lcd.move_to(0, 0)
        lcd.putstr(str(aa))
        lcd.move_to(0,1)
        lcd.putstr(str(bb))
       

def checkinput():
    myinput = Pin(32, Pin.IN)
    m = myinput.value()
    if m != 0:
        runNow()
    else:
        pass

def runNow():
    rev = Pin(14, Pin.OUT)
    w = 0
    while w < wires:
        moveNow() #Feed Wire
        time.sleep(.1)
        moveNow2() #Cutter Simulation / Same motor for now
        time.sleep(.1)
        rev.on()
        moveNow2()
        rev.off()
        w = w + 1
        sleep_ms(500)



def moveNow():
    global inches
    step = Pin(4, Pin.OUT)
    mypwm = 1000  # starting pwm / start speed
    minpulse = 150  # min pwm or max speed
    rate = 10 #accel decel rate
    dest = 541 * inches  # destination 720/REVOLUTION
    x = 1
    decel = 21
    decelbegin = 0
    on = step.on
    off = step.off
    count = 1
    cnt = 1
    while x < dest:
        time.sleep_us(mypwm)
        #print(x, mypwm)
        x = x + 1
        if mypwm <= minpulse:
            if count != 0:
                decelbegin = x + 1
                decel = dest - decelbegin  # decel from here on
                count = 0
        on()
        time.sleep_us(mypwm)
        off()
        if x >= decel + 1:
            if count != 0:
                mypwm = mypwm - rate
            else:
                mypwm = mypwm + rate
                            
        elif x >= dest - decelbegin:
            cnt = 0 #Block and Control Function above
            
def moveNow2():
    inches = .45
    step = Pin(4, Pin.OUT)
    mypwm = 1000  # starting pwm / start speed
    minpulse = 150  # min pwm or max speed
    rate = 10 #accel decel rate
    dest = 540 * inches  # destination 720/REVOLUTION
    x = 1
    decel = 21
    decelbegin = 0
    on = step.on
    off = step.off
    count = 1
    count2 = 1
    while x < dest:
        time.sleep_us(mypwm)
        #print(x, mypwm)
        x = x + 1
        if mypwm <= minpulse:
            if count != 0:
                decelbegin = x + 1
                decel = dest - decelbegin  # decel from here on
                count = 0
        on()
        time.sleep_us(mypwm)
        off()
        if x >= decel + 1:
            if count != 0:
                mypwm = mypwm - rate
            else:
                mypwm = mypwm + rate
                            
        elif x >= dest - decelbegin:
            count2 = 0 #Block and Control Function above

print('Starting KeyPad!')
initNow() #KeyPad

while True:
    getKey()
    checkinput()
    setDisplay()
    time.sleep_ms(200)