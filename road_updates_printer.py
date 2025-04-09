import time
import requests
from bs4 import BeautifulSoup
from Adafruit_Thermal import Adafruit_Thermal

ROAD_URL = "https://roads.dot.ca.gov/roadscell.php?roadnumber=50"
CHECK_INTERVAL = 15 * 60  # 15 minutes

def fetch_road_conditions():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(ROAD_URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        middle_div = soup.find("div", id="middle_column")

        if not middle_div:
            return "Could not find road data section."

        full_text = middle_div.get_text(separator="\n").strip()

        # Only keep content starting from the "This highway information..." line
        marker = "This highway information"
        start_index = full_text.find(marker)
        if start_index == -1:
            return "Could not find road condition start."

        trimmed_text = full_text[start_index:]

        # Clean up: collapse multiple newlines into a single one
        import re
        clean_text = re.sub(r'\n+', '\n', trimmed_text)

        return f"{clean_text}"

    except Exception as e:
        return f"Error fetching road data: {e}"


def print_road_conditions(printer, message):
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

        if conditions[98:] != last_message[98:]:
            print(f"**New information. Printing...**\n{conditions}")
            print_road_conditions(printer, conditions)
            last_message = conditions
        else:
            print("No change. Skipping print.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
