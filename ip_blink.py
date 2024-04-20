import subprocess
import time
import sys

sys.stdout = open("/home/pi/log.txt", "a")
sys.stderr = open("/home/pi/error.txt", "a")

sys.stdout.write("########## STARTING ##########\n")
sys.stderr.write("########## STARTING ##########\n")

dot = 0
dash = 0
bc = 0
bl = 0

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}

class LED:
    def __init__(self, file):
        self.file = file
        self.handle = open(self.file+"/brightness", "w")
        with open(self.file+"/trigger", "w") as f:
            f.write("gpio")


    def on(self):
        self.handle.truncate(0)
        self.handle.write("1")
        self.handle.flush()

    def off(self):
        self.handle.truncate(0)
        self.handle.write("0")
        self.handle.flush()

    def cleanup(self):
        print("Closing", self.handle)
#        list(map(lambda x: print(x, getattr(self.handle, x)), dir(self.handle)))
        self.handle.close()    


    def morse(self, s, dot, dash, between_char, between_letter):
        for idx, char in enumerate(s):
            char = MORSE_CODE_DICT[char]
            for i, x in enumerate(char):
                self.on()
                time.sleep(dash if x=="-" else dot)
                self.off()
                if i == len(char)-1 and idx != len(s)-1:
                    time.sleep(between_letter)
                else: time.sleep(between_char)

    def count(self, n, start, val, pause, between):
        for i, x in enumerate(n):
            self.on()
            time.sleep(start)
            self.off()
            for y in range(x):
                time.sleep(pause)
                self.on()
                time.sleep(val)
                self.off()
            time.sleep(between)
            

if __name__ == "__main__":
    green = LED("/sys/class/leds/led0")
    time.sleep(10)
    ip = subprocess.check_output(["hostname", "-I"]).decode().split(" ")[0]
    print("Received", ip)
    ip = ip.strip("\n").strip(" ").split(".")
    ip = [[int(digit) for digit in part] for part in ip]
    print(ip)
    #green.count([1, 2, 3], 0.7, 0.3, 0.3, 1)
    try:
        while True:
            for x in ip:
                green.count(x, 1, 0.3, 0.3, 1)
                time.sleep(2)
            time.sleep(10)
    finally:
        green.cleanup()

