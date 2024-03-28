import machine
import time

def log_data():
    print("Attempt number 1")
    led = machine.Pin('LED', machine.Pin.OUT)
        
    while True:
        try:
            led.toggle()
        except Exception as error:
            print(error)
            
        print("5555")
        time.sleep(1)
    
    return

