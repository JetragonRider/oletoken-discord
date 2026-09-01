#!/usr/bin/env python3
"""
OLEToken Discord Community - English Setup
Rename categories, update channel topics, re-post announcements in English.
"""
import os, json, time, urllib.request, urllib.error

BOT_TOKEN = os.environ.get("DISCORD_TOKEN", "")
GUILD_ID = os.environ.get("GUILD_ID", "")

if not BOT_TOKEN or not GUILD_ID:
    print("ERROR: DISCORD_TOKEN and GUILD_ID required")
    exit(1)

BASE = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "OLEToken-Bot (1.0)"
}

def api(method, path, data=None, retries=3):
    url = f"{BASE}{path}"
    body = json.dumps(data).encode() if data else None
    for _ in range(retries):
        req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return {} if resp.status == 204 else json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(json.loads(e.read()).get("retry_after", 2))
                continue
            return {"error": e.code}
        except Exception as e:
            return {"error": str(e)}
    return {"error": "rate limited"}

# Category name mappings (Chinese -> English)
CATEGORY_MAP = {
    "信息中心": "Information",
    "服务状态": "Service Status",
    "文档与指南": "Docs & Guides",
    "社区交流": "Community",
    "开发者": "Developers",
    "管理区": "Staff Only",
}

# Channel topic mappings (English topics)
CHANNEL_TOPICS = {
    "announcements": "Official announcements - new features, updates, important notices",
    "rules": "Community rules - please read and follow",
    "faq": "Frequently asked questions",
    "service-status": "Real-time service status - uptime, maintenance, incidents",
    "maintenance": "Scheduled maintenance notifications",
    "api-docs": "API documentation - base_url, authentication, request format",
    "tutorials": "Tutorials - from registration to your first API call",
    "pricing": "Pricing - model price comparison per million tokens",
    "models-list": "Supported models - Claude, GPT, DeepSeek, Qwen, GLM and more",
    "general": "General discussion - free chat",
    "tech-talk": "Tech talk - API usage, performance, best practices",
    "support": "Support - describe your issue here",
    "suggestions": "Suggestions - your ideas matter",
    "api-integration": "API integration - Python, Node, Go, Java",
    "sdk-code": "SDK and code snippets",
    "showcase": "Showcase - projects built with OLEToken",
    "admin": "Admin discussion (staff only)",
    "audit-log": "Audit log (staff only)",
    "bot-commands": "Bot commands channel",
    "welcome": "Welcome to OLEToken community",
}

# English announcement embeds
WELCOME_EMBED = {
    "title": "Welcome to OLEToken Community!",
    "description": (
        "OLEToken is your all-in-one AI API relay station.\n\n"
        "**Why OLEToken?**\n"
        "- Unified API for all major AI models\n"
        "- Transparent pricing, 30-50% cheaper than official\n"
        "- 99.9% uptime guarantee\n"
        "- 24/7 technical support\n\n"
        "**Quick Start:**\n"
        "1. Check #api-docs for integration guide\n"
        "2. See #pricing for model prices\n"
        "3. Ask questions in #support\n"
        "4. Chat in #general\n\n"
        "Please read #rules first!"
    ),
    "color": 0x0099FF,
    "footer": {"text": "OLEToken - Your Gateway to AI Models"}
}

RULES_EMBED = {
    "title": "OLEToken Community Rules",
    "description": (
        "**1. Be Respectful** - No harassment, discrimination, or personal attacks\n\n"
        "**2. No Ads** - No promoting other relay stations or competitors\n\n"
        "**3. Stay Secure** - Never share API keys, tokens, or sensitive info\n\n"
        "**4. Search First** - Check #faq and #api-docs before asking\n\n"
        "**5. No Abuse** - No bulk requests, DDoS, or vulnerability scanning\n\n"
        "**6. Appropriate Content** - No illegal, NSFW, or violent content\n\n"
        "**7. Use Right Channel** - Issues in #support, ideas in #suggestions\n\n"
        "**8. Language** - English and Chinese both welcome\n\n"
        "Violations may result in warning or ban. Admins reserve final say."
    ),
    "color": 0xFF8C00,
    "footer": {"text": "Last updated: 2026-09-01 | OLEToken Team"}
}

PRICING_EMBED = {
    "title": "OLEToken Pricing",
    "description": (
        "**Pay-per-token** (input/output billed separately)\n\n"
        "**Popular Models (per 1M tokens):**\n"
        "| Model | Input ($) | Output ($) |\n"
        "|-------|----------|------------|\n"
        "| Claude Opus 4 | 9.00 | 27.00 |\n"
        "| Claude Sonnet 4 | 3.00 | 9.00 |\n"
        "| GPT-4o | 2.50 | 7.50 |\n"
        "| GPT-4o-mini | 0.15 | 0.60 |\n"
        "| DeepSeek V3 | 0.27 | 1.10 |\n"
        "| Qwen-Max | 1.20 | 3.60 |\n"
        "| GLM-4-Plus | 0.50 | 1.50 |\n\n"
        "**Bonuses:** First deposit +10%, deposit 100 get 10 extra\n"
        "**Balance check:** `GET /v1/dashboard/billing`"
    ),
    "color": 0x00FF00,
    "footer": {"text": "Prices subject to change | Check actual billing"}
}

MODELS_EMBED = {
    "title": "OLEToken Supported Models",
    "description": (
        "**Anthropic**\n"
        "claude-opus-4, claude-sonnet-4, claude-haiku-3.5\n\n"
        "**OpenAI**\n"
        "gpt-4o, gpt-4o-mini, o1, o1-mini, o3-mini\n\n"
        "**DeepSeek**\n"
        "deepseek-v3, deepseek-r1, deepseek-coder\n\n"
        "**Alibaba**\n"
        "qwen-max, qwen-plus, qwen-turbo\n\n"
        "**Zhipu AI**\n"
        "glm-4-plus, glm-4-air, glm-4-flash\n\n"
        "**Moonshot**\n"
        "moonshot-v1-8k, moonshot-v1-32k\n\n"
        "**Google**\n"
        "gemini-2.0-flash, gemini-1.5-pro\n\n"
        "**Image**\n"
        "dall-e-3, stable-diffusion-3, flux-pro\n\n"
        "More models coming soon..."
    ),
    "color": 0x9B59B6,
    "footer": {"text": "Full list in API docs | OLEToken"}
}


def run_english_setup():
    print("=" * 50)
    print("OLEToken English Setup")
    print("=" * 50)

    # Get all channels
    channels = api("GET", f"/guilds/{GUILD_ID}/channels")
    if not isinstance(channels, list):
        print(f"Failed to get channels: {channels}")
        return

    # 1. Rename categories to English
    print("\n[1/4] Renaming categories to English...")
    for ch in channels:
        if ch.get("type") == 4:  # Category
            old_name = ch.get("name", "")
            new_name = None
            for cn, en in CATEGORY_MAP.items():
                if cn in old_name:
                    # Keep emoji prefix
                    emoji = old_name.split(cn)[0] if cn in old_name else ""
                    new_name = f"{emoji}{en}"
                    break
            if new_name and new_name != old_name:
                result = api("PATCH", f"/channels/{ch['id']}", data={"name": new_name})
                if "error" not in result:
                    print(f"  {old_name} -> {new_name}")
                time.sleep(0.5)

    # 2. Update channel topics to English
    print("\n[2/4] Updating channel topics to English...")
    for ch in channels:
        if ch.get("type") == 0:  # Text channel
            ch_name = ch.get("name", "")
            if ch_name in CHANNEL_TOPICS:
                new_topic = CHANNEL_TOPICS[ch_name]
                if ch.get("topic") != new_topic:
                    result = api("PATCH", f"/channels/{ch['id']}", data={"topic": new_topic})
                    if "error" not in result:
                        print(f"  #{ch_name} topic updated")
                    time.sleep(0.3)

    # 3. Re-post announcements in English
    print("\n[3/4] Re-posting announcements in English...")
    # Refresh channel list
    channels = api("GET", f"/guilds/{GUILD_ID}/channels")
    if isinstance(channels, list):
        for ch in channels:
            if ch.get("name") == "welcome":
                # Clear and re-post welcome
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [WELCOME_EMBED]})
                print("  Welcome message posted")
            elif ch.get("name") == "rules":
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [RULES_EMBED]})
                print("  Rules message posted")
            elif ch.get("name") == "pricing":
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [PRICING_EMBED]})
                print("  Pricing message posted")
            elif ch.get("name") == "models-list":
                api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [MODELS_EMBED]})
                print("  Models list posted")
            time.sleep(0.5)

    # 4. Try to set bot nickname
    print("\n[4/4] Setting bot nickname...")
    bot_info = api("GET", "/users/@me")
    bot_id = bot_info.get("id", "")
    nick = api("PATCH", f"/guilds/{GUILD_ID}/members/{bot_id}", data={"nick": "OLEToken Bot"})
    if "error" not in nick:
        print("  Bot nickname -> OLEToken Bot")
    else:
        print(f"  Nickname failed (change app name in Developer Portal)")

    # 5. Post completion announcement
    for ch in channels if isinstance(channels, list) else []:
        if ch.get("name") == "announcements":
            api("POST", f"/channels/{ch['id']}/messages", data={"embeds": [{
                "title": "OLEToken Community Setup Complete!",
                "description": (
                    "OLEToken Discord community is now fully set up!\n\n"
                    "**Created:**\n"
                    "- 7 categories, 22 channels\n"
                    "- 6 roles (Team, Moderator, Developer, VIP, Member, Bot)\n"
                    "- Rules, pricing, and model list announcements\n\n"
                    "**Bot Commands:**\n"
                    "`!help` `!pricing` `!models` `!status` `!docs`\n\n"
                    "Welcome to OLEToken!"
                ),
                "color": 0x00FF00,
                "footer": {"text": "OLEToken Bot"}
            }]})
            print("  Completion announcement posted")
            break

    print("\n" + "=" * 50)
    print("English setup complete!")
    print("=" * 50)


if __name__ == "__main__":
    run_english_setup()
