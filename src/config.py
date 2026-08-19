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

STATUS_PROFILES = {
    "bel": {
        "role": {
            "name": "Bel Vương",
            "color": "#1abc9c",
        },
        "footers": {
            "self": "💫 Đạt 100% để nhận role Bel Vương",
            "other": "✨ Check độ bel thành công!"
        },
        "title_prefix": ":pregnant_man: Bel Check",
        "value_label": "bel",
        "zero_message": ":skull: Gió thổi là bay, bộ xương di động.",
        "low_message": ":relieved: Mới nhú tí nọng, nhìn chung vẫn ốm nhom.",
        "mid_message": ":thinking: Nửa nạc nửa mỡ, bụng bắt đầu rung rinh rồi.",
        "high_message": ":fire: Tròn ủm, ngấn nào ra ngấn nấy.",
        "near_max_message": ":eyes: Mỡ tràn bờ đê, chuẩn bị lăn thay vì đi.",
        "max_message": ":crown: Hệ tư tưởng xôi thịt. 100% Bel Vương!",
    },
    "goon": {
        "role": {
            "name": "Goon Thủ",
            "color": "#e67e22",
        },
        "footers": {
            "self": "💫 Đạt 100% để nhận role Goon Thủ",
            "other": "✨ Check độ goon thành công!"
        },
        "title_prefix": ":jar: Goon Check",
        "value_label": "goon",
        "zero_message": ":cactus: Khô hạn, trình còn non lắm.",
        "low_message": ":smirk: Mới bắt đầu tập tành thôi.",
        "mid_message": ":full_moon_with_face: Đang cuốn dần rồi đó nha.",
        "high_message": ":fire: Tay nghề lên trình, cháy phố.",
        "near_max_message": ":eyes: Sắp 'out trình' tới nơi rồi.",
        "max_message": ":crown: Lọ vương hệ chiến. 100% Goon Thủ!",
    },
    "dam": {
        "role": {
            "name": "Dam Dang",
            "color": "#d4843d",
        },
        "footers": {
            "self": "💫 Đạt 100% để nhận role Dam Dang",
            "other": "✨ Check độ dâm thành công!"
        },
        "title_prefix": ":hot_face: Dâm Check",
        "value_label": "dâm",
        "zero_message": ":ice_cube: Nhạt như nước ốc, chưa có miếng vibe.",
        "low_message": ":sunglasses: Mới chớm, cần thêm tí lửa.",
        "mid_message": ":smiling_imp: Bắt đầu 'tới công chuyện' rồi.",
        "high_message": ":fire: Nhiệt quá, cháy quá cháy.",
        "near_max_message": ":eyes:Quá cháy, sắp bùng nổ rồi.",
        "max_message": ":crown:Đỉnh nóc kịch trần. 100% Dam Dang!",
    },
    "aura": {
        "role": {
            "name": "King Aura",
            "color": "#55fffa",
        },
        "footers": {
            "self": "💫 Đạt 100% để nhận role King Aura",
            "other": "✨ Check aura thành công!"
        },
        "title_prefix": ":shushing_face: Aura Check",
        "value_label": "aura",
        "zero_message": ":ghost: Âm aura, chuẩn L NPC mờ nhạt.",
        "low_message": ":leaves: Aura hơi phèn, chưa đủ trình flex.",
        "mid_message": ":nail_care: Cũng được đấy, bắt đầu có nét rồi.",
        "high_message": ":fire: Keo lỳ tái châu, hào quang chói lóa.",
        "near_max_message": ":star_struck: Đỉnh nóc, aura áp đảo cả server.",
        "max_message": ":crown: W Rizz, Sigma chúa. 100% King Aura!",
    },
    "ngu": {
        "role": {
            "name": "Ngu Nhất Server",
            "color": "#181616",
        },
        "footers": {
            "self": "💫 Đạt 100% để nhận role Ngu Nhất Server",
            "other": "✨ Check độ ngu thành công!"
        },
        "title_prefix": ":clown: Ngu Check",
        "value_label": "ngu",
        "zero_message": ":brain: IQ vô cực, 10 điểm không có nhưng!",
        "low_message": ":leaves: Não hơi lag nhẹ, vẫn còn cứu được.",
        "mid_message": ":penguin: Chớm xà lơ, hệ điều hành load hơi chậm.",
        "high_message": ":clown: Báo thủ real, thở ra là thấy cảm lạnh.",
        "near_max_message": ":skull: Tư duy đi vào lòng đất. Quên mang não hả?",
        "max_message": ":crown: Kẻ hủy diệt tri thức. 100% Ngu Nhất Server!",
    },
}