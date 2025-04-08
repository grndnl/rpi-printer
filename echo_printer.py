import time
import serial
from Adafruit_Thermal import Adafruit_Thermal

def main():
    # Set up the serial connection to the printer
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

    printer.boldOn()
    printer.println("Message:")
    printer.boldOff()
    printer.feed(2)

    print("Type your message. Type 'exit' to quit.\n")
    
    while True:
        try:
            message = input("Message: ")
            if message.lower() == "exit":
                printer.println("End Message.")
                printer.feed(2)
                break

            printer.println(message)
            printer.feed(1)
        except KeyboardInterrupt:
            printer.println("Message Interrupted.")
            printer.feed(2)
            break

if __name__ == "__main__":
    main()
