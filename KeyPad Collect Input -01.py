#Jeff Redington: True Machine Automation: 12/3/2021
#Showing how I was able to take the KEYPAD! input and make it usable for wire count and inches as a float

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
 
def getLength():
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

def getWireCount(): #Lets make wires 1, 2, 3, 4, or 20 at a time.
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