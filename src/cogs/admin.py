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

    @commands.hybrid_command(name="clean", description="[Admin Only] Dọn dẹp tin nhắn trong kênh")
    @app_commands.describe(amount="Số lượng tin nhắn cần xóa")
    @commands.has_permissions(administrator=True)
    async def clean_messages(self, ctx, amount: int):
        """Dọn dẹp tin nhắn: .clean 10"""
        await ctx.channel.purge(limit=amount + 1) # +1 để xóa luôn câu lệnh clean
        msg = await ctx.send(f"🧹 Đã dọn {amount} tin nhắn.")
        await msg.delete(delay=3)

    @commands.hybrid_command(name="setup", description="[Admin Only] Cấu hình kênh này nhận tin từ nguồn Telegram")
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

        # Lưu vào MongoDB
        await db.set_mapping(ctx.channel.id, source_key, source_info['tele_id'])
        
        embed = discord.Embed(
            title="✅ Setup Thành Công",
            description=f"Kênh này sẽ nhận tin từ: **{source_info['name']}**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=source_info['icon_url'])
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="remove", aliases=['stop', 'unsubscribe'], description="[Admin Only] Hủy nhận tin tự động ở kênh hiện tại")
    @commands.has_permissions(administrator=True)
    async def remove_channel(self, ctx):
        """Hủy nhận tin ở kênh hiện tại: .remove"""
        
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

    @commands.hybrid_command(name="ping", description="Kiểm tra độ trễ kết nối của bot")
    async def ping(self, ctx):
        """Kiểm tra bot còn sống không: .ping"""
        # self.bot.latency trả về giây, nhân 1000 để ra mili giây
        latency = round(self.bot.latency * 1000)
        
        # Tạo Embed
        embed = create_ellen_embed(
            title="🦈 Shark Ping",
            description=f"Ping cái gì mà ping? Mau đưa **{latency} viên kẹo** đây 🍬🍭"
        )
        
        # Note: The footer icon is intentionally not added as the helper uses a standard footer
        # If you need the bot avatar in footer, you can manually override:
        # embed.set_footer(text="Victoria Housekeeping Co.", icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version", aliases=['v'], description="Hiển thị phiên bản hiện tại của bot")
    async def version(self, ctx):
        """Kiểm tra phiên bản bot: .version hoặc .v"""
        embed = create_ellen_embed(
            title="📋 Phiên bản hệ thống",
            description=f"Tôi đang chạy phiên bản **v{__version__}**\n\nHỏi làm gì? Đi làm việc đi, đừng phiền tôi nữa."
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="synctree", description="[Admin Only] Đồng bộ slash commands lên Discord")
    @commands.has_permissions(administrator=True)
    async def sync_tree(self, ctx):
        """Đồng bộ command tree lên Discord - chỉ dành cho admin"""
        await ctx.defer()  # Defer vì sync có thể mất thời gian
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