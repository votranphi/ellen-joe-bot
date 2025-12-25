import os
from dotenv import load_dotenv

load_dotenv()

def get_env_int(key):
    val = os.getenv(key)
    return int(val) if val and val.lstrip('-').isdigit() else None

# Danh sách các nguồn có thể Setup
# Key: Tên định danh dùng trong lệnh !setup
TELEGRAM_SOURCES = {
    'nens': {
        'tele_id': get_env_int('TELE_NENS_CHANNEL_ID'),
        'name': 'New Eridu News Stand',
        'icon_url': 'https://static.icy-veins.com/images/zenless-zone-zero/og-images/howls-newsstand.webp'
    },
    'seele': {
        'tele_id': get_env_int('TELE_SL_CHANNEL_ID'),
        'name': 'Seele Leaks',
        'icon_url': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRqGTeTOOx2aKvSCj7Pi3iuTGHFpndmcDsfyeu5jO-k9Tf95eBd'
    },
    'hiragara': {
        'tele_id': get_env_int('TELE_H_CHANNEL_ID'),
        'name': 'Hiragara Leaks',
        'icon_url': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTT9Cag-1GSvCyUuP10mVXkP2R7MZpU6BSZa0Uw9iaBFxtXLjZQ'
    },
    'test': {
        'tele_id': get_env_int('TELE_T_CHANNEL_ID'),
        'name': 'Test',
        'icon_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFfUnCIPVTtIm4RpwIrOehAhXxNXeuKY2TZQ&s'
    }
}