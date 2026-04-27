# Email Automation MVP

This project is a basic marketing email automation demo.

## Current Features

- Read marketing content from `campaign.json`
- Generate HTML email from `email_template.html`
- Output preview file to `output/preview.html`
- Keep content, template, and script separated

## Folder Structure

```text
email-automation
├── data
│   └── subscribed_only.csv
├── campaigns
│   └── spring_sale_2026
│       └── campaign.json
├── templates
│   └── email_template.html
├── output
│   └── preview.html
└── src
    └── generate_email.py
How to Update Marketing Content

Edit this file:

campaigns/spring_sale_2026/campaign.json

Fields:

subject: email subject
preview_text: short preview text shown in inbox
logo_url: logo image URL
hero_image_url: top hero image URL
title: main title
subtitle: subtitle
sections: promotional content blocks
footer_note: footer text
How to Generate Email Preview

Run:

python3 src/generate_email.py

The generated HTML preview will be saved here:

output/preview.html
Next Steps
Connect subscribed user CSV
Add email sending module
Add unsubscribe URL support
Add logging