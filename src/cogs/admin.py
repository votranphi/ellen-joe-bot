import discord
from discord import app_commands
from discord.ext import commands
from src.database import db
from src.config import TELEGRAM_SOURCES
from src.utils import create_ellen_embed
from src.version import __version__

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="clean", description="[Manage Messages] Dọn dẹp tin nhắn trong kênh")
    @app_commands.describe(amount="Số lượng tin nhắn cần xóa")
    @commands.has_permissions(manage_messages=True)
    async def clean_messages(self, ctx, amount: int):
        """Dọn dẹp tin nhắn: .clean 10"""
        await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🧹 Đã dọn {amount} tin nhắn.")
        await msg.delete(delay=3)

    @commands.hybrid_command(name="setup", description="[Admin] Cấu hình kênh này nhận tin từ nguồn Telegram")
    @app_commands.describe(source_key="Mã nguồn (nens, hiragara, seele)")
    @commands.has_permissions(administrator=True)
    async def setup_channel(self, ctx, source_key: str = None):
        """Setup kênh hiện tại nhận tin từ nguồn nào: .setup nens"""
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

        await db.set_mapping(ctx.channel.id, source_key, source_info['tele_id'])
        
        embed = discord.Embed(
            title="✅ Setup Thành Công",
            description=f"Kênh này sẽ nhận tin từ: **{source_info['name']}**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=source_info['icon_url'])
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="remove", aliases=['stop', 'unsubscribe'], description="[Admin] Hủy nhận tin tự động ở kênh hiện tại")
    @commands.has_permissions(administrator=True)
    async def remove_channel(self, ctx):
        """Hủy nhận tin ở kênh hiện tại: .remove"""
        
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

    @commands.hybrid_command(name="ping", description="Kiểm tra độ trễ kết nối của bot")
    async def ping(self, ctx):
        """Kiểm tra bot còn sống không: .ping"""
        latency = round(self.bot.latency * 1000)
        
        # Tạo Embed
        embed = create_ellen_embed(
            title="🦈 Shark Ping",
            description=f"Ping cái gì mà ping? Mau đưa **{latency} viên kẹo** đây 🍬🍭"
        )
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="say", description="[Admin] Gửi tin nhắn dạng Embed (hỗ trợ Markdown & Ảnh)")
    @app_commands.describe(
        content="Nội dung tin nhắn (Markdown)",
        title="Tiêu đề (Optional)",
        image="Link ảnh lớn nằm dưới (Optional)",
        thumbnail="Link ảnh nhỏ góc phải (Optional - Ghi đè ảnh Ellen)",
        color="Mã màu Hex, ví dụ: 00FF00 (Optional)"
    )
    @commands.has_permissions(administrator=True)
    async def say_embed(self, ctx, content: str, title: str = None, image: str = None, thumbnail: str = None, color: str = None):
        """Chuyển tin nhắn thành Embed: .say "Nội dung" title="Tiêu đề" ..."""
        
        embed_color = 0xD7342A
        if color:
            try:
                embed_color = int(color.replace("#", ""), 16)
            except ValueError:
                pass

        embed = create_ellen_embed(
            title=title, 
            description=content, 
            color=embed_color
        )

        if image:
            embed.set_image(url=image)
        
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        try:
            await ctx.message.delete()
        except:
            pass

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version", aliases=['v'], description="Hiển thị phiên bản hiện tại của bot")
    async def version(self, ctx):
        """Kiểm tra phiên bản bot: .version hoặc .v"""
        embed = create_ellen_embed(
            title="📋 Phiên bản hệ thống",
            description=f"Tôi đang chạy phiên bản **v{__version__}**\n\nHỏi làm gì? Đi làm việc đi, đừng phiền tôi nữa."
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="synctree", description="[Admin] Đồng bộ slash commands lên Discord")
    @commands.has_permissions(administrator=True)
    async def sync_tree(self, ctx):
        """Đồng bộ command tree lên Discord - chỉ dành cho admin"""
        await ctx.defer()
        try:
            synced = await self.bot.tree.sync()
            embed = create_ellen_embed(
                title="✅ Tree Sync Hoàn Tất",
                description=f"Đã đồng bộ **{len(synced)}** slash commands lên Discord.\n\nSlash commands sẽ xuất hiện sau vài giây."
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = create_ellen_embed(
                title="❌ Lỗi Sync Tree",
                description=f"Không thể đồng bộ: {str(e)}"
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))