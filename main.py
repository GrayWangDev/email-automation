import argparse
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv


def run_command(command):
    try:
        result = subprocess.run(command, check=True)
        return result.returncode
    except subprocess.CalledProcessError as error:
        print("Command failed:", " ".join(command))
        print("Exit code:", error.returncode)
        return error.returncode

def run_check():
    print("Step: Check project configuration")
    print("-" * 50)

    env_file = Path(".env")

    if not env_file.exists():
        print("ERROR: .env file not found.")
        print("Please create .env from .env.example first.")
        return 1

    load_dotenv()

    required_files = {
        "RAW_CUSTOMERS_FILE": os.getenv("RAW_CUSTOMERS_FILE", "data/customers.csv"),
        "CAMPAIGN_FILE": os.getenv("CAMPAIGN_FILE", "campaigns/spring_sale_2026/campaign.json"),
        "TEMPLATE_FILE": os.getenv("TEMPLATE_FILE", "templates/email_template.html"),
        "SUBSCRIBERS_FILE": os.getenv("SUBSCRIBERS_FILE", "data/subscribed_only.csv"),
    }

    optional_files = {
        "HTML_FILE": os.getenv("HTML_FILE", "output/preview.html"),
        "LOG_FILE": os.getenv("LOG_FILE", "output/send_log.csv"),
    }

    has_error = False

    print("Environment file:")
    print(f"- .env found: {env_file.exists()}")
    print()

    print("Required files:")
    for name, file_path in required_files.items():
        path = Path(file_path)

        if path.exists():
            print(f"- OK: {name} -> {file_path}")
        else:
            print(f"- MISSING: {name} -> {file_path}")
            has_error = True

    print()
    print("Output files / paths:")
    for name, file_path in optional_files.items():
        path = Path(file_path)

        if path.exists():
            print(f"- OK: {name} -> {file_path}")
        else:
            print(f"- Not created yet: {name} -> {file_path}")

    print()
    print("Send settings:")
    print(f"- DRY_RUN: {os.getenv('DRY_RUN', 'true')}")
    print(f"- MAX_SEND_LIMIT: {os.getenv('MAX_SEND_LIMIT', '3')}")
    print(f"- SEND_DELAY_SECONDS: {os.getenv('SEND_DELAY_SECONDS', '2')}")

    print()
    print("SMTP settings:")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_username = os.getenv("SMTP_USERNAME")
    from_email = os.getenv("FROM_EMAIL")

    print(f"- SMTP_HOST: {smtp_host if smtp_host else 'MISSING'}")
    print(f"- SMTP_USERNAME: {smtp_username if smtp_username else 'MISSING'}")
    print(f"- FROM_EMAIL: {from_email if from_email else 'MISSING'}")

    if not smtp_host or not smtp_username or not from_email:
        print()
        print("WARNING: Some SMTP settings are missing.")

    print()
    if has_error:
        print("Configuration check finished with errors.")
        return 1

    print("Configuration check passed.")
    return 0

def run_filter():
    print("Step: Filter subscribed users")
    print("-" * 50)
    return run_command([sys.executable, "src/filter_subscribers.py"])


def run_preview():
    print("Step: Generate HTML email preview")
    print("-" * 50)
    return run_command([sys.executable, "src/generate_email.py"])


def run_send():
    print("Step: Send bulk email")
    print("-" * 50)
    return run_command([sys.executable, "src/send_bulk_email.py"])


def run_all():
    print("Step: Run full email automation workflow")
    print("=" * 50)

    steps = [
        ("Filter subscribed users", run_filter),
        ("Generate HTML preview", run_preview),
        ("Send email", run_send),
    ]

    for step_name, step_function in steps:
        print()
        print(f"Running: {step_name}")

        exit_code = step_function()

        if exit_code != 0:
            print()
            print(f"Stopped because this step failed: {step_name}")
            return exit_code

    print()
    print("=" * 50)
    print("Full workflow finished.")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Marketing Email Automation Tool"
    )

    parser.add_argument(
        "command",
        choices=["check", "filter", "preview", "send", "all"],
        help="Command to run: check, filter, preview, send, or all"
    )

    args = parser.parse_args()

    if args.command == "check":
        exit_code = run_check()
    elif args.command == "filter":
        exit_code = run_filter()
    elif args.command == "preview":
        exit_code = run_preview()
    elif args.command == "send":
        exit_code = run_send()
    elif args.command == "all":
        exit_code = run_all()
    else:
        parser.print_help()
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()