import json
import html
from pathlib import Path


campaign_file = "campaigns/spring_sale_2026/campaign.json"
template_file = "templates/email_template.html"
output_file = "output/preview.html"

unsubscribe_url = "https://example.com/unsubscribe"


def load_campaign(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        return json.load(file)


def load_template(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()


def build_sections_html(sections):
    section_parts = []

    for section in sections:
        heading = html.escape(section.get("heading", ""))
        text = html.escape(section.get("text", ""))
        image_url = html.escape(section.get("image_url", ""))
        button_text = html.escape(section.get("button_text", ""))
        button_url = html.escape(section.get("button_url", ""))

        section_html = f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:30px;">
          <tr>
            <td>
              <img src="{image_url}" alt="{heading}" width="540" style="display:block; width:100%; max-width:540px; border-radius:6px; margin-bottom:18px;">
            </td>
          </tr>
          <tr>
            <td>
              <h2 style="font-size:22px; color:#222222; margin:0 0 10px;">
                {heading}
              </h2>
              <p style="font-size:16px; color:#444444; line-height:1.6; margin:0 0 18px;">
                {text}
              </p>
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background-color:#111111; border-radius:5px;">
                    <a href="{button_url}" style="display:inline-block; padding:12px 20px; color:#ffffff; text-decoration:none; font-size:15px;">
                      {button_text}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
        """

        section_parts.append(section_html)

    return "\n".join(section_parts)


def render_template(template, campaign):
    sections_html = build_sections_html(campaign.get("sections", []))

    html_output = template

    html_output = html_output.replace("{{ subject }}", html.escape(campaign.get("subject", "")))
    html_output = html_output.replace("{{ preview_text }}", html.escape(campaign.get("preview_text", "")))
    html_output = html_output.replace("{{ logo_url }}", html.escape(campaign.get("logo_url", "")))
    html_output = html_output.replace("{{ hero_image_url }}", html.escape(campaign.get("hero_image_url", "")))
    html_output = html_output.replace("{{ title }}", html.escape(campaign.get("title", "")))
    html_output = html_output.replace("{{ subtitle }}", html.escape(campaign.get("subtitle", "")))
    html_output = html_output.replace("{{ sections_html }}", sections_html)
    html_output = html_output.replace("{{ footer_note }}", html.escape(campaign.get("footer_note", "")))
    html_output = html_output.replace("{{ unsubscribe_url }}", html.escape(unsubscribe_url))

    return html_output


def main():
    Path("output").mkdir(exist_ok=True)

    campaign = load_campaign(campaign_file)
    template = load_template(template_file)

    final_html = render_template(template, campaign)

    with open(output_file, mode="w", encoding="utf-8") as file:
        file.write(final_html)

    print("HTML email preview created:", output_file)
    print("Subject:", campaign.get("subject", ""))


if __name__ == "__main__":
    main()