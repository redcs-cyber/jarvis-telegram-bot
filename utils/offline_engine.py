"""Offline Engine - Rule-based response system for offline mode."""
import re
import random
from datetime import datetime

# Knowledge base for offline mode
KNOWLEDGE_BASE = {
    "selamlar": {
        "patterns": [r"merhaba", r"selam", r"hey", r"naber", r"nasılsın", r"günaydın", r"iyi akşamlar", r"iyi geceler"],
        "responses": [
            "Merhaba! Size nasıl yardımcı olabilirim?",
            "Selam! Bugün size ne konuda yardımcı olabilirim?",
            "Merhaba! Hazırım, buyurun.",
        ]
    },
    "jarvis_selamlar": {
        "patterns": [r"merhaba", r"selam", r"hey", r"naber", r"nasılsın"],
        "responses": [
            "Efendim, merhaba! Emrinize amadeyim.",
            "Efendim, size nasıl hizmet edebilirim?",
            "Efendim, buyurun. Tüm sistemler aktif.",
        ]
    },
    "hava_durumu": {
        "patterns": [r"hava", r"sıcaklık", r"yağmur", r"kar", r"güneş"],
        "responses": [
            "⚠️ Offline modda hava durumu bilgisi alınamıyor. Online moda geçmek için /mode online yazın.",
        ]
    },
    "saat": {
        "patterns": [r"saat kaç", r"saat", r"zaman", r"tarih"],
        "responses": ["dynamic_time"]
    },
    "matematik": {
        "patterns": [r"(\d+)\s*[\+\-\*\/]\s*(\d+)", r"hesapla", r"kaç eder"],
        "responses": ["dynamic_math"]
    },
    "kim_sin": {
        "patterns": [r"kimsin", r"adın ne", r"sen ne", r"kendini tanıt"],
        "responses": [
            "Ben Jarvis AI Assistant! Telegram üzerinde çalışan kişisel yapay zeka asistanınızım. Online ve offline modlarda çalışabilirim.",
            "Jarvis AI Assistant olarak hizmetinizdeyim. Araştırma, kod yazma, çeviri ve daha birçok konuda yardımcı olabilirim.",
        ]
    },
    "tesekkur": {
        "patterns": [r"teşekkür", r"sağol", r"eyvallah", r"thanks"],
        "responses": [
            "Rica ederim! Başka bir konuda yardımcı olabilir miyim?",
            "Ne demek, her zaman buradayım!",
            "Memnuniyetle! Başka sorunuz var mı?",
        ]
    },
    "yardim": {
        "patterns": [r"yardım", r"help", r"ne yapabilirsin", r"komutlar"],
        "responses": [
            "📋 *Kullanılabilir Komutlar:*\n\n/start - Başlat\n/help - Yardım\n/jarvis - Jarvis Modu\n/clear - Geçmişi Temizle\n/search - Web Araması\n/code - Kod Çalıştır\n/translate - Çeviri\n/mode - Mod Değiştir\n/settings - Ayarlar\n/stats - İstatistikler\n/weather - Hava Durumu\n/news - Haberler\n/qr - QR Kod Oluştur\n/calc - Hesap Makinesi",
        ]
    },
    "espri": {
        "patterns": [r"espri", r"fıkra", r"şaka", r"güldür", r"komik"],
        "responses": [
            "Programcı neden gözlük takar? Çünkü C# yapamaz! 😄",
            "İki yapay zeka konuşuyormuş. Biri demiş ki: 'Sence insanlar gerçek mi?' 🤖",
            "Bir bug bar'a girmiş. Barmen demiş: 'Burada sana servis yapamayız, sen production'dasın!' 🐛",
        ]
    },
    "varsayilan": {
        "patterns": [],
        "responses": [
            "⚠️ Offline moddayım, bu soruyu yanıtlamak için online moda geçmeniz gerekiyor. /mode online yazarak geçiş yapabilirsiniz.",
            "Offline modda sınırlı yanıt verebiliyorum. Daha detaylı yanıtlar için /mode online yazın.",
        ]
    }
}


def get_offline_response(text: str, jarvis_mode: bool = False) -> str:
    """Get response from offline rule-based engine."""
    text_lower = text.lower().strip()

    # Check time/date
    for pattern in KNOWLEDGE_BASE["saat"]["patterns"]:
        if re.search(pattern, text_lower):
            now = datetime.now()
            return f"🕐 Şu an: {now.strftime('%H:%M:%S')} | Tarih: {now.strftime('%d/%m/%Y')}"

    # Check math
    math_match = re.search(r"(\d+)\s*([\+\-\*\/])\s*(\d+)", text_lower)
    if math_match:
        try:
            result = eval(f"{math_match.group(1)}{math_match.group(2)}{math_match.group(3)}")
            return f"🧮 Sonuç: {math_match.group(1)} {math_match.group(2)} {math_match.group(3)} = {result}"
        except:
            pass

    # Check greetings
    greeting_key = "jarvis_selamlar" if jarvis_mode else "selamlar"
    for pattern in KNOWLEDGE_BASE[greeting_key]["patterns"]:
        if re.search(pattern, text_lower):
            return random.choice(KNOWLEDGE_BASE[greeting_key]["responses"])

    # Check other categories
    for category, data in KNOWLEDGE_BASE.items():
        if category in ["selamlar", "jarvis_selamlar", "saat", "matematik", "varsayilan"]:
            continue
        for pattern in data["patterns"]:
            if re.search(pattern, text_lower):
                return random.choice(data["responses"])

    # Default response
    if jarvis_mode:
        return f"Efendim, offline modda bu konuda size yardımcı olamıyorum. Online moda geçmek için /mode online komutunu kullanabilirsiniz."
    return random.choice(KNOWLEDGE_BASE["varsayilan"]["responses"])
