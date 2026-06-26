import discord
from telethon.tl.types import MessageEntityTextUrl, MessageEntityBold, MessageEntityItalic, MessageEntityCode
from src.config import ELLEN_AVATAR_URL

TEMP_DIR = 'temp_media'
MAX_FILE_SIZE_MB = 24 
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024 

def create_custom_embed(
    description: str,
    title: str = None, 
    color: int = 0xD7342A, 
    url: str = None,
    timestamp = None,
    image: str = None,
    thumbnail: str = None,
    author_name: str = "Ellen Joe", 
    author_icon: str = ELLEN_AVATAR_URL,
    author_url: str = None,
    footer_text: str = "Victoria Housekeeping Co.",
    footer_icon: str = None,
    fields: list = None
):
    embed = discord.Embed(
        title=title, 
        description=description, 
        color=color, 
        url=url, 
        timestamp=timestamp
    )
    
    embed.set_author(
        name=author_name, 
        icon_url=author_icon, 
        url=author_url if author_url else None
    )
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if image:
        embed.set_image(url=image)
        
    embed.set_footer(
        text=footer_text, 
        icon_url=footer_icon if footer_icon else None
    )
    
    if fields:
        for field in fields:
            embed.add_field(
                name=field.get('name', 'No Title'),
                value=field.get('value', 'No Content'),
                inline=field.get('inline', False)
            )
    
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