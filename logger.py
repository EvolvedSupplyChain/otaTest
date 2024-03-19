#logger/camera script
import machine
import time

led = machine.Pin(25, Pin.OUT)
led.on()
while True:
    time.sleep(1)
    led.toggle()