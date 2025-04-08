import qrcode
from PIL import Image
import serial
import time
from Adafruit_Thermal import Adafruit_Thermal

# Configuration
EMAIL = "mailto:1961mewuk@gmail.com"
QR_BOX_SIZE = 10  # Increase size for better print quality
PRINTER_PORT = "/dev/serial0"
BAUD_RATE = 19200

# Create QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=QR_BOX_SIZE,
    border=4,
)
qr.add_data(EMAIL)
qr.make(fit=True)

# Generate image and convert to 1-bit bitmap
qr_img = qr.make_image(fill_color="black", back_color="white").convert('1')

# Save image if you want to debug
qr_img.save("qr_email.bmp")

# Initialize printer
printer = Adafruit_Thermal(serial.Serial(PRINTER_PORT, BAUD_RATE, timeout=5))

# Optional: Feed and center
printer.feed(1)
printer.justify('C')

# Print the image
printer.printImage(qr_img, True)

# Optional: Add label below
printer.feed(1)
printer.println("Scan to Email")
printer.feed(3)
