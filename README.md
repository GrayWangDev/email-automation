# Marketing Email Automation MVP

This project is a basic marketing email automation tool.

It can:

- Read marketing content from a campaign JSON file
- Generate an HTML email preview
- Read subscribed users from a CSV file
- Send HTML emails through SMTP
- Support dry run mode before real sending
- Limit the number of emails sent
- Validate and deduplicate email addresses
- Save sending results to a log file

---

## 1. Project Structure

```text
email-automation
├── data
│   └── subscribed_only.csv
│
├── campaigns
│   └── spring_sale_2026
│       └── campaign.json
│
├── templates
│   └── email_template.html
│
├── output
│   ├── preview.html
│   └── send_log.csv
│
├── src
│   ├── generate_email.py
│   ├── send_test_email.py
│   └── send_bulk_email.py
│
├── .env
├── .gitignore
└── README.md
```

---

## 2. Main Workflow

```text
campaign.json
        ↓
email_template.html
        ↓
generate_email.py
        ↓
output/preview.html
        ↓
send_bulk_email.py
        ↓
subscribed_only.csv
        ↓
HTML emails sent to subscribed users
        ↓
output/send_log.csv
```

---

## 3. Environment Configuration

All important settings are stored in `.env`.

Example:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
TEST_TO_EMAIL=your_email@gmail.com

DRY_RUN=true
MAX_SEND_LIMIT=3
SEND_DELAY_SECONDS=2

SUBSCRIBERS_FILE=data/subscribed_only.csv
CAMPAIGN_FILE=campaigns/spring_sale_2026/campaign.json
TEMPLATE_FILE=templates/email_template.html
HTML_FILE=output/preview.html
LOG_FILE=output/send_log.csv
UNSUBSCRIBE_URL=https://example.com/unsubscribe
```

Important:

- `DRY_RUN=true` means the script will not really send emails.
- `DRY_RUN=false` means real emails will be sent.
- `MAX_SEND_LIMIT=3` means only the first 3 valid subscribers will be processed.
- `SEND_DELAY_SECONDS=2` means the script waits 2 seconds between each email.

---

## 4. Subscriber CSV Format

The subscriber CSV should contain at least these two columns:

```csv
email,subscribed
test1@example.com,true
test2@example.com,true
test3@example.com,false
```

Only users with:

```text
subscribed = true
```

will be processed.

The script will also:

- Skip empty emails
- Skip invalid email addresses
- Skip duplicate emails
- Write skipped records to the send log

---

## 5. Campaign JSON Format

Marketing content is stored in:

```text
campaigns/spring_sale_2026/campaign.json
```

Example:

```json
{
  "campaign_name": "spring_sale_2026",
  "subject": "Spring Sale Gaming PC Deals",
  "preview_text": "Save up to $200 on selected gaming PCs.",
  "logo_url": "https://example.com/logo.png",
  "hero_image_url": "https://example.com/hero.jpg",
  "title": "Spring Sale Gaming PC Deals",
  "subtitle": "Upgrade your setup with limited-time offers.",
  "sections": [
    {
      "heading": "High Performance Gaming PCs",
      "text": "Enjoy smooth gaming, clean cable management, and fast delivery.",
      "image_url": "https://example.com/product1.jpg",
      "button_text": "Shop Now",
      "button_url": "https://example.com/products/gaming-pc"
    }
  ],
  "footer_note": "You are receiving this email because you subscribed to our updates."
}
```

---

## 6. Generate HTML Email Preview

Run:

```bash
python3 src/generate_email.py
```

Output:

```text
output/preview.html
```

Open `preview.html` in a browser to review the email layout.

---

## 7. Send Bulk Email

Before sending, make sure `.env` has:

```env
DRY_RUN=true
```

Then run:

```bash
python3 src/send_bulk_email.py
```

This will simulate sending emails without actually sending them.

To send real emails, change:

```env
DRY_RUN=false
```

Then run:

```bash
python3 src/send_bulk_email.py
```

When `DRY_RUN=false`, the script requires manual confirmation.

You must type:

```text
SEND
```

before real emails are sent.

---

## 8. Sending Log

The sending log is saved to:

```text
output/send_log.csv
```

The log includes:

```csv
time,email,status,error_message
```

Possible statuses:

```text
sent
dry_run
failed
skipped_invalid_email
skipped_duplicate
```

---

## 9. Safety Features

Current safety features:

- Dry run mode
- Maximum send limit
- Email validation
- Duplicate email skipping
- Send delay between emails
- Sending log
- Manual confirmation before real sending

Recommended safe workflow:

```text
1. Set DRY_RUN=true
2. Generate preview.html
3. Review the email preview
4. Run send_bulk_email.py in dry run mode
5. Check the recipient list and log
6. Change DRY_RUN=false only after confirmation
7. Type SEND manually to confirm real sending
```

---

## 10. Important Notes

Do not upload real customer CSV files to GitHub.

The `.env` file contains sensitive email credentials and should not be uploaded.

The following files should be ignored by Git:

```text
.env
output/
data/*.csv
```

Use a sample CSV file for testing if the project is uploaded to GitHub.

---

## 11. Future Improvements

Possible next steps:

- Add a simple web interface
- Support Word, PDF, TXT, or Markdown content input
- Add login and permission control
- Switch from Gmail SMTP to Amazon SES, SendGrid, Mailchimp, or Klaviyo
- Add unsubscribe tracking
- Add campaign history
- Add better email templates
- Deploy to AWS