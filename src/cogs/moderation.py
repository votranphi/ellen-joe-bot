import asyncio
import discord
from discord import app_commands
from discord.ext import commands

from src.database import db
from src.utils import create_custom_embed

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sticky_locks = {}

    def _get_sticky_lock(self, channel_id):
        if channel_id not in self.sticky_locks:
            self.sticky_locks[channel_id] = asyncio.Lock()
        return self.sticky_locks[channel_id]

    async def _replace_sticky_message(self, channel, config=None):
        channel_id = channel.id
        async with self._get_sticky_lock(channel_id):
            current_config = await db.get_sticky_message(channel_id)
            if config is None:
                config = current_config
            if not config:
                return

            old_message_id = current_config.get("message_id") if current_config else None
            if old_message_id:
                try:
                    old_message = await channel.fetch_message(old_message_id)
                    await old_message.delete()
                except (discord.NotFound, discord.Forbidden):
                    pass

            if config["message_type"] == "embed":
                embed = create_custom_embed(**config["embed"])
                sticky_message = await channel.send(embed=embed)
            else:
                sticky_message = await channel.send(config["content"])

            await db.set_sticky_message(
                channel_id=channel_id,
                message_id=sticky_message.id,
                message_type=config["message_type"],
                content=config.get("content"),
                embed=config.get("embed")
            )

    async def _remove_sticky_message(self, channel):
        channel_id = channel.id
        async with self._get_sticky_lock(channel_id):
            config = await db.get_sticky_message(channel_id)
            if not config:
                return False

            message_id = config.get("message_id")
            if message_id:
                try:
                    message = await channel.fetch_message(message_id)
                    await message.delete()
                except (discord.NotFound, discord.Forbidden):
                    pass

            await db.remove_sticky_message(channel_id)
            return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        await self._replace_sticky_message(message.channel)

    ########################################
    ##### COMMANDS SECTION BEGINS HERE #####
    ########################################

    @commands.hybrid_command(name="clean", description="[Manage Messages] Dọn dẹp tin nhắn trong kênh")
    @app_commands.describe(amount="Số lượng tin nhắn cần xóa")
    @commands.has_permissions(manage_messages=True)
    async def clean_messages(self, ctx, amount: int):
        await ctx.defer(ephemeral=True)
        if ctx.interaction:
            limit = amount
        else:
            limit = amount + 1 # If using prefix, there must be an additional message to be deleted
        
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"🧹 Đã dọn {amount} tin nhắn.", delete_after=3)

    @commands.hybrid_command(name="say", description="[Manage Messages] Gửi tin nhắn dạng Embed")
    @app_commands.describe(
        description="Nội dung tin nhắn (Markdown)",
        title="Tiêu đề (Optional)",
        image="Link ảnh lớn nằm dưới (Optional)",
        thumbnail="Link ảnh nhỏ góc phải (Optional)",
        color="Mã màu Hex, ví dụ: 00FF00 (Optional)"
    )
    @commands.has_permissions(manage_messages=True)
    async def say_embed(self, ctx, description: str, title: str = None, image: str = None, thumbnail: str = None, color: str = None):
        embed_color = 0xFF0000
        if color:
            try:
                embed_color = int(color.replace("#", ""), 16)
            except ValueError:
                pass

        embed = create_custom_embed(
            description=description,
            title=title,
            color=embed_color,
            image=image,
            thumbnail=thumbnail
        )

        try:
            if ctx.message:
                await ctx.message.delete()
        except discord.HTTPException:
            pass

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="setup-sticky-message", description="[Manage Messages] Ghim một tin nhắn ở cuối kênh")
    @app_commands.describe(message="Nội dung tin nhắn sticky (Markdown)")
    @commands.has_permissions(manage_messages=True)
    async def sticky_message(self, ctx, message: str):
        config = {
            "message_type": "text",
            "content": message,
            "embed": None
        }

        if ctx.interaction:
            await ctx.defer(ephemeral=True)

        try:
            if ctx.message:
                await ctx.message.delete()
        except discord.HTTPException:
            pass

        await self._replace_sticky_message(ctx.channel, config)
        if ctx.interaction:
            await ctx.send("✅ Đã thiết lập sticky message cho kênh này.", ephemeral=True)
        else:
            await ctx.send("✅ Đã thiết lập sticky message cho kênh này.", delete_after=3)

    @commands.hybrid_command(name="setup-sticky-embed", description="[Manage Messages] Ghim một embed ở cuối kênh")
    @app_commands.describe(
        description="Nội dung tin nhắn (Markdown)",
        title="Tiêu đề (Optional)",
        image="Link ảnh lớn nằm dưới (Optional)",
        thumbnail="Link ảnh nhỏ góc phải (Optional)",
        color="Mã màu Hex, ví dụ: 00FF00 (Optional)"
    )
    @commands.has_permissions(manage_messages=True)
    async def sticky_embed_message(self, ctx, description: str, title: str = None, image: str = None, thumbnail: str = None, color: str = None):
        embed_color = 0xFF0000
        if color:
            try:
                embed_color = int(color.replace("#", ""), 16)
            except ValueError:
                pass

        config = {
            "message_type": "embed",
            "content": None,
            "embed": {
                "description": description,
                "title": title,
                "color": embed_color,
                "image": image,
                "thumbnail": thumbnail
            }
        }

        if ctx.interaction:
            await ctx.defer(ephemeral=True)

        try:
            if ctx.message:
                await ctx.message.delete()
        except discord.HTTPException:
            pass

        await self._replace_sticky_message(ctx.channel, config)
        if ctx.interaction:
            await ctx.send("✅ Đã thiết lập sticky embed message cho kênh này.", ephemeral=True)
        else:
            await ctx.send("✅ Đã thiết lập sticky embed message cho kênh này.", delete_after=3)

    @commands.hybrid_command(name="remove-sticky", description="[Manage Messages] Xóa sticky message khỏi kênh")
    @commands.has_permissions(manage_messages=True)
    async def remove_sticky_message(self, ctx):
        if ctx.interaction:
            await ctx.defer(ephemeral=True)

        try:
            if ctx.message:
                await ctx.message.delete()
        except discord.HTTPException:
            pass

        removed = await self._remove_sticky_message(ctx.channel)
        response = (
            "✅ Đã xóa sticky message khỏi kênh này."
            if removed
            else "ℹ️ Kênh này hiện không có sticky message."
        )

        if ctx.interaction:
            await ctx.send(response, ephemeral=True)
        else:
            await ctx.send(response, delete_after=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))