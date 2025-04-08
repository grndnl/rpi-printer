import time
import requests
from bs4 import BeautifulSoup
from Adafruit_Thermal import Adafruit_Thermal
from datetime import datetime

ROAD_URL = "https://roads.dot.ca.gov/roadscell.php?roadnumber=50"
CHECK_INTERVAL = 15 * 60  # 15 minutes

def fetch_road_conditions():
    try:
        response = requests.get(ROAD_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        pre_tag = soup.find('pre')
        return pre_tag.text.strip() if pre_tag else "No data found."
    except Exception as e:
        return f"Error fetching road data: {e}"

def print_road_conditions(printer, message):
    printer.feed(1)
    printer.boldOn()
    printer.println(f"Hwy 50 Road Report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
    printer.boldOff()
    printer.feed(1)

    for line in message.splitlines():
        printer.println(line)

    printer.feed(3)

def main():
    printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
    print("Starting Road Watcher...")

    last_message = None

    while True:
        print("Checking road conditions...")
        conditions = fetch_road_conditions()

        if conditions != last_message:
            print("New information. Printing...")
            print_road_conditions(printer, conditions)
            last_message = conditions
        else:
            print("No change. Skipping print.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
