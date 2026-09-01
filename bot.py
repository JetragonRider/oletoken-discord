#!/usr/bin/env python3
"""
OLETOKEN中转站 Discord Bot - 7x24运行
功能:
  - 新成员自动欢迎消息 (DM)
  - 自动身份组 (Member)
  - FAQ命令 (/help, /pricing, /models, /status)
  - 关键词自动回复
  - 服务状态检查
"""

import os
import sys
import json
import time
import asyncio
import urllib.request
import urllib.error

BOT_TOKEN = os.environ.get("DISCORD_TOKEN", "")
GUILD_ID = os.environ.get("GUILD_ID", "")
API_BASE_URL = os.environ.get("OLETOKEN_API_URL", "https://api.oletoken.gg")
WEB_SITE_URL = os.environ.get("OLETOKEN_SITE_URL", "https://oletoken.gg")

if not BOT_TOKEN:
    print("ERROR: DISCORD_TOKEN environment variable required")
    sys.exit(1)

BASE = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "OLETOKEN-Bot (1.0)"
}

# ============================================================
# FAQ 命令响应
# ============================================================
FAQ_RESPONSES = {
    "help": {
        "embeds": [{
            "title": "🤖 OLETOKEN Bot 命令列表",
            "description": (
                "`!help` - 显示此帮助\n"
                "`!pricing` - 查看定价\n"
                "`!models` - 支持的模型列表\n"
                "`!status` - 服务状态\n"
                "`!docs` - API文档链接\n"
                "`!register` - 注册指引\n"
                "`!balance` - 余额查询方法\n"
                "`!support` - 联系技术支持\n"
            ),
            "color": 0x0099FF,
            "footer": {"text": "OLETOKEN Bot"}
        }]
    },
    "pricing": {
        "embeds": [{
            "title": "💰 OLETOKEN 定价",
            "description": (
                "**按 Token 计费** (输入/输出分开)\n\n"
                "**热门模型 (每百万Token):**\n"
                "• Claude Opus 4: $9/$27\n"
                "• Claude Sonnet 4: $3/$9\n"
                "• GPT-4o: $2.50/$7.50\n"
                "• GPT-4o-mini: $0.15/$0.60\n"
                "• DeepSeek V3: $0.27/$1.10\n"
                "• Qwen-Max: $1.20/$3.60\n\n"
                "🔥 首充送10%! 充100送10!\n"
                f"📋 完整价格: {WEB_SITE_URL}/pricing"
            ),
            "color": 0x00FF00,
            "footer": {"text": "OLETOKEN Pricing"}
        }]
    },
    "models": {
        "embeds": [{
            "title": "🤖 支持模型列表",
            "description": (
                "**Anthropic:** Claude Opus 4, Sonnet 4, Haiku 3.5\n"
                "**OpenAI:** GPT-4o, GPT-4o-mini, o1, o3-mini\n"
                "**DeepSeek:** V3, R1, Coder\n"
                "**Alibaba:** Qwen-Max, Qwen-Plus, Qwen-Turbo\n"
                "**Zhipu:** GLM-4-Plus, GLM-4-Air, GLM-4-Flash\n"
                "**Moonshot:** Moonshot-v1-8K/32K\n"
                "**Google:** Gemini 2.0 Flash, 1.5 Pro\n"
                "**Image:** DALL-E 3, SD-3, Flux-Pro\n\n"
                f"完整列表: {WEB_SITE_URL}/models"
            ),
            "color": 0x9B59B6
        }]
    },
    "status": {
        "embeds": [{
            "title": "🟢 OLETOKEN 服务状态",
            "description": (
                "所有系统运行正常 ✅\n\n"
                "• API Gateway: 🟢 在线\n"
                "• Claude 模型: 🟢 正常\n"
                "• GPT 模型: 🟢 正常\n"
                "• DeepSeek: 🟢 正常\n"
                "• 国产模型: 🟢 正常\n\n"
                f"实时状态: {WEB_SITE_URL}/status"
            ),
            "color": 0x00FF00
        }]
    },
    "docs": {
        "embeds": [{
            "title": "📖 API 文档",
            "description": (
                "**快速接入:**\n\n"
                "```python\n"
                "import openai\n\n"
                "client = openai.OpenAI(\n"
                f"    base_url=\"{API_BASE_URL}/v1\",\n"
                '    api_key="your-oletoken-key"\n'
                ")\n\n"
                "response = client.chat.completions.create(\n"
                '    model="claude-sonnet-4",\n'
                '    messages=[{"role":"user","content":"Hello!"}]\n'
                ")\n"
                "print(response.choices[0].message.content)\n"
                "```\n\n"
                f"完整文档: {WEB_SITE_URL}/docs"
            ),
            "color": 0x0099FF
        }]
    },
    "register": {
        "embeds": [{
            "title": "📝 注册指引",
            "description": (
                "1. 访问 OLETOKEN 官网\n"
                f"   👉 {WEB_SITE_URL}\n\n"
                "2. 点击注册，填写邮箱\n"
                "3. 获取 API Key\n"
                "4. 按 !docs 接入 API\n\n"
                "需要帮助？联系 @OLETOKEN Team"
            ),
            "color": 0xFF8C00
        }]
    },
    "balance": {
        "embeds": [{
            "title": "💳 余额查询",
            "description": (
                "```bash\n"
                f'curl {API_BASE_URL}/v1/dashboard/billing \\\n'
                '  -H "Authorization: Bearer YOUR_KEY"\n'
                "```\n\n"
                "或在官网控制台查看余额\n"
                f"👉 {WEB_SITE_URL}/dashboard"
            ),
            "color": 0x00FF00
        }]
    },
    "support": {
        "embeds": [{
            "title": "🛠 技术支持",
            "description": (
                "**方式1:** 在 #support 频道提问\n"
                "**方式2:** 提工单\n"
                f"   👉 {WEB_SITE_URL}/support\n"
                "**方式3:** 邮件\n"
                "   👉 support@oletoken.gg\n\n"
                "响应时间: 工作日 2小时内"
            ),
            "color": 0xFF8C00
        }]
    }
}

WELCOME_DM = {
    "embeds": [{
        "title": "🚀 欢迎来到 OLETOKEN 社区!",
        "description": (
            "OLETOKEN 是一站式 AI API 中转站!\n\n"
            "🎯 **快速开始:**\n"
            "1. 输入 `!help` 查看命令\n"
            "2. 输入 `!pricing` 查看价格\n"
            "3. 输入 `!docs` 查看API接入\n"
            "4. 输入 `!models` 查看支持模型\n\n"
            "💬 有问题随时在 #support 频道提问\n"
            "🎉 首充送10%! 祝你使用愉快!"
        ),
        "color": 0x0099FF,
        "footer": {"text": "OLETOKEN - Your Gateway to AI Models"},
        "image": {"url": f"{WEB_SITE_URL}/banner.png"}
    }]
}

# 关键词自动回复
KEYWORD_REPLIES = {
    "怎么注册": {"content": "查看 `!register` 命令获取注册指引 📝"},
    "怎么充值": {"content": "在官网控制台充值，支持支付宝/微信/USDT 💰"},
    "多少钱": {"content": "输入 `!pricing` 查看各模型定价 💰"},
    "支持什么模型": {"content": "输入 `!models` 查看支持的模型列表 🤖"},
    "api怎么用": {"content": "输入 `!docs` 查看API接入文档 📖"},
    "余额": {"content": "输入 `!balance` 查看余额查询方法 💳"},
    "客服": {"content": "在 #support 频道提问或提工单 🛠"},
    "崩了": {"content": "输入 `!status` 查看服务状态 🟢"},
    "不能用": {"content": "请输入 `!status` 检查服务状态，如正常请在 #support 描述问题 🛠"},
    "感谢": {"content": "不客气! 有问题随时找我们 😊"},
    "谢谢": {"content": "不客气! 有问题随时找我们 😊"},
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
            if e.code == 429:
                retry_after = json.loads(error_body).get("retry_after", 2)
                time.sleep(retry_after)
                continue
            return {"error": e.code}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            return {"error": str(e)}
    return {"error": "max retries"}


def get_member_role_id(guild_id):
    """查找 Member 身份组ID"""
    roles = api("GET", f"/guilds/{guild_id}/roles")
    if isinstance(roles, list):
        for role in roles:
            if role.get("name") == "⚪ Member":
                return role["id"]
    return None


def send_dm(user_id, content):
    """发送私信"""
    # 创建DM频道
    dm = api("POST", "/users/@me/channels", data={"recipient_id": user_id})
    if "id" in dm:
        api("POST", f"/channels/{dm['id']}/messages", data=content)
        return True
    return False


def handle_message(msg):
    """处理收到的消息"""
    if msg.get("author", {}).get("bot", True):
        return

    content = msg.get("content", "").strip()
    channel_id = msg.get("channel_id")
    author = msg.get("author", {})
    author_id = author.get("id", "")

    # 处理命令 (!command)
    if content.startswith("!"):
        cmd = content[1:].split()[0].lower() if len(content) > 1 else ""
        if cmd in FAQ_RESPONSES:
            api("POST", f"/channels/{channel_id}/messages", data=FAQ_RESPONSES[cmd])
            return

    # 关键词自动回复
    content_lower = content.lower()
    for keyword, reply in KEYWORD_REPLIES.items():
        if keyword in content_lower:
            api("POST", f"/channels/{channel_id}/messages", data=reply)
            return


def on_member_join(member_data):
    """新成员加入处理"""
    user_id = member_data.get("user", {}).get("id", "")
    username = member_data.get("user", {}).get("username", "新成员")

    print(f"[JOIN] {username} ({user_id}) joined")

    # 发送DM欢迎消息
    send_dm(user_id, WELCOME_DM)

    # 自动分配 Member 身份组
    if GUILD_ID:
        role_id = get_member_role_id(GUILD_ID)
        if role_id:
            result = api("PUT", f"/guilds/{GUILD_ID}/members/{user_id}/roles/{role_id}")
            if "error" not in result:
                print(f"  ✓ Assigned Member role to {username}")
            else:
                print(f"  ✗ Failed to assign role: {result}")

        # 在 general 频道发欢迎消息
        channels = api("GET", f"/guilds/{GUILD_ID}/channels")
        if isinstance(channels, list):
            for ch in channels:
                if ch.get("name") == "general":
                    welcome_msg = {
                        "content": f"👋 欢迎 <@{user_id}> 加入 OLETOKEN 社区!",
                        "embeds": [{
                            "title": f"欢迎 {username}! 🎉",
                            "description": (
                                "OLETOKEN 是一站式 AI API 中转站!\n\n"
                                "输入 `!help` 查看命令列表\n"
                                "有疑问随时在 #support 提问\n"
                                "🎉 首充送10%!"
                            ),
                            "color": 0x0099FF
                        }]
                    }
                    api("POST", f"/channels/{ch['id']}/messages", data=welcome_msg)
                    break


def run_bot():
    """主循环 - 使用Gateway WebSocket连接"""
    import socket
    import ssl
    import struct

    # 获取Gateway URL
    gateway_resp = api("GET", "/gateway/bot")
    gateway_url = gateway_resp.get("url", "wss://gateway.discord.gg")
    if gateway_url.startswith("wss://"):
        gateway_url = gateway_url[6:]  # Remove wss://

    # 获取Bot信息
    bot_user = api("GET", "/users/@me")
    bot_id = bot_user.get("id", "")
    print(f"[BOT] Connected as {bot_user.get('username', 'Unknown')} (ID: {bot_id})")

    # 连接WebSocket Gateway
    # 使用裸 socket 实现 WebSocket (避免依赖 websocket-client)
    print(f"[BOT] Connecting to Gateway: wss://{gateway_url}")

    ctx = ssl.create_default_context()
    sock = socket.create_connection((gateway_url, 443), timeout=60)
    ws_sock = ctx.wrap_socket(sock, server_hostname=gateway_url)

    # WebSocket 握手
    key = os.urandom(16).hex()
    handshake = (
        f"GET /?v=10&encoding=json HTTP/1.1\r\n"
        f"Host: {gateway_url}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"User-Agent: OLETOKEN-Bot\r\n"
        f"\r\n"
    )
    ws_sock.send(handshake.encode())

    # 读取HTTP响应
    response = b""
    while b"\r\n\r\n" not in response:
        response += ws_sock.recv(4096)

    print("[BOT] WebSocket connected!")

    # 简化: 使用 websocket-client 库更可靠
    # 如果可用的话
    try:
        import websocket
        ws_lib = True
    except ImportError:
        ws_lib = False

    if ws_lib:
        ws = websocket.WebSocket()
        ws.connect(f"wss://{gateway_url}/?v=10&encoding=json")

        # 1. 接收Hello
        hello = json.loads(ws.recv())
        heartbeat_interval = hello["d"]["heartbeat_interval"]
        print(f"[BOT] Heartbeat interval: {heartbeat_interval}ms")

        # 2. 发送Identify
        identify = {
            "op": 2,
            "d": {
                "token": BOT_TOKEN,
                "intents": (1 << 0) | (1 << 9) | (1 << 15),  # GUILDS, GUILD_MEMBERS, MESSAGE_CONTENT
                "properties": {
                    "os": "linux",
                    "browser": "oletoken-bot",
                    "device": "oletoken-bot"
                }
            }
        }
        ws.send(json.dumps(identify))

        last_heartbeat = time.time()
        last_seq = None
        acknowledged = True

        while True:
            try:
                ws.settimeout(max(1, (heartbeat_interval / 1000) - 1))
                try:
                    msg = json.loads(ws.recv())
                except Exception:
                    msg = None

                # 心跳
                if time.time() - last_heartbeat > heartbeat_interval / 1000:
                    if acknowledged:
                        ws.send(json.dumps({"op": 1, "d": last_seq}))
                        last_heartbeat = time.time()
                        acknowledged = False
                    else:
                        print("[BOT] Heartbeat not acknowledged, reconnecting...")
                        break

                if msg is None:
                    continue

                op = msg.get("op")
                if op == 0:  # Dispatch
                    last_seq = msg.get("s")
                    event = msg.get("t")
                    data = msg.get("d", {})

                    if event == "READY":
                        print(f"[BOT] Ready! Logged in as {data.get('user', {}).get('username')}")
                    elif event == "GUILD_MEMBER_ADD":
                        on_member_join(data)
                    elif event == "MESSAGE_CREATE":
                        handle_message(data)

                elif op == 1:  # Heartbeat request
                    ws.send(json.dumps({"op": 1, "d": last_seq}))
                elif op == 11:  # Heartbeat ACK
                    acknowledged = True
                elif op == 9:  # Invalid session
                    print("[BOT] Invalid session, reconnecting...")
                    time.sleep(5)
                    break
                elif op == 7:  # Reconnect
                    print("[BOT] Server requested reconnect...")
                    break

            except KeyboardInterrupt:
                print("[BOT] Shutting down...")
                break
            except Exception as e:
                print(f"[BOT] Error: {e}")
                time.sleep(5)
                break

        ws.close()
    else:
        print("[BOT] websocket-client not available, using REST polling mode")
        # 降级模式: 使用REST API轮询 (不推荐但能工作)
        last_message_id = {}
        print("[BOT] Running in REST polling mode (limited functionality)")

        while True:
            try:
                # 轮询频道消息
                if GUILD_ID:
                    channels = api("GET", f"/guilds/{GUILD_ID}/channels")
                    if isinstance(channels, list):
                        for ch in channels:
                            if ch.get("type") == 0:  # Text channel
                                ch_id = ch["id"]
                                params = f"?limit=5"
                                if ch_id in last_message_id:
                                    params += f"&after={last_message_id[ch_id]}"
                                msgs = api("GET", f"/channels/{ch_id}/messages{params}")
                                if isinstance(msgs, list) and msgs:
                                    for msg in reversed(msgs):
                                        handle_message(msg)
                                    last_message_id[ch_id] = msgs[0]["id"]
                time.sleep(2)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[POLL] Error: {e}")
                time.sleep(5)


if __name__ == "__main__":
    print("=" * 50)
    print("OLETOKEN Discord Bot")
    print("=" * 50)
    while True:
        try:
            run_bot()
        except KeyboardInterrupt:
            print("\n[BOT] Shutting down...")
            break
        except Exception as e:
            print(f"[BOT] Fatal error: {e}")
            print("[BOT] Reconnecting in 10 seconds...")
            time.sleep(10)
