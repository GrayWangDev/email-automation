import os
import re
import csv
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

RAW_CUSTOMERS_FILE = os.getenv("RAW_CUSTOMERS_FILE", "data/customers.csv")
FILTERED_SUBSCRIBERS_FILE = os.getenv("FILTERED_SUBSCRIBERS_FILE", "data/subscribed_only.csv")

EMAIL_COLUMN = os.getenv("EMAIL_COLUMN", "邮箱")
SUBSCRIBE_COLUMN = os.getenv("SUBSCRIBE_COLUMN", "订阅状态")
SUBSCRIBED_VALUE = os.getenv("SUBSCRIBED_VALUE", "已订阅")


def is_valid_email(email):
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(email_pattern, email) is not None


def filter_subscribers():
    output_path = Path(FILTERED_SUBSCRIBERS_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    seen_emails = set()
    total_rows = 0
    subscribed_count = 0
    skipped_empty_email = 0
    skipped_invalid_email = 0
    skipped_duplicate = 0
    skipped_not_subscribed = 0

    with open(RAW_CUSTOMERS_FILE, mode="r", newline="", encoding="utf-8-sig") as infile, \
         open(FILTERED_SUBSCRIBERS_FILE, mode="w", newline="", encoding="utf-8-sig") as outfile:

        reader = csv.DictReader(infile)

        if EMAIL_COLUMN not in reader.fieldnames:
            raise ValueError(f"Missing email column: {EMAIL_COLUMN}")

        if SUBSCRIBE_COLUMN not in reader.fieldnames:
            raise ValueError(f"Missing subscribe column: {SUBSCRIBE_COLUMN}")

        writer = csv.DictWriter(outfile, fieldnames=["email", "subscribed"])
        writer.writeheader()

        for row in reader:
            total_rows += 1

            email = row.get(EMAIL_COLUMN, "").strip().lower()
            subscribe_status = row.get(SUBSCRIBE_COLUMN, "").strip()

            if subscribe_status != SUBSCRIBED_VALUE:
                skipped_not_subscribed += 1
                continue

            if not email:
                skipped_empty_email += 1
                continue

            if not is_valid_email(email):
                skipped_invalid_email += 1
                continue

            if email in seen_emails:
                skipped_duplicate += 1
                continue

            seen_emails.add(email)

            writer.writerow({
                "email": email,
                "subscribed": "true"
            })

            subscribed_count += 1

    print("Filter subscribers finished.")
    print("-" * 50)
    print(f"Input file: {RAW_CUSTOMERS_FILE}")
    print(f"Output file: {FILTERED_SUBSCRIBERS_FILE}")
    print(f"Total rows: {total_rows}")
    print(f"Subscribed users exported: {subscribed_count}")
    print(f"Skipped not subscribed: {skipped_not_subscribed}")
    print(f"Skipped empty email: {skipped_empty_email}")
    print(f"Skipped invalid email: {skipped_invalid_email}")
    print(f"Skipped duplicate: {skipped_duplicate}")


if __name__ == "__main__":
    filter_subscribers()