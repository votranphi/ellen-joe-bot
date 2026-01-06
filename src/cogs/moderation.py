import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
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
            limit = amount + 1 # Tính cả tin nhắn gọi lệnh nếu dùng prefix
        
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"🧹 Đã dọn {amount} tin nhắn.", delete_after=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))