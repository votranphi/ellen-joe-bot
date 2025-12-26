import discord
from discord.ext import commands
from src.utils import create_ellen_embed
from src.version import __version__

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Hiển thị danh sách lệnh của Ellen: .help"""
        
        embed = create_ellen_embed(
            title="Bảng công việc (Help Menu)",
            description="Phiền phức thật đấy... Xem nhanh đi để tôi còn đi nghỉ. Đây là những gì tôi có thể làm:",
            footer_text=f"Victoria Housekeeping Co. • v{__version__} • Xong việc thì để tôi yên."
        )
        
        # Nhóm lệnh Trò chuyện
        embed.add_field(
            name="💬 Trò chuyện",
            value="`.chat <nội dung>`: Nói chuyện với tôi. Đừng hỏi mấy câu thừa thãi.",
            inline=False
        )
        
        # Nhóm lệnh Đồng bộ (Bridge)
        embed.add_field(
            name="🔗 Đồng bộ Telegram",
            value="`.setup <nguồn>`: Cấu hình kênh này nhận tin (Admin).\n`.sync <số lượng>`: Lấy lại tin cũ từ Telegram.\n`.remove`: Nghỉ việc, không nhận tin ở đây nữa.",
            inline=False
        )
        
        # Nhóm lệnh Quản trị
        embed.add_field(
            name="🛠️ Quản trị & Hệ thống",
            value="`.clean <số lượng>`: Dọn dẹp tin nhắn cho sạch sẽ.\n`.ping`: Kiểm tra xem tôi có đang ngủ gật không.",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))