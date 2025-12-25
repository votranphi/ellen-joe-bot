import discord
from discord.ext import commands
from src.database import db
from src.config import TELEGRAM_SOURCES

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clean")
    @commands.has_permissions(manage_messages=True)
    async def clean_messages(self, ctx, amount: int):
        """Dọn dẹp tin nhắn: !clean 10"""
        await ctx.channel.purge(limit=amount + 1) # +1 để xóa luôn câu lệnh clean
        msg = await ctx.send(f"🧹 Đã dọn {amount} tin nhắn.")
        await msg.delete(delay=3)

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_channel(self, ctx, source_key: str = None):
        """Setup kênh hiện tại nhận tin từ nguồn nào: !setup nens"""
        if not source_key:
            sources = ", ".join([f"`{k}`" for k in TELEGRAM_SOURCES.keys()])
            await ctx.send(f"⚠️ Vui lòng chọn nguồn. Các nguồn hiện có: {sources}")
            return

        source_info = TELEGRAM_SOURCES.get(source_key)
        if not source_info:
            await ctx.send("❌ Nguồn không tồn tại.")
            return

        if not source_info['tele_id']:
            await ctx.send("❌ Nguồn này chưa được cấu hình ID trong .env")
            return

        # Lưu vào MongoDB
        await db.set_mapping(ctx.channel.id, source_key, source_info['tele_id'])
        
        embed = discord.Embed(
            title="✅ Setup Thành Công",
            description=f"Kênh này sẽ nhận tin từ: **{source_info['name']}**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=source_info['icon_url'])
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))