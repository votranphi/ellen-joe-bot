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
            return "💀", "Bel cạn sạch rồi, đúng nghĩa không còn một chút nào."
        if bel_percent < 25:
            return "😌", "Mức này còn rất thấp, chưa đủ để gọi là bel."
        if bel_percent < 50:
            return "🤔", "Có dấu hiệu rồi đó, nhưng vẫn còn khá xa để thành bel thực thụ."
        if bel_percent < 75:
            return "🔥", "Khá rõ mùi bel, tiếp tục là sẽ lên rất nhanh."
        if bel_percent < 100:
            return "👀", "Gần chạm ngưỡng cuối rồi, chỉ còn một bước nữa thôi."
        return "👑", "100% bel vương xác nhận. Không còn gì để bàn cãi nữa."

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
            await ctx.send("⚠️ Bot không đủ quyền để chỉnh role Bel vương.")
        except discord.HTTPException:
            await ctx.send("⚠️ Không thể cập nhật role Bel vương lúc này.")

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
            footer_text=":dizzy: Đạt 100% để nhận role Bel vương"
        )

        await self._sync_bel_role(ctx, bel_percent)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))