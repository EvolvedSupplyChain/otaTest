#logger/camera script
import machine
import time
#test test test
def main():
    print("Attempt number 1")
    led = machine.Pin(25, machine.Pin.OUT)
    led.on()


    while True:
        time.sleep(1)
        led.toggle()
