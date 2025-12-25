import os
from telethon.tl.types import MessageEntityTextUrl, MessageEntityBold, MessageEntityItalic, MessageEntityCode

TEMP_DIR = 'temp_media'
MAX_FILE_SIZE_MB = 24 
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024 

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