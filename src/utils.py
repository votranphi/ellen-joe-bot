import discord
from telethon.tl.types import MessageEntityTextUrl, MessageEntityBold, MessageEntityItalic, MessageEntityCode

TEMP_DIR = 'temp_media'
MAX_FILE_SIZE_MB = 24 
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024 

def create_custom_embed(
    description: str,
    title: str = None, 
    color: int = None, 
    url: str = None,
    timestamp = None,
    image: str = None,
    thumbnail: str = None,
    author_name: str = None, 
    author_icon: str = None,
    author_url: str = None,
    footer_text: str = None,
    footer_icon: str = None,
    fields: list = None
):
    embed_kwargs = {
        "title": title,
        "description": description,
        "url": url,
        "timestamp": timestamp,
    }

    if color is not None:
        embed_kwargs["color"] = color

    embed = discord.Embed(**embed_kwargs)

    if author_name is not None or author_icon is not None or author_url is not None:
        embed.set_author(
            name=author_name or "\u200b",
            icon_url=author_icon,
            url=author_url if author_url else None
        )
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if image:
        embed.set_image(url=image)
        
    if footer_text is not None or footer_icon is not None:
        embed.set_footer(
            text=footer_text or "\u200b",
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