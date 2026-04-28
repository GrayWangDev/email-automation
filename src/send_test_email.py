import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")
TEST_TO_EMAIL = os.getenv("TEST_TO_EMAIL")

HTML_FILE = "output/preview.html"
SUBJECT = "Test Marketing Email Preview"


def read_html_file(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()


def send_email(to_email, subject, html_content):
    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject

    message.set_content("This email contains an HTML version. Please view it in an HTML-compatible email client.")
    message.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


def check_env():
    required_values = {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USERNAME": SMTP_USERNAME,
        "SMTP_PASSWORD": SMTP_PASSWORD,
        "FROM_EMAIL": FROM_EMAIL,
        "TEST_TO_EMAIL": TEST_TO_EMAIL
    }

    missing = []

    for key, value in required_values.items():
        if not value:
            missing.append(key)

    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")


def main():
    check_env()

    html_content = read_html_file(HTML_FILE)

    send_email(
        to_email=TEST_TO_EMAIL,
        subject=SUBJECT,
        html_content=html_content
    )

    print("Test email sent successfully to:", TEST_TO_EMAIL)


if __name__ == "__main__":
    main()