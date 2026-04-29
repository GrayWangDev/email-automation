# 营销邮件自动化测试清单

每次发送营销邮件前，都建议按照这份清单检查。

---

## 1. 准备原始客户 CSV

把原始客户 CSV 放到：

`data/customers.csv`

确认 CSV 里有必要字段。

常见中文字段：

- 邮箱
- 订阅状态

示例：

```csv
姓名,邮箱,累计金额,购买次数,订阅状态
Alice,alice@example.com,100,1,已订阅
Bob,bob@example.com,200,2,未订阅
```

---

## 2. 检查 `.env` 里的 CSV 配置

打开 `.env`，确认：

```env
RAW_CUSTOMERS_FILE=data/customers.csv
FILTERED_SUBSCRIBERS_FILE=data/subscribed_only.csv
SUBSCRIBERS_FILE=data/subscribed_only.csv

EMAIL_COLUMN=邮箱
SUBSCRIBE_COLUMN=订阅状态
SUBSCRIBED_VALUE=已订阅
```

如果 CSV 字段名变化，需要同步修改。

例如 CSV 里字段变成：

```text
邮箱地址
是否订阅
Yes
```

则 `.env` 改成：

```env
EMAIL_COLUMN=邮箱地址
SUBSCRIBE_COLUMN=是否订阅
SUBSCRIBED_VALUE=Yes
```

---

## 3. 检查项目配置

运行：

```bash
python3 main.py check
```

确认终端显示：

```text
Configuration check passed.
```

这个命令不会发送邮件。

它只检查：

- `.env` 是否存在
- 原始客户 CSV 是否存在
- campaign JSON 是否存在
- 邮件模板是否存在
- 订阅用户 CSV 是否存在
- 发送设置是否存在
- SMTP 设置是否存在

如果检查失败，先修复缺失文件或配置，再继续。

---

## 4. 筛选已订阅用户

运行：

```bash
python3 main.py filter
```

或者直接运行：

```bash
python3 src/filter_subscribers.py
```

正常结果类似：

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

打开：

`data/subscribed_only.csv`

确认格式是：

```csv
email,subscribed
customer1@example.com,true
customer2@example.com,true
```

检查：

- 只保留了已订阅用户
- 邮箱格式正确
- 重复邮箱已去重
- 没有多余客户信息
- 没有未订阅用户

---

## 5. 准备营销内容

修改营销内容文件：

`campaigns/spring_sale_2026/campaign.json`

检查字段：

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

确认：

- 邮件标题正确
- 图片 URL 正确
- 按钮文字正确
- 按钮链接正确
- 正文内容正确

---

## 6. 检查图片 URL

每个图片 URL 都要检查：

- 在无痕窗口打开 URL
- 确认图片能正常加载
- 确认不需要登录
- 确认没有 403 或 404
- 推荐使用 png、jpg、jpeg
- 尽量避免 svg、webp、avif
- 不要使用本地路径，例如 `images/logo.png`
- 不要使用本地文件路径，例如 `file:///Users/...`

推荐：

`https://example.com/images/product.jpg`

不推荐：

`/images/product.jpg`

`file:///Users/user/Desktop/logo.png`

如果图片本地 HTML 能显示，但邮件里不能显示，通常说明：

- 图片不是公开可访问
- 图片需要登录
- 图片服务器防盗链
- 图片依赖官网 CSS
- 图片格式不适合邮件客户端

---

## 7. 检查主要 `.env` 配置

打开 `.env`，确认：

```env
DRY_RUN=true
MAX_SEND_LIMIT=3
SEND_DELAY_SECONDS=2

CAMPAIGN_FILE=campaigns/spring_sale_2026/campaign.json
TEMPLATE_FILE=templates/email_template.html
HTML_FILE=output/preview.html
LOG_FILE=output/send_log.csv
UNSUBSCRIBE_URL=https://example.com/unsubscribe
```

测试阶段保持：

```env
DRY_RUN=true
```

在预览和测试邮件确认前，不要改成：

```env
DRY_RUN=false
```

---

## 8. 生成 HTML 邮件预览

运行：

```bash
python3 main.py preview
```

或者直接运行：

```bash
python3 src/generate_email.py
```

正常输出类似：

```text
HTML email preview created: output/preview.html
Subject: Your Campaign Subject
```

打开：

`output/preview.html`

检查：

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

## 9. 发送测试邮件

运行：

```bash
python3 main.py test-send
```

这个命令只会发送到 `.env` 里的：

```env
TEST_TO_EMAIL=your_email@gmail.com
```

它不会读取客户 CSV，也不会群发。

确认测试邮箱收到邮件后，检查：

- 邮件标题正确
- 图片能显示
- 按钮能点击
- 链接跳转正确
- 桌面端显示正常
- 手机端显示可以接受
- 邮件没有进入垃圾箱

---

## 10. Dry Run 模拟批量发送

确认 `.env` 里是：

```env
DRY_RUN=true
MAX_SEND_LIMIT=3
```

运行：

```bash
python3 main.py send
```

或者直接运行：

```bash
python3 src/send_bulk_email.py
```

正常输出类似：

```text
DRY_RUN mode: True
DRY RUN - would send to: xxx@example.com
```

这一步不会真的发送邮件。

检查：

- 邮件标题正确
- 订阅用户数量正确
- 收件人列表正确
- 没有无效邮箱
- 没有重复邮箱
- MAX_SEND_LIMIT 数量正确

---

## 11. 内部测试发送

正式发给客户前，可以只用内部测试邮箱。

临时把 `data/subscribed_only.csv` 改成内部测试邮箱：

```csv
email,subscribed
your_email@example.com,true
boss_email@example.com,true
test_email@example.com,true
```

然后设置 `.env`：

```env
DRY_RUN=false
MAX_SEND_LIMIT=3
```

运行：

```bash
python3 main.py send
```

系统提示时输入：

```text
SEND
```

确认所有内部测试邮箱都收到邮件。

测试完成后，把 `.env` 改回：

```env
DRY_RUN=true
```

---

## 12. 检查发送日志

打开：

`output/send_log.csv`

可能出现的状态：

- sent
- dry_run
- failed
- skipped_invalid_email
- skipped_duplicate

确认没有异常失败。

如果有失败，查看 `error_message` 原因。

---

## 13. 正式发送前最终检查

正式发送前确认：

- 营销内容已经审核
- HTML 预览已经检查
- 测试邮件已经收到
- 按钮 URL 正确
- 图片 URL 公开且稳定
- 原始客户 CSV 已正确筛选
- `subscribed_only.csv` 只包含目标收件人
- `MAX_SEND_LIMIT` 设置正确
- `DRY_RUN=false` 只在准备正式发送时使用
- 正式发送需要手动输入 `SEND`
- 真实客户 CSV 不会上传 GitHub

再运行一次：

```bash
python3 main.py check
```

确认：

```text
Configuration check passed.
```

---

## 14. 正式发送

获得确认后，修改 `.env`：

```env
DRY_RUN=false
MAX_SEND_LIMIT=100
```

然后运行：

```bash
python3 main.py send
```

或：

```bash
python3 src/send_bulk_email.py
```

系统提示时输入：

```text
SEND
```

发送过程中观察终端输出，并检查：

`output/send_log.csv`

---

## 15. 发送后处理

发送后：

- 查看 `output/send_log.csv`
- 检查失败邮箱
- 检查是否有邮件进入垃圾箱
- 记录 campaign 名称和发送时间
- 不要把真实日志或客户 CSV 上传 GitHub
- 把 `.env` 改回：

```env
DRY_RUN=true
```

---

## 16. GitHub 安全检查

上传 GitHub 前，确认这些文件不会上传：

- .env
- data/customers.csv
- data/subscribed_only.csv
- output/preview.html
- output/send_log.csv

运行：

```bash
git status
```

如果看到敏感文件，先不要提交。

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

---

## 17. 推荐完整测试顺序

每次活动建议按这个顺序：

```text
1. 添加或更新 data/customers.csv
2. 检查 .env 里的 CSV 字段配置
3. 运行 python3 main.py check
4. 运行 python3 main.py filter
5. 检查 data/subscribed_only.csv
6. 更新 campaign.json
7. 检查所有图片 URL 和按钮 URL
8. 运行 python3 main.py preview
9. 打开 output/preview.html 检查
10. 运行 python3 main.py test-send
11. 确认测试邮件正常
12. 设置 DRY_RUN=true
13. 运行 python3 main.py send
14. 检查 Dry Run 输出
15. 如需内部测试，把 subscribed_only.csv 临时换成内部邮箱
16. 设置 DRY_RUN=false 和 MAX_SEND_LIMIT=3
17. 运行 python3 main.py send
18. 输入 SEND 发送内部测试邮件
19. 确认内部测试邮件正常
20. 恢复真实 subscribed_only.csv
21. 获得正式发送批准
22. 运行 python3 main.py check
23. 设置 DRY_RUN=false 和正确的 MAX_SEND_LIMIT
24. 运行 python3 main.py send
25. 输入 SEND 确认正式发送
26. 检查 output/send_log.csv
27. 发送结束后设置 DRY_RUN=true
```

---

## 18. 可选完整流程命令

也可以运行完整流程：

```bash
python3 main.py all
```

它会依次执行：

```text
1. 检查项目配置
2. 筛选已订阅用户
3. 生成 HTML 预览
4. 根据 .env 执行 Dry Run 或发送
```

为了安全，使用 `main.py all` 时建议保持：

```env
DRY_RUN=true
```

不要在没有完全确认的情况下，用：

```bash
python3 main.py all
```

配合：

```env
DRY_RUN=false
```

否则可能直接进入正式发送流程。