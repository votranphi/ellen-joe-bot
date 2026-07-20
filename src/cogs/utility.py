import secrets
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from src.utils import create_custom_embed
from src.version import __version__
from src.config import ELLEN_AVATAR_URL, STATUS_PROFILES

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _build_status_comment(self, percent: float, profile: dict) -> tuple[str, str]:
        if percent == 0:
            return profile["zero_icon"], profile["zero_message"]
        if percent < 25:
            return profile["low_icon"], profile["low_message"]
        if percent < 50:
            return profile["mid_icon"], profile["mid_message"]
        if percent < 75:
            return profile["high_icon"], profile["high_message"]
        if percent < 100:
            return profile["near_max_icon"], profile["near_max_message"]
        return profile["max_icon"], profile["max_message"]

    async def _sync_reward_role(self, ctx, member: discord.Member, percent: float, profile: dict):
        if not ctx.guild:
            return

        role_id = profile["role_id"]
        role = ctx.guild.get_role(role_id) if role_id else None
        if not role:
            return

        try:
            if percent == 100:
                if role not in member.roles:
                    await member.add_roles(role, reason=f'{profile["display_name"]} check đạt 100%')
            elif percent == 0 and role in member.roles:
                await member.remove_roles(role, reason=f'{profile["display_name"]} check đạt 0%')
        except discord.Forbidden:
            await ctx.send(f'⚠️ Bot không đủ quyền để chỉnh role {profile["display_name"]}.')
        except discord.HTTPException:
            await ctx.send(f'⚠️ Không thể cập nhật role {profile["display_name"]} lúc này.')

    async def _run_status_check(self, ctx, profile_key: str, member: Optional[discord.Member] = None):
        profile = STATUS_PROFILES[profile_key]
        target = member or ctx.author
        percent = secrets.randbelow(10001) / 100
        icon, comment = self._build_status_comment(percent, profile)
        value_label = profile["value_label"]
        is_self_check = target.id == ctx.author.id
        footer_text = profile["self_footer"] if is_self_check else profile["other_footer"]

        embed = create_custom_embed(
            title=f'{profile["title_prefix"]}: {target.name}',
            description=f'## Mức độ {value_label}: {percent:.2f}%\n{icon} {comment}',
            color=secrets.randbelow(0x1000000),
            footer_text=footer_text
        )

        if is_self_check:
            await self._sync_reward_role(ctx, target, percent, profile)
        await ctx.send(embed=embed)

    ### COMMANDS SECTION BEGINS HERE ###

    @commands.hybrid_command(name="ping", description="Kiểm tra độ trễ kết nối của bot")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        
        embed = create_custom_embed(
            title="🦈 Shark Ping",
            description=f"Ping cái gì mà ping? Mau đưa **{latency} viên kẹo** đây 🍬🍭",
            color=0xff0000, # red
            thumbnail=ELLEN_AVATAR_URL
        )
        
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version", aliases=['v'], description="Hiển thị phiên bản hiện tại của bot")
    async def version(self, ctx):
        embed = create_custom_embed(
            title="📋 Phiên bản hệ thống",
            description=f"Tôi đang chạy phiên bản **v{__version__}**\n\nHỏi làm gì? Đừng phiền tôi nữa.",
            color=0xff0000, # red
            thumbnail=ELLEN_AVATAR_URL
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="bel", description="Kiểm tra mức độ bel của bạn hoặc người khác")
    @app_commands.describe(member="Người muốn check mức độ bel")
    async def bel_check(self, ctx, member: Optional[discord.Member] = None):
        await self._run_status_check(ctx, "bel", member)

    @commands.hybrid_command(name="goon", description="Kiểm tra mức độ lọ của bạn hoặc người khác")
    @app_commands.describe(member="Người muốn check mức độ lọ")
    async def goon_check(self, ctx, member: Optional[discord.Member] = None):
        await self._run_status_check(ctx, "goon", member)

    @commands.hybrid_command(name="dam", description="Kiểm tra mức độ dâm của bạn hoặc người khác")
    @app_commands.describe(member="Người muốn check mức độ dâm")
    async def dam_check(self, ctx, member: Optional[discord.Member] = None):
        await self._run_status_check(ctx, "dam", member)

async def setup(bot):
    await bot.add_cog(Utility(bot))