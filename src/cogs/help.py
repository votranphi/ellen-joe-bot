import discord
from discord.ext import commands
from src.config import ELLEN_AVATAR_URL

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Hiển thị danh sách lệnh của Ellen: .help"""
        
        embed = discord.Embed(
            title="Bảng công việc (Help Menu)",
            description="Phiền phức thật đấy... Xem nhanh đi để tôi còn đi nghỉ. Đây là những gì tôi có thể làm:",
            color=0xD7342A # Màu đỏ đặc trưng của Victoria Housekeeping
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

        # Trang trí theo phong cách Ellen
        embed.set_author(name="Ellen Joe", icon_url=ELLEN_AVATAR_URL)
        embed.set_thumbnail(url=ELLEN_AVATAR_URL)
        embed.set_footer(text="Victoria Housekeeping Co. • Xong việc thì để tôi yên.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))