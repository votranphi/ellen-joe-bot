from discord.ext import commands
from src.utils import create_custom_embed
from src.version import __version__
from src.config import ELLEN_AVATAR_URL

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Kiểm tra độ trễ kết nối của bot")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        
        embed = create_custom_embed(
            description=f"Ping cái gì mà ping? Mau đưa **{latency} viên kẹo** đây 🍬🍭",
            title="🦈 Shark Ping",
            thumbnail=ELLEN_AVATAR_URL
        )
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version", aliases=['v'], description="Hiển thị phiên bản hiện tại của bot")
    async def version(self, ctx):
        embed = create_custom_embed(
            description=f"Tôi đang chạy phiên bản **v{__version__}**\n\nHỏi làm gì? Đi làm việc đi, đừng phiền tôi nữa.",
            title="📋 Phiên bản hệ thống",
            thumbnail=ELLEN_AVATAR_URL
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))