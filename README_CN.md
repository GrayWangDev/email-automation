# 营销邮件自动化工具 MVP

这是一个基础版的营销邮件自动化工具。

目前它可以完成：

- 读取原始客户 CSV 文件
- 从原始 CSV 中筛选已订阅用户
- 生成干净的订阅用户 CSV
- 读取营销内容 `campaign.json`
- 根据 HTML 模板生成营销邮件预览
- 通过 SMTP 发送 HTML 邮件
- 支持 Dry Run 测试模式，避免误发
- 支持发送数量限制
- 自动校验邮箱格式
- 自动去重重复邮箱
- 支持按活动记录已发送用户，避免同一活动重复发送给同一邮箱
- 生成发送日志
- 通过统一命令 `main.py` 运行整个流程

---

## 1. 项目作用

这个项目的目标是把营销邮件发送流程自动化。

市场部以后只需要准备：

- 邮件标题
- 预览文字
- 产品图片 URL
- 邮件正文
- 按钮文字
- 按钮跳转链接
- 原始客户 CSV

技术人员运行脚本后，系统可以自动：

```text
筛选已订阅用户
↓
生成 HTML 邮件
↓
发送测试邮件
↓
Dry Run 模拟发送
↓
确认后正式发送
↓
记录发送日志
```

---

## 2. 项目目录结构

```text
email-automation
├── main.py
│
├── data
│   ├── customers.csv
│   ├── subscribed_only.csv
│   ├── sample_customers.csv
│   └── sample_subscribers.csv
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
│   ├── send_log.csv
│   └── recipient_history.csv
│
├── src
│   ├── filter_subscribers.py
│   ├── generate_email.py
│   ├── send_test_email.py
│   └── send_bulk_email.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── README_CN.md
├── TESTING_CHECKLIST.md
└── TESTING_CHECKLIST_CN.md
```

重要说明：

- `.env` 不能上传到 GitHub，因为里面有邮箱账号和密码。
- `data/customers.csv` 不能上传到 GitHub，因为里面可能有真实客户数据。
- `data/subscribed_only.csv` 不能上传到 GitHub，因为里面有客户邮箱。
- `output/` 不能上传到 GitHub，因为里面有预览文件、发送日志和收件人历史。
- `sample_customers.csv` 和 `sample_subscribers.csv` 是示例数据，可以上传。

---

## 3. 整体流程

```text
原始客户 CSV
        ↓
filter_subscribers.py
        ↓
已订阅用户 CSV
        ↓
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
发送 HTML 邮件
        ↓
output/send_log.csv
```

现在也可以通过统一入口运行：

```text
python3 main.py all
        ↓
check
        ↓
filter
        ↓
preview
        ↓
send
```

---

## 4. 安装依赖

第一次运行项目时，需要安装 Python 依赖：

```bash
python3 -m pip install -r requirements.txt
```

目前主要依赖：

```text
python-dotenv
```

这个库用于读取 `.env` 配置文件。

---

## 5. 环境配置 `.env`

项目根目录需要有一个 `.env` 文件。

可以参考：

```text
.env.example
```

示例：

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

RAW_CUSTOMERS_FILE=data/customers.csv
FILTERED_SUBSCRIBERS_FILE=data/subscribed_only.csv
SUBSCRIBERS_FILE=data/subscribed_only.csv

EMAIL_COLUMN=邮箱
SUBSCRIBE_COLUMN=订阅状态
SUBSCRIBED_VALUE=已订阅

CAMPAIGN_FILE=campaigns/spring_sale_2026/campaign.json
TEMPLATE_FILE=templates/email_template.html
HTML_FILE=output/preview.html
LOG_FILE=output/send_log.csv
RECIPIENT_HISTORY_FILE=output/recipient_history.csv
SUPPRESS_PREVIOUS_SENDS=true
UNSUBSCRIBE_URL=https://example.com/unsubscribe
```

字段说明：

| 配置项 | 作用 |
|---|---|
| `SMTP_HOST` | 邮件服务器地址 |
| `SMTP_PORT` | 邮件服务器端口 |
| `SMTP_USERNAME` | 发件邮箱账号 |
| `SMTP_PASSWORD` | 发件邮箱授权码或 SMTP 密码 |
| `FROM_EMAIL` | 发件人邮箱 |
| `TEST_TO_EMAIL` | 测试收件邮箱 |
| `DRY_RUN` | 是否开启模拟发送 |
| `MAX_SEND_LIMIT` | 最多处理多少个邮箱 |
| `SEND_DELAY_SECONDS` | 每封邮件之间等待几秒 |
| `RAW_CUSTOMERS_FILE` | 原始客户 CSV 路径 |
| `FILTERED_SUBSCRIBERS_FILE` | 筛选后的订阅用户 CSV 输出路径 |
| `SUBSCRIBERS_FILE` | 发送模块读取的订阅用户 CSV |
| `EMAIL_COLUMN` | 原始 CSV 中的邮箱列名 |
| `SUBSCRIBE_COLUMN` | 原始 CSV 中的订阅状态列名 |
| `SUBSCRIBED_VALUE` | 什么值代表已订阅 |
| `CAMPAIGN_FILE` | 营销内容 JSON 文件路径 |
| `TEMPLATE_FILE` | HTML 邮件模板路径 |
| `HTML_FILE` | 生成的 HTML 预览文件路径 |
| `LOG_FILE` | 发送日志文件路径 |
| `RECIPIENT_HISTORY_FILE` | 收件人发送历史文件路径，用于避免同一活动重复发送 |
| `SUPPRESS_PREVIOUS_SENDS` | 是否跳过当前活动已经成功发送过的邮箱 |
| `UNSUBSCRIBE_URL` | 退订链接 |

---

## 6. Dry Run 是什么？

`DRY_RUN=true` 表示只模拟发送，不会真的发邮件。

例如：

```env
DRY_RUN=true
```

运行发送命令后，系统只会显示：

```text
DRY RUN - would send to: xxx@example.com
```

这一步不会真的发送邮件。

正式发送前才改成：

```env
DRY_RUN=false
```

为了安全，建议平时默认保持：

```env
DRY_RUN=true
```

Dry Run 不会把邮箱写入 `recipient_history.csv` 的成功发送记录，因此不会影响后续正式发送去重。

### 防止同一活动重复发送

发送模块会根据 `campaign_name + email` 做跨批次去重。

例如：

```text
5 月 1 日，spring_sale_2026 成功发送给 alice@example.com
5 月 2 日，alice@example.com 又因为浏览网页出现在新的 CSV
系统会跳过 alice@example.com，不再重复发送 spring_sale_2026
```

如果换成新的活动，例如 `summer_sale_2026`，同一个邮箱仍然可以收到新活动邮件。

这个功能依赖：

```env
RECIPIENT_HISTORY_FILE=output/recipient_history.csv
SUPPRESS_PREVIOUS_SENDS=true
```

只有真实发送成功的记录会写入 `recipient_history.csv` 并参与后续去重。`dry_run` 和 `failed` 不会阻止下次发送。

---

## 7. 原始客户 CSV 格式

原始客户 CSV 可以有很多字段，例如：

```csv
姓名,邮箱,累计金额,购买次数,注册时间,订阅状态,业务员
Alice,alice@example.com,100,1,2026-01-01,已订阅,Tom
Bob,bob@example.com,200,2,2026-01-02,未订阅,Tom
Charlie,charlie@example.com,300,3,2026-01-03,已订阅,Amy
Duplicate Alice,alice@example.com,400,4,2026-01-04,已订阅,Amy
Invalid Email,wrong-email,500,5,2026-01-05,已订阅,Tom
Empty Email,,600,6,2026-01-06,已订阅,Amy
```

脚本只关心两个字段：

```text
邮箱
订阅状态
```

这两个字段可以在 `.env` 里配置：

```env
EMAIL_COLUMN=邮箱
SUBSCRIBE_COLUMN=订阅状态
SUBSCRIBED_VALUE=已订阅
```

如果以后 CSV 字段变成：

```text
邮箱地址
是否订阅
Yes
```

则改成：

```env
EMAIL_COLUMN=邮箱地址
SUBSCRIBE_COLUMN=是否订阅
SUBSCRIBED_VALUE=Yes
```

---

## 8. 筛选已订阅用户

运行：

```bash
python3 main.py filter
```

或者直接运行：

```bash
python3 src/filter_subscribers.py
```

它会读取：

```text
data/customers.csv
```

然后生成：

```text
data/subscribed_only.csv
```

输出格式：

```csv
email,subscribed
alice@example.com,true
charlie@example.com,true
```

筛选逻辑：

- 只保留已订阅用户
- 跳过空邮箱
- 跳过格式错误的邮箱
- 跳过重复邮箱
- 邮箱统一转成小写
- 输出文件只保留 `email` 和 `subscribed`

---

## 9. 订阅用户 CSV 格式

最终发送模块读取的 CSV 格式应该是：

```csv
email,subscribed
test1@example.com,true
test2@example.com,true
test3@example.com,false
```

只有：

```text
subscribed = true
```

的邮箱会被处理。

---

## 10. 营销内容 `campaign.json`

营销内容放在：

```text
campaigns/spring_sale_2026/campaign.json
```

示例：

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
    },
    {
      "heading": "Limited Time Discount",
      "text": "Selected models are available with special promotional pricing.",
      "image_url": "https://example.com/product2.jpg",
      "button_text": "View Deals",
      "button_url": "https://example.com/collections/sale"
    }
  ],
  "footer_note": "You are receiving this email because you subscribed to our updates."
}
```

字段说明：

| 字段 | 作用 |
|---|---|
| `campaign_name` | 活动名称 |
| `subject` | 邮件标题 |
| `preview_text` | 邮箱列表里显示的预览文字 |
| `logo_url` | Logo 图片链接 |
| `hero_image_url` | 邮件顶部主图链接 |
| `title` | 邮件大标题 |
| `subtitle` | 副标题 |
| `sections` | 促销内容模块 |
| `heading` | 模块标题 |
| `text` | 模块正文 |
| `image_url` | 模块图片 |
| `button_text` | 按钮文字 |
| `button_url` | 按钮跳转链接 |
| `footer_note` | 邮件底部说明 |

---

## 11. 图片 URL 要求

营销邮件中的图片必须使用公网可访问的完整链接。

推荐：

```text
https://example.com/images/product.jpg
```

不推荐：

```text
/images/product.jpg
file:///Users/user/Desktop/logo.png
images/logo.png
```

图片 URL 检查方法：

1. 复制图片 URL。
2. 打开 Chrome 无痕窗口。
3. 粘贴 URL。
4. 如果能直接看到图片，说明基本可用。
5. 如果出现 403、404、需要登录，则邮件里也无法稳定显示。

建议图片格式：

```text
png
jpg
jpeg
```

尽量避免：

```text
svg
webp
avif
```

有些图片在网页上显示正常，但邮件里不正常，是因为网页可能使用了 CSS、登录权限或防盗链。邮件客户端不会继承官网 CSS。

---

## 12. 生成 HTML 邮件预览

运行：

```bash
python3 main.py preview
```

或者直接运行：

```bash
python3 src/generate_email.py
```

生成文件：

```text
output/preview.html
```

生成后用浏览器打开 `preview.html` 检查：

- Logo 或品牌区域
- 主图
- 标题
- 副标题
- 产品模块
- 按钮
- Footer
- 退订链接区域
- 整体排版

---

## 13. 发送测试邮件

发送测试邮件命令：

```bash
python3 main.py test-send
```

这个命令只会发送到 `.env` 里的：

```env
TEST_TO_EMAIL=your_email@gmail.com
```

它不会读取客户 CSV，也不会群发。

适合用于：

- 发给自己检查邮件效果
- 发给领导确认样式
- 发给市场部确认内容

---

## 14. 批量发送 / Dry Run

运行：

```bash
python3 main.py send
```

如果 `.env` 里是：

```env
DRY_RUN=true
```

则不会真的发送，只会模拟：

```text
DRY RUN - would send to: xxx@example.com
```

如果要真实发送，需要改成：

```env
DRY_RUN=false
```

然后再次运行：

```bash
python3 main.py send
```

真实发送前，系统会要求输入：

```text
SEND
```

只有输入 `SEND` 后才会真的发送。

---

## 15. 统一命令入口

项目支持以下命令：

```bash
python3 main.py check
python3 main.py filter
python3 main.py preview
python3 main.py test-send
python3 main.py send
python3 main.py all
```

命令说明：

| 命令 | 作用 |
|---|---|
| `check` | 检查配置和必要文件 |
| `filter` | 从原始 CSV 筛选已订阅用户 |
| `preview` | 生成 HTML 邮件预览 |
| `test-send` | 发送测试邮件到 `TEST_TO_EMAIL` |
| `send` | Dry Run 或正式批量发送 |
| `all` | 按顺序执行 check、filter、preview、send |

推荐正式发送前先运行：

```bash
python3 main.py check
```

这个命令不会发送邮件，只会检查配置。

---

## 16. 推荐完整运行流程

一般活动可以按这个顺序：

```bash
python3 main.py check
python3 main.py filter
python3 main.py preview
python3 main.py test-send
python3 main.py send
```

或者在 Dry Run 阶段运行完整流程：

```bash
python3 main.py all
```

建议安全流程：

```text
1. 把原始客户 CSV 放入 data/customers.csv
2. 检查 .env 里的 CSV 字段配置
3. 运行 python3 main.py check
4. 运行 python3 main.py filter
5. 检查 data/subscribed_only.csv
6. 更新 campaign.json
7. 检查所有图片 URL 和按钮 URL
8. 运行 python3 main.py preview
9. 打开 output/preview.html 检查邮件
10. 运行 python3 main.py test-send
11. 确认测试邮箱收到邮件
12. 保持 DRY_RUN=true
13. 运行 python3 main.py send
14. 检查 Dry Run 结果
15. 获得上级或市场部确认
16. 设置 DRY_RUN=false
17. 设置正确的 MAX_SEND_LIMIT
18. 运行 python3 main.py send
19. 输入 SEND 确认正式发送
20. 检查 output/send_log.csv
21. 发送结束后把 DRY_RUN 改回 true
```

---

## 17. 发送日志

发送日志保存到：

```text
output/send_log.csv
```

日志字段：

```csv
time,email,status,error_message
```

可能出现的状态：

```text
sent
dry_run
failed
skipped_invalid_email
skipped_duplicate
skipped_previously_sent
```

用途：

- 查看哪些邮箱发送成功
- 查看哪些邮箱发送失败
- 查看哪些邮箱被跳过
- 排查失败原因

另外，正式发送成功的收件人会记录到：

```text
output/recipient_history.csv
```

这个文件用于防止同一个 `campaign_name` 重复发送给同一个邮箱。

---

## 18. 安全机制

当前项目已有安全机制：

- Dry Run 模拟发送
- 最大发送数量限制
- 邮箱格式校验
- 重复邮箱跳过
- 同一活动已成功发送过的邮箱自动跳过
- 每封邮件之间延迟发送
- 发送日志记录
- 正式发送前必须输入 `SEND`
- 原始 CSV 先筛选再发送
- CSV 字段名可配置
- 所有重要路径集中在 `.env`
- 统一命令入口 `main.py`
- `test-send` 和正式发送分开

建议：

```text
平时默认 DRY_RUN=true
正式发送前必须先 test-send
正式发送前必须先 check
正式发送前必须确认 MAX_SEND_LIMIT
发送后立刻把 DRY_RUN 改回 true
```

---

## 19. GitHub 安全注意事项

不要上传真实客户数据。

不要上传：

```text
.env
data/customers.csv
data/subscribed_only.csv
output/preview.html
output/send_log.csv
output/recipient_history.csv
```

可以上传：

```text
data/sample_customers.csv
data/sample_subscribers.csv
README.md
README_CN.md
TESTING_CHECKLIST.md
TESTING_CHECKLIST_CN.md
src/
templates/
campaigns/
```

推荐 `.gitignore`：

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

上传 GitHub 前先运行：

```bash
git status
```

确认没有敏感文件再提交。

---

## 20. 更新 GitHub

修改项目后，上传 GitHub：

```bash
git status
git add .
git status
git commit -m "Update marketing email automation workflow"
git push
```

提交前必须确认没有：

```text
.env
真实客户 CSV
output 文件
发送日志
```

---

## 21. 后续可扩展方向

后续可以继续扩展：

- 做成网页界面
- 支持 Word、PDF、TXT、Markdown 输入
- 增加登录权限
- 接入 Amazon SES、SendGrid、Mailchimp、Klaviyo
- 增加退订功能
- 增加活动历史记录
- 增加更好看的邮件模板
- 在网页中预览邮件
- 部署到 AWS
