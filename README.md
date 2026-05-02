# 钓鱼邮件安全意识培训系统

基于 Flask 的企业内部钓鱼邮件模拟与安全意识培训平台，用于对员工进行钓鱼邮件识别能力的测试与教育。

## 功能

- **钓鱼邮件发送** — 通过 SMTP 向目标员工发送仿真的钓鱼邮件，支持多种场景模板
- **点击跟踪** — 记录员工点击行为（IP、User-Agent、浏览器信息等），生成统计报表
- **安全教育** — 点击钓鱼链接后展示警示教育页面，帮助员工识别钓鱼邮件的特征
- **管理面板** — Web 管理界面，支持活动管理、实时发送进度、统计数据查看
- **模板可定制** — 邮件模板和警示页面模板均支持自定义编辑

## 邮件模板

| 模板 ID | 场景 |
|---------|------|
| `hr_bonus` | HR 年终绩效奖金确认通知 |
| `it_maintenance` | IT 系统维护升级通知 |
| `shared_document` | 内部文件分享通知 |
| `ceo_message` | CEO 组织架构优化通知 |
| `invoice_notice` | 财务报销审核通知 |
| `meeting_invite` | 战略规划会议邀请 |
| `security_compliance` | 信息安全合规自查通知 |

## 技术栈

- **Python 3** + Flask
- SQLite（点击行为追踪）
- 邮件模板：HTML + 内联 CSS
- 前端管理面板：原生 JavaScript（无框架依赖）
- 打包工具：PyInstaller

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务（默认 http://0.0.0.0:5000）
python main.py
```

启动后自动打开浏览器访问管理面板 `http://127.0.0.1:5000/admin`。

## 配置

所有配置通过 `config.json` 管理，也可在管理面板中在线修改：

| 配置项 | 说明 |
|--------|------|
| `smtp_server` | SMTP 服务器地址 |
| `smtp_port` | SMTP 端口 |
| `sender_email` | 发件人邮箱 |
| `sender_password` | 发件人邮箱密码 |
| `base_url` | 跟踪服务器外网访问地址 |
| `email_template` | 使用的邮件模板 ID |
| `warning_template` | 警示页面模板 ID |
| `campaign_name` | 活动名称 |
| `email_subject` | 邮件主题 |
| `server_host` | 服务器监听地址 |
| `server_port` | 服务器监听端口 |

## 目标邮箱列表

将目标员工邮箱放入 `maillist.xlsx`，系统会自动读取。支持通过管理面板预览当前列表。

## 打包

```bash
pyinstaller PhishingTrainer.spec
```

打包后生成独立的可执行文件，可直接分发运行，无需安装 Python 环境。

## 项目结构

```
├── main.py              # 程序入口
├── tracker_server.py    # Flask Web 服务 & API 路由
├── email_sender.py      # SMTP 邮件发送模块
├── dataconfig.py        # SQLite 数据库管理
├── templates.py         # 邮件 HTML 模板
├── template_config.py   # 模板文本配置
├── config_manager.py    # 配置文件读写
├── getmiallist.py       # Excel 邮箱列表读取
├── config.json          # 运行配置文件
├── requirements.txt     # Python 依赖
├── static/              # 前端静态文件 & 警示页面
│   ├── admin.html       # 管理面板
│   ├── login.html       # 登录页面
│   └── warning_*.html   # 警示教育页面模板
└── dist/                # PyInstaller 打包输出
```
