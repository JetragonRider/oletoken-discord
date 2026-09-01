#!/usr/bin/env python3
"""
OLETOKEN中转站 Discord社区 - 服务器初始化脚本
一次性运行: 创建分类、频道、身份组、权限、规则公告
使用 Discord Bot API (REST), 不需要长连接
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

BOT_TOKEN = os.environ.get("DISCORD_TOKEN", "")
GUILD_ID = os.environ.get("GUILD_ID", "")

if not BOT_TOKEN or not GUILD_ID:
    print("ERROR: DISCORD_TOKEN and GUILD_ID environment variables required")
    sys.exit(1)

BASE = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "OLEToken-Bot (1.0)"
}

def api(method, path, data=None, max_retries=3):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode() if data else None
    for attempt in range(max_retries):
        req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            if resp.status == 204:
                return {}
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            if e.code == 429:  # Rate limited
                retry_after = json.loads(error_body).get("retry_after", 2)
                print(f"  Rate limited, waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            print(f"  HTTP {e.code}: {error_body[:200]}")
            if attempt < max_retries - 1:
                time.sleep(2)
            return {"error": e.code, "body": error_body[:500]}
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            return {"error": str(e)}
    return {"error": "max retries exceeded"}

# ============================================================
# 身份组配置 (Role Configuration)
# ============================================================
ROLES = [
    {
        "name": "🔴 OLETOKEN Team",
        "color": 0xFF0000,
        "permissions": 0x1FEDC9DF,  # Administrator
        "hoist": True,
        "mentionable": False
    },
    {
        "name": "🟠 Moderator",
        "color": 0xFF8C00,
        "permissions": 0x1FEDC9CF,  # Manage channels, roles, kick, ban, etc
        "hoist": True,
        "mentionable": True
    },
    {
        "name": "🟢 Developer",
        "color": 0x00FF00,
        "permissions": 0x00000010,  # Send messages + basic
        "hoist": True,
        "mentionable": True
    },
    {
        "name": "🔵 VIP Member",
        "color": 0x0099FF,
        "permissions": 0x00000000,
        "hoist": True,
        "mentionable": True
    },
    {
        "name": "⚪ Member",
        "color": 0xAAAAAA,
        "permissions": 0x00000000,
        "hoist": False,
        "mentionable": False
    },
    {
        "name": "🤖 OLEToken Bot",
        "color": 0x5865F2,
        "permissions": 0x1FEDC9DF,
        "hoist": False,
        "mentionable": False
    }
]

# ============================================================
# 分类和频道配置
# ============================================================
CATEGORIES = [
    {
        "name": "📢 信息中心",
        "channels": [
            {"name": "announcements", "type": 0, "topic": "OLETOKEN官方公告 - 新功能/更新/重要通知"},
            {"name": "rules", "type": 0, "topic": "社区规则 - 请所有成员阅读并遵守"},
            {"name": "faq", "type": 0, "topic": "常见问题解答"}
        ]
    },
    {
        "name": "🟢 服务状态",
        "channels": [
            {"name": "service-status", "type": 0, "topic": "实时服务状态 - 上线/维护/故障通知"},
            {"name": "maintenance", "type": 0, "topic": "计划维护通知"}
        ]
    },
    {
        "name": "📖 文档与指南",
        "channels": [
            {"name": "api-docs", "type": 0, "topic": "API接入文档 - base_url/认证/请求格式"},
            {"name": "tutorials", "type": 0, "topic": "使用教程 - 从注册到调用"},
            {"name": "pricing", "type": 0, "topic": "定价说明 - 各模型价格对比"},
            {"name": "models-list", "type": 0, "topic": "支持模型列表 - Claude/GPT/DeepSeek/Qwen/GLM等"}
        ]
    },
    {
        "name": "💬 社区交流",
        "channels": [
            {"name": "general", "type": 0, "topic": "综合讨论 - 自由聊天"},
            {"name": "tech-talk", "type": 0, "topic": "技术交流 - API使用/性能/最佳实践"},
            {"name": "support", "type": 0, "topic": "问题反馈 - 遇到问题请在此描述"},
            {"name": "suggestions", "type": 0, "topic": "功能建议 - 你的想法很重要"}
        ]
    },
    {
        "name": "💻 开发者",
        "channels": [
            {"name": "api-integration", "type": 0, "topic": "API接入讨论 - Python/Node/Go/Java"},
            {"name": "sdk-code", "type": 0, "topic": "SDK与代码片段分享"},
            {"name": "showcase", "type": 0, "topic": "项目展示 - 用OLETOKEN搭建的项目"}
        ]
    },
    {
        "name": "🔒 管理区",
        "channels": [
            {"name": "admin", "type": 0, "topic": "管理讨论 (仅管理组)"},
            {"name": "audit-log", "type": 0, "topic": "审核记录 (仅管理组)"},
            {"name": "bot-commands", "type": 0, "topic": "机器人命令频道"}
        ],
        "staff_only": True
    }
]

# ============================================================
# 规则公告内容
# ============================================================
WELCOME_EMBED = {
    "title": "🚀 欢迎来到 OLETOKEN 中转站社区!",
    "description": (
        "OLETOKEN 是一站式 AI API 中转站，支持 Claude、GPT、DeepSeek、Qwen、GLM 等主流模型。\n\n"
        "🔥 **为什么选择 OLETOKEN?**\n"
        "• 统一 API 接口，一个 key 调用所有模型\n"
        "• 透明定价，比官方便宜 30-50%\n"
        "• 99.9% 可用性保证\n"
        "• 7x24 技术支持\n\n"
        "📋 **快速开始:**\n"
        "1. 访问 #api-docs 查看接入文档\n"
        "2. 在 #pricing 查看定价\n"
        "3. 有问题去 #support 提问\n"
        "4. 在 #general 和大家交流\n\n"
        "⚠️ 请先阅读 #rules 中的社区规则"
    ),
    "color": 0x0099FF,
    "footer": {"text": "OLETOKEN - Your Gateway to AI Models"}
}

RULES_EMBED = {
    "title": "📋 OLETOKEN 社区规则",
    "description": (
        "**1. 尊重他人** - 禁止人身攻击、歧视、骚扰\n\n"
        "**2. 禁止广告** - 未经允许禁止推广其他中转站或竞品\n\n"
        "**3. 安全使用** - 禁止分享 API Key、Token 等敏感信息\n\n"
        "**4. 合理提问** - 先看 #faq 和 #api-docs，再提问\n\n"
        "**5. 禁止滥用** - 禁止批量请求、DDoS、漏洞扫描\n\n"
        "**6. 内容合规** - 禁止违规、色情、暴力内容\n\n"
        "**7. 反馈渠道** - 问题请发 #support，建议请发 #suggestions\n\n"
        "**8. 语言** - 中文/英文均可，请互相理解\n\n"
        "违反规则将被警告或封禁。管理员保留最终解释权。"
    ),
    "color": 0xFF8C00,
    "footer": {"text": "最后更新: 2026-09-01 | OLETOKEN Team"}
}

PRICING_EMBED = {
    "title": "💰 OLETOKEN 定价说明",
    "description": (
        "**定价模式:** 按 Token 计费 (输入/输出分开计价)\n\n"
        "**热门模型价格 (每百万Token):**\n\n"
        "| 模型 | 输入 ($) | 输出 ($) |\n"
        "|------|---------|----------|\n"
        "| Claude Opus 4 | 9.00 | 27.00 |\n"
        "| Claude Sonnet 4 | 3.00 | 9.00 |\n"
        "| GPT-4o | 2.50 | 7.50 |\n"
        "| GPT-4o-mini | 0.15 | 0.60 |\n"
        "| DeepSeek V3 | 0.27 | 1.10 |\n"
        "| Qwen-Max | 1.20 | 3.60 |\n"
        "| GLM-4-Plus | 0.50 | 1.50 |\n\n"
        "💡 **充值优惠:** 首充送10%，充100送10\n"
        "📊 **详细价格:** 见 #models-list 频道\n"
        "🔄 **余额查询:** 调用 `/v1/dashboard/billing`"
    ),
    "color": 0x00FF00,
    "footer": {"text": "价格随时更新 | 以实际扣费为准"}
}

MODELS_EMBED = {
    "title": "🤖 OLETOKEN 支持模型列表",
    "description": (
        "**Anthropic**\n"
        "• claude-opus-4, claude-sonnet-4, claude-haiku-3.5\n\n"
        "**OpenAI**\n"
        "• gpt-4o, gpt-4o-mini, o1, o1-mini, o3-mini\n\n"
        "**DeepSeek**\n"
        "• deepseek-v3, deepseek-r1, deepseek-coder\n\n"
        "**Alibaba**\n"
        "• qwen-max, qwen-plus, qwen-turbo\n\n"
        "**Zhipu AI**\n"
        "• glm-4-plus, glm-4-air, glm-4-flash\n\n"
        "**Moonshot**\n"
        "• moonshot-v1-8k, moonshot-v1-32k\n\n"
        "**Google**\n"
        "• gemini-2.0-flash, gemini-1.5-pro\n\n"
        "**Image Models**\n"
        "• dall-e-3, stable-diffusion-3, flux-pro\n\n"
        "更多模型持续接入中..."
    ),
    "color": 0x9B59B6,
    "footer": {"text": "完整列表见 API文档 | OLETOKEN"}
}


def setup_server():
    print("=" * 60)
    print("OLETOKEN Discord 社区初始化")
    print("=" * 60)

    # 1. 创建身份组
    print("\n[1/4] 创建身份组...")
    role_ids = {}
    for role in ROLES:
        result = api("POST", f"/guilds/{GUILD_ID}/roles", data=role)
        if "id" in result:
            role_ids[role["name"]] = result["id"]
            print(f"  ✓ {role['name']} (ID: {result['id']})")
        else:
            print(f"  ✗ {role['name']}: {result}")
        time.sleep(0.5)

    staff_role_id = role_ids.get("🟠 Moderator", "")
    team_role_id = role_ids.get("🔴 OLETOKEN Team", "")

    # 2. 创建分类和频道
    print("\n[2/4] 创建分类和频道...")
    for category in CATEGORIES:
        # 创建分类
        cat_data = {"name": category["name"], "type": 4}
        if category.get("staff_only") and staff_role_id:
            cat_data["permission_overwrites"] = [
                {
                    "id": GUILD_ID,
                    "type": 0,  # role
                    "deny": 0x400,  # VIEW_CHANNEL
                },
                {
                    "id": staff_role_id,
                    "type": 0,
                    "allow": 0x400,
                }
            ]
            if team_role_id:
                cat_data["permission_overwrites"].append({
                    "id": team_role_id,
                    "type": 0,
                    "allow": 0x400,
                })

        cat_result = api("POST", f"/guilds/{GUILD_ID}/channels", data=cat_data)
        cat_id = cat_result.get("id", "")
        if cat_id:
            print(f"  📁 {category['name']} (ID: {cat_id})")
        else:
            print(f"  ✗ {category['name']}: {cat_result}")
            continue

        time.sleep(0.5)

        # 创建频道
        for ch in category["channels"]:
            ch_data = {
                "name": ch["name"],
                "type": ch["type"],
                "topic": ch.get("topic", ""),
                "parent_id": cat_id
            }

            # 管理区频道额外权限
            if category.get("staff_only") and staff_role_id:
                ch_data["permission_overwrites"] = [
                    {"id": GUILD_ID, "type": 0, "deny": 0x400},
                    {"id": staff_role_id, "type": 0, "allow": 0x400},
                ]
                if team_role_id:
                    ch_data["permission_overwrites"].append(
                        {"id": team_role_id, "type": 0, "allow": 0x400}
                    )

            ch_result = api("POST", f"/guilds/{GUILD_ID}/channels", data=ch_data)
            if "id" in ch_result:
                print(f"    #{ch['name']} (ID: {ch_result['id']})")
            else:
                print(f"    ✗ #{ch['name']}: {ch_result}")
            time.sleep(0.5)

    # 3. 发送公告内容
    print("\n[3/4] 发布公告内容...")

    # 公告频道发欢迎消息
    welcome_result = api("POST", f"/guilds/{GUILD_ID}/channels",
                         data={"name": "welcome", "type": 0, "topic": "欢迎来到OLETOKEN社区", "parent_id": ""})
    if "id" in welcome_result:
        api("POST", f"/channels/{welcome_result['id']}/messages",
            data={"embeds": [WELCOME_EMBED]})
        print("  ✓ 欢迎公告已发布")

    # 规则频道
    channels = api("GET", f"/guilds/{GUILD_ID}/channels")
    if isinstance(channels, list):
        for ch in channels:
            if ch.get("name") == "rules":
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [RULES_EMBED]})
                print("  ✓ 规则公告已发布")
            elif ch.get("name") == "pricing":
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [PRICING_EMBED]})
                print("  ✓ 定价公告已发布")
            elif ch.get("name") == "models-list":
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [MODELS_EMBED]})
                print("  ✓ 模型列表已发布")
            time.sleep(0.5)

    # 4. 设置系统频道 (欢迎消息)
    print("\n[4/4] 配置系统设置...")
    # 设置社区频道的欢迎消息
    api("PATCH", f"/guilds/{GUILD_ID}", data={
        "system_channel_flags": 0,  # Enable join notifications
    })
    print("  ✓ 系统频道已配置")

    # 输出频道ID映射
    print("\n" + "=" * 60)
    print("✅ 初始化完成!")
    print("=" * 60)
    print(f"\n身份组ID映射:")
    for name, rid in role_ids.items():
        print(f"  {name}: {rid}")

    # 保存配置到文件
    config = {"roles": role_ids, "guild_id": GUILD_ID}
    with open("server_config.json", "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("\n配置已保存到 server_config.json")


if __name__ == "__main__":
    setup_server()
