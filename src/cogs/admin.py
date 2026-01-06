import discord
from discord import app_commands
from discord.ext import commands
from src.database import db
from src.config import TELEGRAM_SOURCES
from src.utils import create_custom_embed
from src.version import __version__
from src.config import ELLEN_AVATAR_URL

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="clean", description="[Manage Messages] Dọn dẹp tin nhắn trong kênh")
    @app_commands.describe(amount="Số lượng tin nhắn cần xóa")
    @commands.has_permissions(manage_messages=True)
    async def clean_messages(self, ctx, amount: int):
        await ctx.defer(ephemeral=True)
        if ctx.interaction:
            limit = amount
        else:
            limit = amount + 1
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"🧹 Đã dọn {amount} tin nhắn.", delete_after=3)

    @commands.hybrid_command(name="setup", description="[Admin] Cấu hình kênh này nhận tin từ nguồn Telegram")
    @app_commands.describe(source_key="Mã nguồn (nens, hiragara, seele)")
    @commands.has_permissions(administrator=True)
    async def setup_channel(self, ctx, source_key: str = None):
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
        
        embed = create_custom_embed(
            title="✅ Setup Thành Công",
            description=f"Kênh này sẽ nhận tin từ: **{source_info['name']}**",
            color=0x00ff00,
            thumbnail=source_info['icon_url']
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="remove", aliases=['stop', 'unsubscribe'], description="[Admin] Hủy nhận tin tự động ở kênh hiện tại")
    @commands.has_permissions(administrator=True)
    async def remove_channel(self, ctx):
        is_deleted = await db.remove_mapping(ctx.channel.id)
        
        if is_deleted:
            embed = create_custom_embed(
                title="✅ Đã hủy đăng ký",
                description="Kênh này sẽ **không còn nhận tin nhắn** tự động nữa.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("⚠️ Kênh này chưa được setup nguồn nào cả.")

    @commands.hybrid_command(name="ping", description="Kiểm tra độ trễ kết nối của bot")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        
        embed = create_custom_embed(
            description=f"Ping cái gì mà ping? Mau đưa **{latency} viên kẹo** đây 🍬🍭",
            title="🦈 Shark Ping",
            thumbnail=ELLEN_AVATAR_URL
        )
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="say", description="[Admin] Gửi tin nhắn dạng Embed")
    @app_commands.describe(
        content="Nội dung tin nhắn (Markdown)",
        title="Tiêu đề (Optional)",
        image="Link ảnh lớn nằm dưới (Optional)",
        thumbnail="Link ảnh nhỏ góc phải (Optional)",
        color="Mã màu Hex, ví dụ: 00FF00 (Optional)"
    )
    @commands.has_permissions(administrator=True)
    async def say_embed(self, ctx, content: str, title: str = None, image: str = None, thumbnail: str = None, color: str = None):
        embed_color = 0xD7342A
        if color:
            try:
                embed_color = int(color.replace("#", ""), 16)
            except ValueError:
                pass

        embed = create_custom_embed(
            description=content,
            title=title, 
            color=embed_color,
            image=image,
            thumbnail=thumbnail
        )
        kwargs = {
            "description": content,
            "title": title,
            "color": embed_color,
            "image": image
        }
        if thumbnail:
            kwargs["thumbnail"] = thumbnail
            
        embed = create_custom_embed(**kwargs)


        try:
            await ctx.message.delete()
        except:
            pass

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version", aliases=['v'], description="Hiển thị phiên bản hiện tại của bot")
    async def version(self, ctx):
        embed = create_custom_embed(
            description=f"Tôi đang chạy phiên bản **v{__version__}**\n\nHỏi làm gì? Đi làm việc đi, đừng phiền tôi nữa.",
            title="📋 Phiên bản hệ thống",
            thumbnail=ELLEN_AVATAR_URL
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="synctree", description="[Admin] Đồng bộ slash commands lên Discord")
    @commands.has_permissions(administrator=True)
    async def sync_tree(self, ctx):
        await ctx.defer()
        try:
            synced = await self.bot.tree.sync()
            embed = create_custom_embed(
                description=f"Đã đồng bộ **{len(synced)}** slash commands lên Discord.\n\nSlash commands sẽ xuất hiện sau vài giây.",
                title="✅ Tree Sync Hoàn Tất"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = create_custom_embed(
                description=f"Không thể đồng bộ: {str(e)}",
                title="❌ Lỗi Sync Tree"
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot))