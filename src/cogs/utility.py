import secrets

import discord
from discord.ext import commands
from src.utils import create_custom_embed
from src.version import __version__
from src.config import ELLEN_AVATAR_URL

BEL_VUONG_ROLE_ID = 1528100067280551956

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _build_bel_comment(self, bel_percent: float) -> tuple[str, str]:
        if bel_percent == 0:
            return "💀", "Gió thổi là bay, bộ xương di động."
        if bel_percent < 25:
            return "😌", "Mới nhú tí nọng, nhìn chung vẫn ốm nhom."
        if bel_percent < 50:
            return "🤔", "Nửa nạc nửa mỡ, bụng bắt đầu rung rinh rồi."
        if bel_percent < 75:
            return "🔥", "Tròn ủm, ngấn nào ra ngấn nấy."
        if bel_percent < 100:
            return "👀", "Mỡ tràn bờ đê, chuẩn bị lăn thay vì đi."
        return "👑", "Hệ tư tưởng xôi thịt. 100% Bel Vương!"

    async def _sync_bel_role(self, ctx, bel_percent: float):
        if not ctx.guild:
            return

        member = ctx.author
        role = ctx.guild.get_role(BEL_VUONG_ROLE_ID)
        if not role:
            return

        try:
            if bel_percent == 100:
                if role not in member.roles:
                    await member.add_roles(role, reason="Bel check đạt 100%")
            elif bel_percent == 0 and role in member.roles:
                await member.remove_roles(role, reason="Bel check đạt 0%")
        except discord.Forbidden:
            await ctx.send("⚠️ Bot không đủ quyền để chỉnh role Bel Vương.")
        except discord.HTTPException:
            await ctx.send("⚠️ Không thể cập nhật role Bel Vương lúc này.")

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

    @commands.hybrid_command(name="bel", description="Giải trí: kiểm tra mức độ bel của bạn")
    async def bel_check(self, ctx):
        bel_percent = secrets.randbelow(10001) / 100
        icon, comment = self._build_bel_comment(bel_percent)

        embed = create_custom_embed(
            title=f":pregnant_man: Bel Check: {ctx.author.name}",
            description=f"## Mức độ bel: {bel_percent:.2f}%\n{icon} {comment}",
            color=secrets.randbelow(0x1000000),
            footer_text="💫 Đạt 100% để nhận role Bel Vương"
        )

        await self._sync_bel_role(ctx, bel_percent)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))