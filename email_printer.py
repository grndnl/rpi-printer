import configparser
import os
import time
import imaplib
import email
from email.header import decode_header
from Adafruit_Thermal import Adafruit_Thermal

# Load email credentials from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

EMAIL = config.get("EMAIL", "address")
PASSWORD = config.get("EMAIL", "password")

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# Printer setup
printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)

def connect_to_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    return mail

def clean(text):
    return ''.join(c if c.isprintable() else '?' for c in text)

def check_and_print_emails():
    mail = connect_to_gmail()
    mail.select("inbox")

    # Search for unread messages
    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()

    if not email_ids:
        print("No new emails.")
        return

    for num in email_ids:
        status, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                subject = clean(subject)

                from_, encoding = decode_header(msg.get("From"))[0]
                if isinstance(from_, bytes):
                    from_ = from_.decode(encoding if encoding else "utf-8")
                from_ = clean(from_)

                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                body = clean(body.strip().replace("\r", "").replace("\n", " "))[:200]

                # Print to thermal printer
                printer.feed(1)
                printer.boldOn()
                printer.println("New Email!")
                printer.boldOff()
                printer.println("From: " + from_)
                printer.println("Subject: " + subject)
                printer.println("Body: " + body)
                printer.feed(2)

    mail.logout()

def loop_check_emails(interval_minutes=30):
    while True:
        try:
            print("Checking for new emails...")
            check_and_print_emails()
            print("Done. Sleeping for {} minutes...".format(interval_minutes))
            time.sleep(interval_minutes * 60)
        except Exception as e:
            printer.println("Error occurred: {}".format(str(e)))
            printer.feed(1)
            print("Error:", e)
            time.sleep(60)  # wait a minute before retrying

if __name__ == "__main__":
    loop_check_emails()