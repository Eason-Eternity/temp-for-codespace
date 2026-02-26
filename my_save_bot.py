import os
import asyncio
import logging
from telethon import TelegramClient, events

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== 配置区 =====
API_ID = int(os.environ.get("API_ID", 38474201))
API_HASH = os.environ.get("API_HASH", "73cf36ca5463deb34d9c52723448e729")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8461479543:AAEffIOuZ8c2rjFmi-IKcSM4cKcEdc4IOmM")
SAVE_PATH = "./downloads"
# ===== 配置结束 =====

os.makedirs(SAVE_PATH, exist_ok=True)

# 创建客户端（不带代理，因为服务器在国外）
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage)
async def handler(event):
    try:
        # 只处理有文件的消息
        if event.message.file:
            file_name = event.message.file.name or f"file_{event.message.id}"
            file_size = event.message.file.size / 1024 / 1024

            await event.reply(f"📥 收到文件，正在保存 ({file_size:.2f} MB)...")

            file_path = await event.message.download_media(file=SAVE_PATH)

            await event.reply(
                f"✅ 保存成功！\n"
                f"📄 {file_name}\n"
                f"📦 {file_size:.2f} MB"
            )
            logger.info(f"已保存: {file_path}")

        # 处理 /start 命令
        elif event.message.text and event.message.text.startswith('/start'):
            await event.reply("👋 发文件给我，自动保存（支持2GB）")

    except Exception as e:
        logger.error(f"错误: {str(e)}")
        await event.reply(f"❌ 保存失败：{str(e)}")

async def main():
    logger.info("🚀 机器人启动中...")
    logger.info(f"📁 保存路径: {os.path.abspath(SAVE_PATH)}")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())