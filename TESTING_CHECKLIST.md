# Marketing Email Automation Testing Checklist

This checklist should be followed before sending any marketing email campaign.

---

## 1. Prepare Raw Customer CSV

Put the original customer CSV file into:

`data/customers.csv`

Check that the file contains the required columns.

Example Chinese columns:

- 邮箱
- 订阅状态

Example row:

```csv
姓名,邮箱,累计金额,购买次数,订阅状态
Alice,alice@example.com,100,1,已订阅
Bob,bob@example.com,200,2,未订阅
```

---

## 2. Check .env CSV Settings

Open `.env` and confirm:

```env
RAW_CUSTOMERS_FILE=data/customers.csv
FILTERED_SUBSCRIBERS_FILE=data/subscribed_only.csv
SUBSCRIBERS_FILE=data/subscribed_only.csv

EMAIL_COLUMN=邮箱
SUBSCRIBE_COLUMN=订阅状态
SUBSCRIBED_VALUE=已订阅
```

If the CSV column names change, update these values.

For example, if the CSV uses:

```text
邮箱地址
是否订阅
Yes
```

Then update `.env`:

```env
EMAIL_COLUMN=邮箱地址
SUBSCRIBE_COLUMN=是否订阅
SUBSCRIBED_VALUE=Yes
```

---

## 3. Check Project Configuration

Before running the campaign workflow, run:

```bash
python3 main.py check
```

Confirm the result shows:

```text
Configuration check passed.
```

This command does not send emails.

It only checks:

- `.env`
- Raw customer CSV
- Campaign JSON
- Email template
- Subscriber CSV
- Send settings
- SMTP settings

If the check fails, fix the missing file or configuration before continuing.

---

## 4. Filter Subscribed Users

Run:

```bash
python3 main.py filter
```

Or run the script directly:

```bash
python3 src/filter_subscribers.py
```

Expected result:

```text
Filter subscribers finished.
Input file: data/customers.csv
Output file: data/subscribed_only.csv
Total rows: ...
Subscribed users exported: ...
Skipped not subscribed: ...
Skipped empty email: ...
Skipped invalid email: ...
Skipped duplicate: ...
```

Open:

`data/subscribed_only.csv`

Confirm the output format is:

```csv
email,subscribed
customer1@example.com,true
customer2@example.com,true
```

Check:

- Only subscribed users are included.
- Emails are valid.
- Duplicate emails are removed.
- No unrelated customer data is included.

---

## 5. Prepare Campaign Content

Update the campaign JSON file:

`campaigns/spring_sale_2026/campaign.json`

Check these fields:

- subject
- preview_text
- logo_url
- hero_image_url
- title
- subtitle
- sections
- heading
- text
- image_url
- button_text
- button_url
- footer_note

Make sure all image URLs and button URLs are correct.

---

## 6. Check Image URLs

For each image URL:

- Open the URL in an incognito browser window.
- Confirm the image loads successfully.
- Confirm the image does not require login.
- Confirm the image does not return 403 or 404.
- Prefer png, jpg, or jpeg.
- Avoid svg, webp, or avif for better email compatibility.
- Avoid local paths such as `images/logo.png`.
- Avoid local file paths such as `file:///Users/...`.

Good image URL example:

`https://example.com/images/product.jpg`

Bad image URL examples:

`/images/product.jpg`

`file:///Users/user/Desktop/logo.png`

If the image works locally but not in email, the image may not be publicly accessible or may depend on website CSS.

---

## 7. Check Main .env Configuration

Open `.env` and confirm these settings:

```env
DRY_RUN=true
MAX_SEND_LIMIT=3
SEND_DELAY_SECONDS=2

CAMPAIGN_FILE=campaigns/spring_sale_2026/campaign.json
TEMPLATE_FILE=templates/email_template.html
HTML_FILE=output/preview.html
LOG_FILE=output/send_log.csv
RECIPIENT_HISTORY_FILE=output/recipient_history.csv
SUPPRESS_PREVIOUS_SENDS=true
UNSUBSCRIBE_URL=https://example.com/unsubscribe
```

For testing, keep:

```env
DRY_RUN=true
```

Do not set `DRY_RUN=false` until the preview and test results are confirmed.

---

## 8. Generate HTML Preview

Run:

```bash
python3 main.py preview
```

Or run the script directly:

```bash
python3 src/generate_email.py
```

Expected result:

```text
HTML email preview created: output/preview.html
Subject: Your Campaign Subject
```

Open:

`output/preview.html`

Check:

- Logo or brand area
- Hero image
- Title
- Subtitle
- Product sections
- Buttons
- Footer
- Unsubscribe link area
- Overall layout

---

## 9. Send Dry Run

Make sure `.env` has:

```env
DRY_RUN=true
MAX_SEND_LIMIT=3
```

Run:

```bash
python3 main.py send
```

Or run the script directly:

```bash
python3 src/send_bulk_email.py
```

Expected result:

```text
DRY_RUN mode: True
DRY RUN - would send to: xxx@example.com
```

No real emails should be sent in this step.

Check:

- Correct subject
- Correct number of subscribers
- Correct recipient list
- No invalid emails
- No duplicate emails
- MAX_SEND_LIMIT is correct

---

## 10. Send Test Email

Before sending to real customers, use only internal test emails in:

`data/subscribed_only.csv`

Example:

```csv
email,subscribed
your_email@example.com,true
boss_email@example.com,true
test_email@example.com,true
```

Set `.env` like this:

```env
DRY_RUN=false
MAX_SEND_LIMIT=3
```

Run:

```bash
python3 main.py send
```

Or run the script directly:

```bash
python3 src/send_bulk_email.py
```

When prompted, type:

```text
SEND
```

Confirm all test emails are received.

Check in inbox:

- Subject is correct.
- Images load correctly.
- Buttons are clickable.
- Layout looks good on desktop.
- Layout looks acceptable on mobile.
- Email does not go to spam.

After the test, change `.env` back to:

```env
DRY_RUN=true
```

---

## 11. Check Sending Log

Open:

`output/send_log.csv`

Check possible statuses:

- sent
- dry_run
- failed
- skipped_invalid_email
- skipped_duplicate
- skipped_previously_sent

Confirm there are no unexpected failures.

If a real send has already been completed, also check:

`output/recipient_history.csv`

Confirm that successfully sent recipients are recorded under the correct `campaign_name`. If the same campaign is sent again and the CSV contains the same email, that recipient should be skipped and `send_log.csv` should show `skipped_previously_sent`.

---

## 12. Final Pre-Send Safety Check

Before sending to real subscribers, confirm:

- Campaign content has been approved.
- Preview has been reviewed.
- Test emails were received successfully.
- Button URLs are correct.
- Image URLs are public and stable.
- `campaign_name` in `campaign.json` is correct and stable.
- Subscriber CSV contains only intended recipients.
- Raw customer CSV was filtered correctly.
- `SUPPRESS_PREVIOUS_SENDS=true`.
- MAX_SEND_LIMIT is set correctly.
- DRY_RUN is false only when ready.
- Manual confirmation SEND is required.
- Real customer CSV will not be uploaded to GitHub.

Run one final configuration check:

```bash
python3 main.py check
```

Confirm:

```text
Configuration check passed.
```

---

## 13. Real Send

Only after approval, update `.env`:

```env
DRY_RUN=false
MAX_SEND_LIMIT=100
```

Then run:

```bash
python3 main.py send
```

Or run the script directly:

```bash
python3 src/send_bulk_email.py
```

When prompted, type:

```text
SEND
```

Monitor terminal output and:

`output/send_log.csv`

If terminal output includes:

```text
Skipped previously sent recipient
```

the script found an email that already received the same campaign and skipped the duplicate send.

---

## 14. After Sending

After sending:

- Save or review `output/send_log.csv`.
- Review `output/recipient_history.csv`.
- Check failed emails.
- Check inbox or spam reports.
- Record campaign name and send time.
- Do not commit real logs or customer CSV files to GitHub.
- Change `DRY_RUN` back to `true` after sending.

---

## 15. GitHub Safety Check

Before pushing to GitHub, make sure these files are not uploaded:

- .env
- data/customers.csv
- data/subscribed_only.csv
- output/preview.html
- output/send_log.csv
- output/recipient_history.csv

Run:

```bash
git status
```

If sensitive files appear in Git status, stop and fix `.gitignore` first.

Recommended `.gitignore`:

```gitignore
__pycache__/
*.pyc

.env

output/

data/*.csv
!data/sample_subscribers.csv
!data/sample_customers.csv

.DS_Store
```

---

## 16. Recommended Full Testing Order

Follow this order for each campaign:

```text
1. Add or update data/customers.csv
2. Check .env CSV column settings
3. Run python3 main.py check
4. Run python3 main.py filter
5. Check data/subscribed_only.csv
6. Update campaign.json
7. Check all image URLs and button URLs
8. Run python3 main.py preview
9. Review output/preview.html
10. Set DRY_RUN=true
11. Run python3 main.py send
12. Review dry run output
13. Replace subscriber CSV with internal test emails
14. Set DRY_RUN=false and MAX_SEND_LIMIT=3
15. Run python3 main.py send
16. Type SEND to send test emails
17. Confirm test emails look correct
18. Restore real subscribed_only.csv
19. Get approval
20. Run python3 main.py check
21. Set DRY_RUN=false with correct MAX_SEND_LIMIT
22. Run python3 main.py send
23. Type SEND to confirm real sending
24. Review send_log.csv
25. Review recipient_history.csv
26. Set DRY_RUN=true after sending
```

---

## 17. Optional Full Workflow Command

You can also run the full workflow with:

```bash
python3 main.py all
```

This will run:

```text
1. Check project configuration
2. Filter subscribed users
3. Generate HTML preview
4. Send or dry run based on .env
```

For safety, keep:

```env
DRY_RUN=true
```

when using:

```bash
python3 main.py all
```

Do not use `main.py all` with `DRY_RUN=false` unless the campaign is fully approved.
