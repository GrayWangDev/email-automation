import os
import re
import json
import csv
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

SUBSCRIBERS_FILE = os.getenv("SUBSCRIBERS_FILE", "data/subscribed_only.csv")
CAMPAIGN_FILE = os.getenv("CAMPAIGN_FILE", "campaigns/spring_sale_2026/campaign.json")
HTML_FILE = os.getenv("HTML_FILE", "output/preview.html")
LOG_FILE = os.getenv("LOG_FILE", "output/send_log.csv")
HISTORY_FILE = os.getenv("HISTORY_FILE", "output/campaign_history.csv")
RECIPIENT_HISTORY_FILE = os.getenv("RECIPIENT_HISTORY_FILE", "output/recipient_history.csv")
SUPPRESS_PREVIOUS_SENDS = os.getenv("SUPPRESS_PREVIOUS_SENDS", "true").strip().lower() == "true"

DRY_RUN = os.getenv("DRY_RUN", "true").strip().lower() == "true"
MAX_SEND_LIMIT = int(os.getenv("MAX_SEND_LIMIT", "3"))
SEND_DELAY_SECONDS = int(os.getenv("SEND_DELAY_SECONDS", "2"))


def check_env():
    required_values = {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USERNAME": SMTP_USERNAME,
        "SMTP_PASSWORD": SMTP_PASSWORD,
        "FROM_EMAIL": FROM_EMAIL
    }

    missing = []

    for key, value in required_values.items():
        if not value:
            missing.append(key)

    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")


def read_html_file(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()

def load_campaign(campaign_file):
    with open(campaign_file, mode="r", encoding="utf-8") as file:
        return json.load(file)


def get_campaign_name(campaign):
    campaign_name = campaign.get("campaign_name", "").strip()

    if campaign_name:
        return campaign_name

    return Path(CAMPAIGN_FILE).parent.name or Path(CAMPAIGN_FILE).stem

def is_valid_email(email):
    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(email_pattern, email) is not None

def load_subscribers(file_path):
    subscribers = []
    seen_emails = set()

    with open(file_path, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            email = row.get("email", "").strip().lower()
            subscribed = row.get("subscribed", "").strip().lower()

            if not email:
                continue

            if subscribed != "true":
                continue

            if not is_valid_email(email):
                print(f"Skipped invalid email: {email}")
                write_log(email, "skipped_invalid_email")
                continue

            if email in seen_emails:
                print(f"Skipped duplicate email: {email}")
                write_log(email, "skipped_duplicate")
                continue

            seen_emails.add(email)
            subscribers.append(email)

    return subscribers


def create_message(to_email, subject, html_content):
    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content(
        "This email contains an HTML version. Please view it in an HTML-compatible email client."
    )
    message.add_alternative(html_content, subtype="html")

    return message

#邮件发送记录
def write_log(email, status, error_message=""):
    Path("output").mkdir(exist_ok=True)

    file_exists = Path(LOG_FILE).exists()

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        fieldnames = ["time", "email", "status", "error_message"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email": email,
            "status": status,
            "error_message": error_message
        })


def load_sent_recipient_history(campaign_name):
    sent_emails = set()
    history_path = Path(RECIPIENT_HISTORY_FILE)

    if not history_path.exists():
        return sent_emails

    with open(history_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            history_campaign_name = row.get("campaign_name", "").strip()
            status = row.get("status", "").strip().lower()
            email = row.get("email", "").strip().lower()

            if history_campaign_name == campaign_name and status == "sent" and email:
                sent_emails.add(email)

    return sent_emails


def write_recipient_history(campaign_name, subject, email, status, error_message=""):
    Path(RECIPIENT_HISTORY_FILE).parent.mkdir(parents=True, exist_ok=True)

    file_exists = Path(RECIPIENT_HISTORY_FILE).exists()

    with open(RECIPIENT_HISTORY_FILE, mode="a", newline="", encoding="utf-8") as file:
        fieldnames = ["time", "campaign_name", "campaign_file", "subject", "email", "status", "error_message"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campaign_name": campaign_name,
            "campaign_file": CAMPAIGN_FILE,
            "subject": subject,
            "email": email,
            "status": status,
            "error_message": error_message
        })


def filter_previously_sent_recipients(subscribers, campaign_name):
    if not SUPPRESS_PREVIOUS_SENDS:
        return subscribers, 0

    sent_emails = load_sent_recipient_history(campaign_name)
    filtered_subscribers = []
    skipped_count = 0

    for email in subscribers:
        if email in sent_emails:
            print(f"Skipped previously sent recipient: {email}")
            write_log(email, "skipped_previously_sent")
            skipped_count += 1
            continue

        filtered_subscribers.append(email)

    return filtered_subscribers, skipped_count
#活动记录
def write_campaign_history(
    subject,
    total_subscribers,
    processed_count,
    sent_count,
    failed_count,
    dry_run_count,
    skipped_previously_sent_count
):
    Path(HISTORY_FILE).parent.mkdir(parents=True, exist_ok=True)

    file_exists = Path(HISTORY_FILE).exists()

    with open(HISTORY_FILE, mode="a", newline="", encoding="utf-8") as file:
        fieldnames = [
            "time",
            "campaign_file",
            "subject",
            "dry_run",
            "total_subscribers",
            "processed_count",
            "sent_count",
            "failed_count",
            "dry_run_count",
            "skipped_previously_sent_count"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campaign_file": CAMPAIGN_FILE,
            "subject": subject,
            "dry_run": str(DRY_RUN).lower(),
            "total_subscribers": total_subscribers,
            "processed_count": processed_count,
            "sent_count": sent_count,
            "failed_count": failed_count,
            "dry_run_count": dry_run_count,
            "skipped_previously_sent_count": skipped_previously_sent_count
        })


#发送的二次确认，防止误操作
def confirm_before_sending(send_count, subject):
    if DRY_RUN:
        print("DRY_RUN is enabled. No real emails will be sent.")
        return True

    print("WARNING: DRY_RUN is false. Real emails will be sent.")
    print(f"Email subject: {subject}")
    print(f"Number of emails to send: {send_count}")
    print("Type SEND to confirm:")

    confirmation = input("> ").strip()

    if confirmation != "SEND":
        print("Send cancelled. No emails were sent.")
        return False

    return True

def send_bulk_emails(subscribers, html_content, subject, campaign_name):
    eligible_subscribers, skipped_previously_sent_count = filter_previously_sent_recipients(
        subscribers,
        campaign_name
    )
    send_list = eligible_subscribers[:MAX_SEND_LIMIT]

    sent_count = 0
    failed_count = 0
    dry_run_count = 0

    print(f"Total subscribed users found: {len(subscribers)}")
    print(f"Skipped previously sent for this campaign: {skipped_previously_sent_count}")
    print(f"Eligible users after history check: {len(eligible_subscribers)}")
    print(f"Safety limit enabled. Will process only: {len(send_list)} email(s)")
    print(f"DRY_RUN mode: {DRY_RUN}")
    print("-" * 50)

    if not send_list:
        print("No eligible recipients to process after history check.")
        write_campaign_history(
            subject=subject,
            total_subscribers=len(subscribers),
            processed_count=0,
            sent_count=0,
            failed_count=0,
            dry_run_count=0,
            skipped_previously_sent_count=skipped_previously_sent_count
        )
        return

    confirmed = confirm_before_sending(len(send_list), subject)

    if not confirmed:
        write_campaign_history(
            subject=subject,
            total_subscribers=len(subscribers),
            processed_count=0,
            sent_count=0,
            failed_count=0,
            dry_run_count=0,
            skipped_previously_sent_count=skipped_previously_sent_count
        )
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        for index, email in enumerate(send_list, start=1):
            try:
                message = create_message(email, subject, html_content)

                if DRY_RUN:
                    print(f"[{index}/{len(send_list)}] DRY RUN - would send to: {email}")
                    write_log(email, "dry_run")
                    dry_run_count += 1
                else:
                    server.send_message(message)
                    print(f"[{index}/{len(send_list)}] Sent to: {email}")
                    write_log(email, "sent")
                    write_recipient_history(campaign_name, subject, email, "sent")
                    sent_count += 1

                time.sleep(SEND_DELAY_SECONDS)

            except Exception as error:
                print(f"[{index}/{len(send_list)}] Failed to send to: {email}")
                print("Error:", error)
                write_log(email, "failed", str(error))
                write_recipient_history(campaign_name, subject, email, "failed", str(error))
                failed_count += 1

    write_campaign_history(
        subject=subject,
        total_subscribers=len(subscribers),
        processed_count=len(send_list),
        sent_count=sent_count,
        failed_count=failed_count,
        dry_run_count=dry_run_count,
        skipped_previously_sent_count=skipped_previously_sent_count
    )


def main():
    check_env()

    campaign = load_campaign(CAMPAIGN_FILE)
    campaign_name = get_campaign_name(campaign)
    subject = campaign.get("subject", "Marketing Email")
    html_content = read_html_file(HTML_FILE)
    subscribers = load_subscribers(SUBSCRIBERS_FILE)

    if not subscribers:
        print("No subscribed users found.")
        return

    print("Email subject:", subject)
    print("Campaign name:", campaign_name)

    send_bulk_emails(subscribers, html_content, subject, campaign_name)

    print("-" * 50)
    print("Bulk send test finished.")
    print("Send log saved to:", LOG_FILE)


if __name__ == "__main__":
    main()
