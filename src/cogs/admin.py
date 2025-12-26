import discord
from discord.ext import commands
from src.database import db
from src.config import TELEGRAM_SOURCES, ELLEN_AVATAR_URL

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

    @commands.command(name="remove", aliases=['stop', 'unsubscribe'])
    @commands.has_permissions(administrator=True)
    async def remove_channel(self, ctx):
        """Hủy nhận tin ở kênh hiện tại: !remove"""
        
        # Gọi hàm xóa trong database
        is_deleted = await db.remove_mapping(ctx.channel.id)
        
        if is_deleted:
            embed = discord.Embed(
                title="✅ Đã hủy đăng ký",
                description="Kênh này sẽ **không còn nhận tin nhắn** tự động nữa.",
                color=0xff0000 # Màu đỏ
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("⚠️ Kênh này chưa được setup nguồn nào cả.")

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Kiểm tra bot còn sống không: !ping"""
        # self.bot.latency trả về giây, nhân 1000 để ra mili giây
        latency = round(self.bot.latency * 1000)
        
        # Tạo Embed
        embed = discord.Embed(
            title="🦈 Shark Ping",
            description=f"Ping cái gì mà ping? Mau đưa **{latency} viên kẹo (ms)** đây 🍬🍭",
            color=0xD7342A # Màu đỏ đặc trưng (giống trong chat.py)
        )
        
        # Thêm Thumbnail (Avatar của Ellen) và Footer
        embed.set_thumbnail(url=ELLEN_AVATAR_URL)
        embed.set_footer(text="Victoria Housekeeping Co.", icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))