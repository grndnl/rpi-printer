import time
import requests
from bs4 import BeautifulSoup
from Adafruit_Thermal import Adafruit_Thermal
from datetime import datetime

ROAD_URL = "https://roads.dot.ca.gov/roadscell.php?roadnumber=50"
CHECK_INTERVAL = 15 * 60  # 15 minutes

def fetch_road_conditions():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        }
        response = requests.get(ROAD_URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        middle_div = soup.find("div", id="middle_column")

        if not middle_div:
            return "Could not find road data section."

        # Clean all the tags and join the visible text
        road_text = middle_div.get_text(separator="\n").strip()
        return road_text

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
