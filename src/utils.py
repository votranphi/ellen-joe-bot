import os
import discord
from telethon.tl.types import MessageEntityTextUrl, MessageEntityBold, MessageEntityItalic, MessageEntityCode
from src.config import ELLEN_AVATAR_URL

TEMP_DIR = 'temp_media'
MAX_FILE_SIZE_MB = 24 
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024 

def create_ellen_embed(title=None, description=None, color=0xD7342A, footer_text="Victoria Housekeeping Co."):
    """
    Create a standardized Discord Embed for Ellen Joe.
    
    Args:
        title (str, optional): The embed title
        description (str, optional): The embed description
        color (int, optional): The embed color. Defaults to 0xD7342A (Ellen's red)
        footer_text (str, optional): The footer text. Defaults to "Victoria Housekeeping Co."
    
    Returns:
        discord.Embed: A configured embed with Ellen's branding
    """
    # Create embed with optional title and description
    if title and description:
        embed = discord.Embed(title=title, description=description, color=color)
    elif title:
        embed = discord.Embed(title=title, color=color)
    elif description:
        embed = discord.Embed(description=description, color=color)
    else:
        embed = discord.Embed(color=color)
    
    # Set Ellen's author info
    embed.set_author(name="Ellen Joe", icon_url=ELLEN_AVATAR_URL)
    
    # Set Ellen's thumbnail
    embed.set_thumbnail(url=ELLEN_AVATAR_URL)
    
    # Set footer
    embed.set_footer(text=footer_text)
    
    return embed

def format_discord_message(message):
    text = message.message or ""
    if not message.entities:
        return text

    entities = sorted(message.entities, key=lambda x: x.offset, reverse=True)
    for entity in entities:
        offset = entity.offset
        length = entity.length
        chunk = text[offset : offset + length]
        
        if isinstance(entity, MessageEntityTextUrl):
            text = text[:offset] + f"[{chunk}]({entity.url})" + text[offset + length:]
        elif isinstance(entity, MessageEntityBold):
            text = text[:offset] + f"**{chunk}**" + text[offset + length:]
        elif isinstance(entity, MessageEntityItalic):
            text = text[:offset] + f"*{chunk}*" + text[offset + length:]
        elif isinstance(entity, MessageEntityCode):
            text = text[:offset] + f"`{chunk}`" + text[offset + length:]
            
    return text