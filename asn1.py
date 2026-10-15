from email import policy
from email.parser import Parser
from email.utils import parseaddr
from pathlib import Path


def analyze_email_header(filename):
    try:
        # Read the email header from a text file
        raw_header = Path(filename).read_text(
            encoding="utf-8",
            errors="replace"
        )

        # Parse the header
        msg = Parser(policy=policy.default).parsestr(raw_header)

        print("\n===== EMAIL HEADER ANALYSIS =====")

        # Display important header fields
        print("From:", msg.get("From", "Not available"))
        print("To:", msg.get("To", "Not available"))
        print("Subject:", msg.get("Subject", "Not available"))
        print("Date:", msg.get("Date", "Not available"))
        print("Return-Path:", msg.get("Return-Path", "Not available"))

        # Display Received records
        print("\n--- Received Server Records ---")
        received = msg.get_all("Received", [])

        if received:
            for number, record in enumerate(received, start=1):
                print(f"{number}. {record}")
        else:
            print("No Received records found.")

        # Display email authentication results
        print("\n--- Email Authentication ---")
        auth_results = msg.get_all("Authentication-Results", [])
        auth_results += msg.get_all("Received-SPF", [])

        if auth_results:
            for result in auth_results:
                print(result)
        else:
            print("No authentication results found.")

        # Check for possible warning signs
        print("\n--- Potential Warning Signs ---")
        warnings = []

        sender = parseaddr(msg.get("From", ""))[1]
        return_path = parseaddr(msg.get("Return-Path", ""))[1]

        if not sender:
            warnings.append("Sender address is missing.")

        if sender and return_path:
            sender_domain = sender.rsplit("@", 1)[-1].lower()
            return_domain = return_path.rsplit("@", 1)[-1].lower()

            if sender_domain != return_domain:
                warnings.append(
                    "From and Return-Path domains differ; investigate."
                )

        for result in auth_results:
            result_text = str(result).lower()

            if any(check in result_text for check in
                   ["spf=fail", "dkim=fail", "dmarc=fail"]):
                warnings.append(
                    "An email authentication failure was reported."
                )
                break

        if not received:
            warnings.append(
                "No Received records found; the header may be incomplete."
            )

        if warnings:
            for warning in warnings:
                print("WARNING:", warning)
        else:
            print("No obvious warning signs detected.")

        print("\nNote: Header analysis alone cannot prove an email is safe.")

    except FileNotFoundError:
        print(f"Error: {filename} was not found.")
    except Exception as error:
        print("Error analyzing header:", error)


if __name__ == "__main__":
    analyze_email_header("email_header.txt")