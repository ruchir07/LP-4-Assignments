# A person on a nearby road is trying to enter a WiFi network by trying to crack the
# Password to use the IP Printer resource; write a program to detect such an attempt
# and prohibit the access. Develop the necessary scenario by Using an IEEE 802.11,
# configure a Wi-Fi adapter and Access Point.


from collections import defaultdict
from datetime import datetime
import csv

MAX_FAILURES = 3
LOG_FILE = "wifi_logs.csv"


def detect_attacks():
    failed_attempts = defaultdict(int)
    blocked_devices = set()

    try:
        with open(LOG_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            print("===== WI-FI SECURITY MONITOR =====")

            for row in reader:
                mac = row["mac"].strip().upper()
                status = row["status"].strip().upper()

                if status == "FAIL":
                    failed_attempts[mac] += 1

                    print(
                        f"Failed login: {mac} | "
                        f"Count: {failed_attempts[mac]}"
                    )

                    if failed_attempts[mac] >= MAX_FAILURES:
                        blocked_devices.add(mac)

                elif status == "SUCCESS":
                    print(f"Successful login: {mac}")

        print("\n===== SECURITY REPORT =====")

        if blocked_devices:
            for mac in sorted(blocked_devices):
                print(
                    f"ALERT: {mac} exceeded the failure limit."
                )
                print(f"Action: Add {mac} to the blocklist.")

            with open("blocked_devices.txt", "w") as file:
                for mac in sorted(blocked_devices):
                    file.write(mac + "\n")

            print("\nBlocklist saved to blocked_devices.txt")
            print("Apply the blocklist through the access point.")
        else:
            print("No device exceeded the failure threshold.")

    except FileNotFoundError:
        print(f"Error: {LOG_FILE} was not found.")
    except (KeyError, csv.Error) as error:
        print("Invalid log file:", error)


if __name__ == "__main__":
    detect_attacks()