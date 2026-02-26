import os
import asyncio
from telethon import TelegramClient, events

# ===== 配置区 =====
API_ID = 38474201
API_HASH = '73cf36ca5463deb34d9c52723448e729'
PHONE_NUMBER = '+8619822307092'
SAVE_PATH = './downloads'

# 代理配置（用 Clash/V2Ray 的 HTTP 端口）
proxy = ('http', '127.0.0.1', 7890)  # 换成 http  # 元组格式：(协议, 地址, 端口)
# ===== 配置结束 =====

os.makedirs(SAVE_PATH, exist_ok=True)

# 创建客户端，明确传入 proxy 参数
client = TelegramClient(
    'my_save_session',
    API_ID,
    API_HASH,
    proxy=proxy  # 这一行必须有
)

@client.on(events.NewMessage)
async def handler(event):
    try:
        if not event.out:
            return

        if event.message.media:
            # 获取文件名
            if hasattr(event.message.media, 'document'):
                doc = event.message.media.document
                file_name = None
                for attr in doc.attributes:
                    if hasattr(attr, 'file_name'):
                        file_name = attr.file_name
                        break
                if not file_name:
                    file_name = f"document_{doc.id}.bin"
                file_size = doc.size / 1024 / 1024
            elif hasattr(event.message.media, 'photo'):
                file_name = f"photo_{event.message.id}.jpg"
                file_size = 0
            else:
                return

            print(f"📥 收到: {file_name} ({file_size:.2f} MB)")
            file_path = await event.message.download_media(file=SAVE_PATH)
            await event.reply(f"✅ 已保存: {file_name}")
            print(f"✅ 已保存: {file_path}")

    except Exception as e:
        print(f"❌ 错误: {str(e)}")

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("👋 发文件给我，自动保存（支持2GB）")

async def main():
    print("🚀 机器人启动中...")
    print(f"📁 保存路径: {os.path.abspath(SAVE_PATH)}")
    print(f"🌐 代理: {proxy[0]}://{proxy[1]}:{proxy[2]}")
    
    await client.start(phone=PHONE_NUMBER)
    print("✅ 登录成功！等待消息...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
