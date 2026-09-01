# OLETOKEN 中转站 Discord 社区 🚀

一站式 AI API 中转站 Discord 社区自动搭建方案：频道/身份组/权限/欢迎机器人，全部自动化。

## 社区结构

```
OLETOKEN 中转站
├── 📢 信息中心
│   ├── #announcements  - 官方公告
│   ├── #rules          - 社区规则
│   └── #faq            - 常见问题
├── 🟢 服务状态
│   ├── #service-status - 实时服务状态
│   └── #maintenance    - 维护通知
├── 📖 文档与指南
│   ├── #api-docs       - API接入文档
│   ├── #tutorials      - 使用教程
│   ├── #pricing         - 定价说明
│   └── #models-list    - 支持模型列表
├── 💬 社区交流
│   ├── #general         - 综合讨论
│   ├── #tech-talk       - 技术交流
│   ├── #support         - 问题反馈
│   └── #suggestions     - 功能建议
├── 🤖 模型讨论
│   ├── #claude-models   - Claude模型
│   ├── #gpt-models      - GPT模型
│   ├── #cn-models        - 国产模型
│   └── #image-models    - 图像模型
├── 💻 开发者
│   ├── #api-integration - API接入
│   ├── #sdk-code        - SDK与代码
│   └── #showcase        - 项目展示
├── 🔒 管理区 (仅管理组)
│   ├── #admin            - 管理讨论
│   ├── #audit-log        - 审核记录
│   └── #bot-commands     - 机器人命令
└── #welcome             - 欢迎频道
```

## 身份组

| 身份组 | 颜色 | 权限 |
|--------|------|------|
| 🔴 OLETOKEN Team | 红色 | 管理员 |
| 🟠 Moderator | 橙色 | 管理频道/封禁 |
| 🟢 Developer | 绿色 | 普通成员+ |
| 🔵 VIP Member | 蓝色 | 普通成员+ |
| ⚪ Member | 灰色 | 基础权限 |
| 🤖 Bot | 紫色 | 管理员 |

## Bot 命令

| 命令 | 功能 |
|------|------|
| `!help` | 命令列表 |
| `!pricing` | 定价 |
| `!models` | 支持模型 |
| `!status` | 服务状态 |
| `!docs` | API文档 |
| `!register` | 注册指引 |
| `!balance` | 余额查询 |
| `!support` | 技术支持 |

## 快速部署

### 1. 创建 Discord Bot

1. 访问 https://discord.com/developers/applications
2. 点击 "New Application"，命名为 "OLETOKEN Bot"
3. 进入 Bot 页面 → Reset Token → 复制 Token
4. 开启 Privileged Gateway Intents:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. OAuth2 → URL Generator:
   - Scopes: `bot`, `applications.commands`
   - Permissions: Manage Channels, Manage Roles, Send Messages, Embed Links, Read Message History, Add Reactions, Kick Members, Ban Members
6. 复制生成的 URL，在浏览器中打开
7. 选择你的 Discord 服务器，授权

### 2. 创建 Discord 服务器

1. 在 Discord 中创建新服务器，命名为 "OLETOKEN 中转站"
2. 开启开发者模式 (用户设置 → 高级 → 开发者模式)
3. 右键服务器图标 → 复制服务器 ID (Guild ID)

### 3. 设置 GitHub Secrets

在 https://github.com/JetragonRider/oletoken-discord/settings/secrets/actions 添加:

| Secret 名称 | 值 |
|-------------|---|
| `DISCORD_TOKEN` | 你的 Bot Token |
| `GUILD_ID` | 服务器 ID |
| `OLETOKEN_API_URL` | API地址 (如 https://api.oletoken.gg) |
| `OLETOKEN_SITE_URL` | 官网地址 (如 https://oletoken.gg) |

### 4. 运行初始化

1. 访问 https://github.com/JetragonRider/oletoken-discord/actions
2. 选择 "Setup OLETOKEN Discord Server" workflow
3. 点击 "Run workflow" → 选择 `full_setup`
4. 等待运行完成 (~1分钟)

### 5. 启动 Bot

1. 选择 "Run OLETOKEN Bot" workflow
2. 点击 "Run workflow"
3. Bot 将 24/7 运行 (每6小时自动重启)

## 文件说明

| 文件 | 说明 |
|------|------|
| `setup_server.py` | 一次性初始化脚本 (创建频道/身份组/权限) |
| `bot.py` | 24/7 运行的 Discord Bot |
| `requirements.txt` | Python 依赖 |
| `.github/workflows/setup.yml` | 初始化 GitHub Actions |
| `.github/workflows/run-bot.yml` | Bot 运行 GitHub Actions |

## 自动化功能

✅ 自动创建 7 个分类 + 25+ 频道
✅ 自动创建 6 个身份组 (管理员/版主/开发者/VIP/会员/Bot)
✅ 管理区频道仅管理组可见
✅ 自动发布: 欢迎公告/社区规则/定价说明/模型列表
✅ 新成员自动欢迎 (DM + 频道)
✅ 新成员自动分配 Member 身份组
✅ FAQ 命令系统 (!help, !pricing, !models 等)
✅ 关键词自动回复
✅ 7x24 运行 (GitHub Actions, 每6小时重启)

## 技术栈

- Python 3.11
- Discord API v10 (REST + Gateway WebSocket)
- GitHub Actions (CI/CD + 24/7 运行)
- 无第三方 Bot 库依赖 (纯标准库 + websocket-client)
