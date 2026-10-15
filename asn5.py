import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

LOG_FILE = "security_logs.csv"
ALERT_FILE = "security_alerts.txt"

THRESHOLD = 3
WINDOW_MINUTES = 5


def analyze_logs():
    events = defaultdict(list)
    alerts = []

    if not Path(LOG_FILE).exists():
        print("Error: security_logs.csv not found.")
        return

    # Read and group failed login events by IP address
    with open(LOG_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                timestamp = datetime.strptime(
                    row["timestamp"].strip(),
                    "%Y-%m-%d %H:%M:%S"
                )
                ip = row["ip"].strip()
                event = row["event"].strip().upper()
                status = row["status"].strip().upper()

                if event == "LOGIN" and status == "FAIL":
                    events[ip].append(timestamp)

            except (ValueError, KeyError) as error:
                print("Skipping invalid log entry:", error)

    # Correlate events within a time window
    for ip, timestamps in events.items():
        timestamps.sort()

        for i in range(len(timestamps)):
            window_end = timestamps[i] + timedelta(
                minutes=WINDOW_MINUTES
            )

            count = sum(
                1 for time in timestamps
                if timestamps[i] <= time <= window_end
            )

            if count >= THRESHOLD:
                alert = (
                    f"ALERT: {count} failed logins from {ip} "
                    f"within {WINDOW_MINUTES} minutes, "
                    f"starting at {timestamps[i]}"
                )

                alerts.append(alert)
                break

    # Display and save results
    print("===== LOG CORRELATION REPORT =====")

    if alerts:
        for alert in alerts:
            print(alert)

        Path(ALERT_FILE).write_text(
            "\n".join(alerts) + "\n",
            encoding="utf-8"
        )

        print("\nAlerts saved to", ALERT_FILE)
    else:
        print("No suspicious login pattern detected.")

        Path(ALERT_FILE).write_text(
            "No suspicious login pattern detected.\n",
            encoding="utf-8"
        )


if __name__ == "__main__":
    analyze_logs()