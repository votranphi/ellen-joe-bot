import discord
from discord import app_commands
from discord.ext import commands
from telethon import TelegramClient, events
import os
import asyncio
import shutil
from src.config import TELEGRAM_SOURCES
from src.database import db
from src.utils import format_discord_message, TEMP_DIR, MAX_FILE_SIZE_BYTES, MAX_FILE_SIZE_MB

class TelegramBridge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_id = os.getenv('TELE_API_ID')
        self.api_hash = os.getenv('TELE_API_HASH')
        self.t_client = TelegramClient('session_bot_v2', self.api_id, self.api_hash)
        
    async def cog_load(self):
        await self.t_client.start()
        print("🔵 Telethon Client Started")
        
        self.t_client.add_event_handler(self.on_tele_message, events.NewMessage())

    async def cog_unload(self):
        await self.t_client.disconnect()

    async def forward_to_discord(self, message, discord_channel_ids):
        formatted_text = format_discord_message(message)
        
        file_path = None
        display_text = formatted_text
        
        if message.media:
            file_size = message.file.size if message.file else 0
            if file_size > MAX_FILE_SIZE_BYTES:
                display_text += f"\n\n_⚠️ [Media quá lớn (> {MAX_FILE_SIZE_MB}MB)]_"
            else:
                try:
                    if not os.path.exists(TEMP_DIR): os.makedirs(TEMP_DIR)
                    path = await message.download_media(file=TEMP_DIR)
                    if path:
                        if os.path.getsize(path) > MAX_FILE_SIZE_BYTES:
                            os.remove(path)
                            display_text += f"\n\n_⚠️ [File tải về quá lớn]_"
                        else:
                            file_path = path
                except Exception as e:
                    print(f"Lỗi tải media: {e}")

        for d_id in discord_channel_ids:
            channel = self.bot.get_channel(d_id)
            if not channel: continue
            
            source_key = await db.get_source_by_discord_id(d_id)
            source_info = TELEGRAM_SOURCES.get(source_key, {})
            
            embed = discord.Embed(
                description=display_text if display_text else "*[Chỉ có media]*",
                color=0x0088cc,
                timestamp=message.date
            )
            embed.set_author(
                name=source_info.get('name', 'Telegram Sync'),
                icon_url=source_info.get('icon_url', '')
            )
            
            discord_file = discord.File(file_path) if file_path else None
            try:
                await channel.send(content="**⸻⸻⸻**", embed=embed, file=discord_file)
            except Exception as e:
                print(f"Lỗi gửi Discord: {e}")
            finally:
                if discord_file: discord_file.close()

        if file_path:
            try: os.remove(file_path)
            except: pass

    async def on_tele_message(self, event):
        chat_id = event.chat_id
        dest_discord_ids = await db.get_discord_channels_by_tele_id(chat_id)
        
        if dest_discord_ids:
            print(f"📩 Live Sync: Tin nhắn từ {chat_id} -> {dest_discord_ids}")
            await self.forward_to_discord(event.message, dest_discord_ids)

    @commands.hybrid_command(name="sync", description="[Admin] Đồng bộ tin nhắn cũ từ Telegram sang Discord")
    @app_commands.describe(limit="Số lượng tin nhắn muốn lấy (mặc định: 5)")
    @commands.has_permissions(administrator=True)
    async def sync_history(self, ctx, limit: int = 5):
        """Đồng bộ tin nhắn cũ: .sync 5"""
        
        try:
            await ctx.message.delete()
        except:
            pass

        status_msg = await ctx.send(f"⏳ Đang đồng bộ {limit} tin nhắn gần nhất...")
        
        source_key = await db.get_source_by_discord_id(ctx.channel.id)
        
        if not source_key:
            await status_msg.edit(content="❌ Kênh này chưa được setup. Dùng lệnh `.setup <source>` trước.")
            await status_msg.delete(delay=5)
            return
            
        source_info = TELEGRAM_SOURCES.get(source_key)
        tele_id = source_info['tele_id']
        
        try:
            messages = await self.t_client.get_messages(tele_id, limit=limit)
        except Exception as e:
            await status_msg.edit(content=f"❌ Lỗi Telegram: {e}")
            await status_msg.delete(delay=10)
            return

        if not messages:
            await status_msg.edit(content="⚠️ Không tìm thấy tin nhắn nào.")
            await status_msg.delete(delay=5)
            return

        for msg in reversed(messages):
            await self.forward_to_discord(msg, [ctx.channel.id])
            await asyncio.sleep(1.5) # Delay để tránh rate limit

        await status_msg.edit(content="✅ Đồng bộ hoàn tất!")
        await status_msg.delete(delay=3)

async def setup(bot):
    await bot.add_cog(TelegramBridge(bot))