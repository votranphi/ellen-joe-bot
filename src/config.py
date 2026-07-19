import os
from dotenv import load_dotenv

load_dotenv()

def get_env_int(key):
    val = os.getenv(key)
    return int(val) if val and val.lstrip('-').isdigit() else None

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

ELLEN_AVATAR_URL = "https://pbs.twimg.com/media/GTX9pylaIAAvr-R.png"

STATUS_PROFILES = { # only in Bean's server
    "bel": {
        "display_name": "Bel Vương",
        "role_id": 1528100067280551956,
        "title_prefix": ":pregnant_man: Bel Check",
        "value_label": "bel",
        "footer": "💫 Đạt 100% để nhận role Bel Vương",
        "zero_icon": "💀",
        "zero_message": "Gió thổi là bay, bộ xương di động.",
        "low_icon": "😌",
        "low_message": "Mới nhú tí nọng, nhìn chung vẫn ốm nhom.",
        "mid_icon": "🤔",
        "mid_message": "Nửa nạc nửa mỡ, bụng bắt đầu rung rinh rồi.",
        "high_icon": "🔥",
        "high_message": "Tròn ủm, ngấn nào ra ngấn nấy.",
        "near_max_icon": "👀",
        "near_max_message": "Mỡ tràn bờ đê, chuẩn bị lăn thay vì đi.",
        "max_icon": "👑",
        "max_message": "Hệ tư tưởng xôi thịt. 100% Bel Vương!",
    },
    "goon": {
        "display_name": "Lọ Vương",
        "role_id": 1528271445392625824,
        "title_prefix": ":bottle_with_popping_cork: Goon Check",
        "value_label": "lọ",
        "footer": "💫 Đạt 100% để nhận role Lọ Vương",
        "zero_icon": "🫗",
        "zero_message": "Khô như sa mạc, chai lọ còn phải xin nghỉ phép.",
        "low_icon": "😏",
        "low_message": "Lung lay chút đỉnh, nhưng vẫn còn ngây thơ.",
        "mid_icon": "🫣",
        "mid_message": "Bắt đầu nghiện mùi men, mắt đã hơi lạc đường.",
        "high_icon": "🔥",
        "high_message": "Đã vào guồng, chuẩn bị thành huyền thoại lọ.",
        "near_max_icon": "👀",
        "near_max_message": "Lọ tràn bờ đê, nhìn là biết không còn đường lui.",
        "max_icon": "👑",
        "max_message": "Đỉnh cao lọ học. 100% Lọ Vương!",
    },
    "dam": {
        "display_name": "Dam Dang",
        "role_id": 1528271546999636009,
        "title_prefix": ":fire: Dâm Check",
        "value_label": "dâm",
        "footer": "💫 Đạt 100% để nhận role Dam Dang",
        "zero_icon": "🧊",
        "zero_message": "Tâm hồn trong như nước suối, gió xuân còn chê nhạt.",
        "low_icon": "😎",
        "low_message": "Mới chớm lửa, nhìn vẫn còn hiền.",
        "mid_icon": "😈",
        "mid_message": "Nhiệt bắt đầu lên, khó mà ngồi yên.",
        "high_icon": "🔥",
        "high_message": "Lửa cháy rõ rồi, ai đứng gần cũng thấy nóng.",
        "near_max_icon": "👀",
        "near_max_message": "Hừng hực như than hồng, chuẩn bị bùng nổ.",
        "max_icon": "👑",
        "max_message": "Bản năng bốc cháy. 100% Dam Dang!",
    },
}