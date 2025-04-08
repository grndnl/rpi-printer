import time
import serial
from Adafruit_Thermal import Adafruit_Thermal

def main():
    # Set up the serial connection to the printer
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

    printer.boldOn()
    printer.println("Thermal Printer Ready!")
    printer.boldOff()
    printer.feed(1)

    print("Type your message. Type 'exit' to quit.\n")
    
    while True:
        try:
            message = input("You: ")
            if message.lower() == "exit":
                printer.println("Goodbye!")
                printer.feed(2)
                break

            printer.println(message)
            printer.feed(1)
        except KeyboardInterrupt:
            printer.println("Interrupted. Bye!")
            printer.feed(2)
            break

if __name__ == "__main__":
    main()
