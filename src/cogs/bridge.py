import discord
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
        # Khởi tạo Telethon Client
        self.api_id = os.getenv('TELE_API_ID')
        self.api_hash = os.getenv('TELE_API_HASH')
        self.t_client = TelegramClient('session_bot_v2', self.api_id, self.api_hash)
        
    async def cog_load(self):
        # Khởi động Telethon khi Cog load
        await self.t_client.start()
        print("🔵 Telethon Client Started")
        
        # Đăng ký sự kiện lắng nghe tin mới (Live Listener)
        self.t_client.add_event_handler(self.on_tele_message, events.NewMessage())

    async def cog_unload(self):
        await self.t_client.disconnect()

    # --- HÀM XỬ LÝ CHUNG: GỬI 1 TIN SANG DISCORD ---
    async def forward_to_discord(self, message, discord_channel_ids):
        # Xử lý text
        formatted_text = format_discord_message(message)
        
        # Xử lý media
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

        # Gửi sang các kênh Discord đích
        for d_id in discord_channel_ids:
            channel = self.bot.get_channel(d_id)
            if not channel: continue
            
            # Lấy info nguồn để set Author/Icon (Cần query ngược lại từ DB hoặc truyền vào)
            # Ở đây ta lấy tạm thông tin từ message gốc hoặc config global nếu có thể
            # Để đơn giản, ta sẽ lấy info từ mapping DB (nếu cần tối ưu có thể cache)
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

        # Cleanup file
        if file_path:
            try: os.remove(file_path)
            except: pass

    # --- 1. LIVE LISTENER (Tự động) ---
    async def on_tele_message(self, event):
        chat_id = event.chat_id
        # Tìm xem Telegram ID này có được map với kênh Discord nào không
        dest_discord_ids = await db.get_discord_channels_by_tele_id(chat_id)
        
        if dest_discord_ids:
            print(f"📩 Live Sync: Tin nhắn từ {chat_id} -> {dest_discord_ids}")
            await self.forward_to_discord(event.message, dest_discord_ids)

    # --- 2. COMMAND SYNC (Thủ công) ---
    @commands.command(name="sync")
    @commands.has_permissions(administrator=True)
    async def sync_history(self, ctx, limit: int = 5):
        """Đồng bộ tin nhắn cũ: !sync 5"""
        await ctx.send(f"⏳ Đang đồng bộ {limit} tin nhắn gần nhất...")
        
        # 1. Xác định kênh hiện tại đang map với nguồn nào
        source_key = await db.get_source_by_discord_id(ctx.channel.id)
        
        if not source_key:
            await ctx.send("❌ Kênh này chưa được setup. Dùng lệnh `!setup <source>` trước.")
            return
            
        source_info = TELEGRAM_SOURCES.get(source_key)
        tele_id = source_info['tele_id']
        
        # 2. Lấy tin nhắn từ Telegram
        try:
            messages = await self.t_client.get_messages(tele_id, limit=limit)
        except Exception as e:
            await ctx.send(f"❌ Lỗi Telegram: {e}")
            return

        if not messages:
            await ctx.send("⚠️ Không tìm thấy tin nhắn nào.")
            return

        # 3. Gửi tin (Dùng lại hàm forward_to_discord nhưng chỉ cho kênh hiện tại)
        for msg in reversed(messages):
            await self.forward_to_discord(msg, [ctx.channel.id])
            await asyncio.sleep(1.5) # Delay để tránh rate limit

        await ctx.send("✅ Đồng bộ hoàn tất!")

async def setup(bot):
    await bot.add_cog(TelegramBridge(bot))