# Marketing Email Automation Testing Checklist

This checklist should be followed before sending any marketing email campaign.

---

## 1. Prepare Campaign Content

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
- button_text
- button_url
- footer_note

Make sure all image URLs and button URLs are correct.

---

## 2. Check Image URLs

For each image URL:

- Open the URL in an incognito browser window.
- Confirm the image loads successfully.
- Confirm the image does not require login.
- Confirm the image does not return 403 or 404.
- Prefer png, jpg, or jpeg.
- Avoid local paths such as `images/logo.png`.
- Avoid local file paths such as `file:///Users/...`.

Good image URL example:

`https://example.com/images/product.jpg`

Bad image URL examples:

`/images/product.jpg`

`file:///Users/user/Desktop/logo.png`

---

## 3. Check .env Configuration

Open `.env` and confirm these settings:

```env
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

For testing, keep:

```env
DRY_RUN=true
```

Do not set `DRY_RUN=false` until the preview and test results are confirmed.

---

## 4. Generate HTML Preview

Run:

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

## 5. Send Dry Run

Run:

```bash
python3 src/send_bulk_email.py
```

Make sure `.env` has:

```env
DRY_RUN=true
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

---

## 6. Send Test Email

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
python3 src/send_bulk_email.py
```

When prompted, type:

```text
SEND
```

Confirm all test emails are received.

Check in inbox:

- Subject is correct
- Images load correctly
- Buttons are clickable
- Layout looks good on desktop
- Layout looks acceptable on mobile
- Email does not go to spam

---

## 7. Check Sending Log

Open:

`output/send_log.csv`

Check possible statuses:

- sent
- dry_run
- failed
- skipped_invalid_email
- skipped_duplicate

Confirm there are no unexpected failures.

---

## 8. Final Pre-Send Safety Check

Before sending to real subscribers, confirm:

- Campaign content has been approved.
- Preview has been reviewed.
- Test emails were received successfully.
- Button URLs are correct.
- Image URLs are public and stable.
- Subscriber CSV contains only intended recipients.
- MAX_SEND_LIMIT is set correctly.
- DRY_RUN is false only when ready.
- Manual confirmation SEND is required.

---

## 9. Real Send

Only after approval, update `.env`:

```env
DRY_RUN=false
MAX_SEND_LIMIT=100
```

Then run:

```bash
python3 src/send_bulk_email.py
```

When prompted, type:

```text
SEND
```

Monitor terminal output and `output/send_log.csv`.

---

## 10. After Sending

After sending:

- Save or review `output/send_log.csv`.
- Check failed emails.
- Check inbox or spam reports.
- Record campaign name and send time.
- Do not commit real logs or customer CSV files to GitHub.

---

## 11. GitHub Safety Check

Before pushing to GitHub, make sure these files are not uploaded:

- .env
- data/customers.csv
- data/subscribed_only.csv
- output/preview.html
- output/send_log.csv

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
.DS_Store
```