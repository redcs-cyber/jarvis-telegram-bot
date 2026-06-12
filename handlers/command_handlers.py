"""Telegram command and message handlers."""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction
from config import BOT_NAME, BOT_VERSION, MODE_ONLINE, MODE_OFFLINE
from models.session import SessionManager
from utils.ai_agent import get_ai_response, web_search, run_python_code
from utils.offline_engine import get_offline_response
from utils.tools import generate_qr_code, calculate, run_code

session_manager = SessionManager()


# ============== INLINE KEYBOARDS ==============

def get_main_menu_keyboard():
    """Main menu inline keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🔍 Web Arama", callback_data="menu_search"),
            InlineKeyboardButton("💻 Kod Çalıştır", callback_data="menu_code"),
        ],
        [
            InlineKeyboardButton("🌐 Çeviri", callback_data="menu_translate"),
            InlineKeyboardButton("🧮 Hesaplama", callback_data="menu_calc"),
        ],
        [
            InlineKeyboardButton("🤖 Jarvis Modu", callback_data="menu_jarvis"),
            InlineKeyboardButton("⚙️ Ayarlar", callback_data="menu_settings"),
        ],
        [
            InlineKeyboardButton("📊 İstatistikler", callback_data="menu_stats"),
            InlineKeyboardButton("❓ Yardım", callback_data="menu_help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings_keyboard(session):
    """Settings inline keyboard."""
    mode_emoji = "🟢" if session.mode == MODE_ONLINE else "🔴"
    jarvis_emoji = "✅" if session.jarvis_mode else "❌"
    keyboard = [
        [
            InlineKeyboardButton(f"{mode_emoji} Mod: {session.mode.upper()}", callback_data="toggle_mode"),
        ],
        [
            InlineKeyboardButton(f"{jarvis_emoji} Jarvis Modu", callback_data="toggle_jarvis"),
        ],
        [
            InlineKeyboardButton("🗑️ Geçmişi Temizle", callback_data="clear_history"),
        ],
        [
            InlineKeyboardButton("◀️ Ana Menü", callback_data="main_menu"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


# ============== COMMAND HANDLERS ==============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)

    welcome_text = (
        f"🤖 *{BOT_NAME} v{BOT_VERSION}*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Merhaba *{user.first_name}*! 👋\n\n"
        f"Ben Jarvis, kişisel AI asistanınızım.\n"
        f"Size şu konularda yardımcı olabilirim:\n\n"
        f"🔍 *Web Araması* - İnternette arama\n"
        f"💻 *Kod Çalıştırma* - Python kodu çalıştır\n"
        f"🌐 *Çeviri* - Metinleri çevir\n"
        f"📄 *Dosya Analizi* - Dosyaları analiz et\n"
        f"🧮 *Hesaplama* - Matematik işlemleri\n"
        f"📰 *Haberler* - Son haberler\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 Mod: *{session.mode.upper()}*\n"
        f"🤖 Jarvis: *{'Aktif' if session.jarvis_mode else 'Pasif'}*\n"
    )

    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_main_menu_keyboard()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "📋 *KOMUT LİSTESİ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🚀 *Temel Komutlar:*\n"
        "/start - Botu başlat\n"
        "/help - Bu yardım mesajı\n"
        "/clear - Geçmişi temizle\n\n"
        "🤖 *AI Komutları:*\n"
        "/jarvis - Jarvis modunu aç/kapat\n"
        "/mode [online/offline] - Mod değiştir\n"
        "/search [sorgu] - Web araması\n"
        "/code [kod] - Kod çalıştır\n"
        "/translate [dil] [metin] - Çeviri\n\n"
        "🛠️ *Araçlar:*\n"
        "/calc [ifade] - Hesap makinesi\n"
        "/qr [metin] - QR kod oluştur\n"
        "/weather [şehir] - Hava durumu\n"
        "/news - Son haberler\n\n"
        "📊 *Diğer:*\n"
        "/stats - Kullanım istatistikleri\n"
        "/settings - Ayarlar menüsü\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 _Herhangi bir mesaj yazarak da benimle sohbet edebilirsiniz!_"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def jarvis_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /jarvis command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    is_active = session.toggle_jarvis_mode()

    if is_active:
        text = (
            "🎩 *JARVIS MODU AKTİF*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Efendim, Jarvis modu aktif edildi.\n"
            "Artık size daha profesyonel ve kibar bir üslupla hizmet edeceğim.\n\n"
            "_Tüm sistemler çevrimiçi, emrinize amadeyim._"
        )
    else:
        text = (
            "🤖 *JARVIS MODU KAPALI*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Jarvis modu kapatıldı.\n"
            "Normal asistan moduna geçildi."
        )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command."""
    user = update.effective_user
    session_manager.clear_session(user.id)
    await update.message.reply_text(
        "🗑️ *Geçmiş Temizlendi*\n\nKonuşma geçmişi başarıyla silindi.",
        parse_mode=ParseMode.MARKDOWN
    )


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)

    if not context.args:
        await update.message.reply_text(
            "🔍 *Web Arama*\n\nKullanım: `/search [sorgu]`\nÖrnek: `/search Python öğrenme kaynakları`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    query = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    results = web_search(query)
    session.search_count += 1

    response = f"🔍 *Arama Sonuçları:* `{query}`\n━━━━━━━━━━━━━━━━━━━━\n\n{results}"
    await update.message.reply_text(response[:4096], parse_mode=ParseMode.MARKDOWN)


async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /code command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)

    if not context.args:
        await update.message.reply_text(
            "💻 *Kod Çalıştır*\n\nKullanım: `/code [python kodu]`\nÖrnek: `/code print('Merhaba!')`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    code = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    output = run_code(code)
    session.code_count += 1

    response = f"💻 *Kod Çıktısı:*\n━━━━━━━━━━━━━━━━━━━━\n\n```\n{output}\n```"
    await update.message.reply_text(response[:4096], parse_mode=ParseMode.MARKDOWN)


async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /translate command."""
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "🌐 *Çeviri*\n\nKullanım: `/translate [dil] [metin]`\nÖrnek: `/translate en Merhaba dünya`\n\nDiller: en, tr, de, fr, es, it, ja, ko, zh, ar, ru",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    target_lang = context.args[0]
    text = " ".join(context.args[1:])
    await update.message.chat.send_action(ChatAction.TYPING)

    from utils.ai_agent import translate_text
    result = translate_text(text, target_lang)

    response = f"🌐 *Çeviri Sonucu:*\n━━━━━━━━━━━━━━━━━━━━\n\n📝 Orijinal: _{text}_\n🎯 Hedef ({target_lang}): *{result}*"
    await update.message.reply_text(response[:4096], parse_mode=ParseMode.MARKDOWN)


async def mode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mode command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)

    if not context.args:
        current = "🟢 Online" if session.mode == MODE_ONLINE else "🔴 Offline"
        await update.message.reply_text(
            f"⚙️ *Mod Ayarı*\n\nMevcut mod: {current}\n\nKullanım: `/mode online` veya `/mode offline`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    new_mode = context.args[0].lower()
    if session.set_mode(new_mode):
        emoji = "🟢" if new_mode == "online" else "🔴"
        await update.message.reply_text(
            f"{emoji} *Mod Değiştirildi*\n\nYeni mod: *{new_mode.upper()}*",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("⚠️ Geçersiz mod. `online` veya `offline` kullanın.", parse_mode=ParseMode.MARKDOWN)


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)

    text = (
        "⚙️ *AYARLAR*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Aşağıdaki butonları kullanarak ayarları değiştirin:"
    )
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=get_settings_keyboard(session)
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command."""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    stats = session.get_stats()

    mode_emoji = "🟢" if stats["mode"] == "online" else "🔴"
    jarvis_emoji = "✅" if stats["jarvis_mode"] else "❌"

    text = (
        "📊 *KULLANIM İSTATİSTİKLERİ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 Kullanıcı ID: `{stats['user_id']}`\n"
        f"💬 Toplam Mesaj: *{stats['message_count']}*\n"
        f"🔍 Arama Sayısı: *{stats['search_count']}*\n"
        f"💻 Kod Çalıştırma: *{stats['code_count']}*\n"
        f"📝 Geçmiş Uzunluğu: *{stats['history_length']}*\n\n"
        f"{mode_emoji} Mod: *{stats['mode'].upper()}*\n"
        f"{jarvis_emoji} Jarvis Modu: *{'Aktif' if stats['jarvis_mode'] else 'Pasif'}*\n"
        f"📅 Oturum Başlangıcı: _{stats['created_at']}_"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /calc command."""
    if not context.args:
        await update.message.reply_text(
            "🧮 *Hesap Makinesi*\n\nKullanım: `/calc [ifade]`\nÖrnek: `/calc 25 * 4 + 10`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    expression = " ".join(context.args)
    result = calculate(expression)
    await update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /qr command."""
    if not context.args:
        await update.message.reply_text(
            "📱 *QR Kod Oluşturucu*\n\nKullanım: `/qr [metin veya URL]`\nÖrnek: `/qr https://google.com`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    text = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.UPLOAD_PHOTO)

    try:
        qr_buffer = generate_qr_code(text)
        await update.message.reply_photo(
            photo=qr_buffer,
            caption=f"📱 *QR Kod*\n\nİçerik: `{text}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ QR kod oluşturma hatası: {str(e)}")


async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /weather command."""
    if not context.args:
        await update.message.reply_text(
            "🌤️ *Hava Durumu*\n\nKullanım: `/weather [şehir]`\nÖrnek: `/weather İstanbul`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    city = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    # Use wttr.in for free weather
    import requests
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3&lang=tr", timeout=5)
        weather_info = response.text.strip()

        detailed = requests.get(f"https://wttr.in/{city}?format=%C+%t+%h+%w&lang=tr", timeout=5)
        detail_text = detailed.text.strip()

        text = (
            f"🌤️ *Hava Durumu - {city}*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📍 {weather_info}\n"
            f"📋 Detay: {detail_text}"
        )
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Hava durumu alınamadı: {str(e)}")


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /news command."""
    await update.message.chat.send_action(ChatAction.TYPING)

    results = web_search("son dakika haberler Türkiye bugün")
    response = f"📰 *SON HABERLER*\n━━━━━━━━━━━━━━━━━━━━\n\n{results}"
    await update.message.reply_text(response[:4096], parse_mode=ParseMode.MARKDOWN)


# ============== CALLBACK QUERY HANDLER ==============

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button presses."""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    session = session_manager.get_session(user.id)

    if query.data == "main_menu":
        text = (
            f"🤖 *{BOT_NAME}*\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Ana menüye hoş geldiniz! Aşağıdan bir işlem seçin:"
        )
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())

    elif query.data == "menu_search":
        await query.edit_message_text(
            "🔍 *Web Arama*\n\nAramak istediğiniz şeyi `/search [sorgu]` komutuyla yazın.\nÖrnek: `/search yapay zeka nedir`",
            parse_mode=ParseMode.MARKDOWN
        )

    elif query.data == "menu_code":
        await query.edit_message_text(
            "💻 *Kod Çalıştır*\n\nÇalıştırmak istediğiniz Python kodunu `/code [kod]` komutuyla yazın.\nÖrnek: `/code print(2+2)`",
            parse_mode=ParseMode.MARKDOWN
        )

    elif query.data == "menu_translate":
        await query.edit_message_text(
            "🌐 *Çeviri*\n\nKullanım: `/translate [dil] [metin]`\nÖrnek: `/translate en Merhaba dünya`",
            parse_mode=ParseMode.MARKDOWN
        )

    elif query.data == "menu_calc":
        await query.edit_message_text(
            "🧮 *Hesap Makinesi*\n\nKullanım: `/calc [ifade]`\nÖrnek: `/calc 100 * 5 / 2`",
            parse_mode=ParseMode.MARKDOWN
        )

    elif query.data == "menu_jarvis":
        is_active = session.toggle_jarvis_mode()
        emoji = "✅" if is_active else "❌"
        text = f"🤖 Jarvis Modu: {emoji} *{'Aktif' if is_active else 'Pasif'}*"
        if is_active:
            text += "\n\n_Efendim, emrinize amadeyim._"
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())

    elif query.data == "menu_settings":
        text = "⚙️ *AYARLAR*\n━━━━━━━━━━━━━━━━━━━━\n\nAyarları değiştirmek için butonları kullanın:"
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_settings_keyboard(session))

    elif query.data == "menu_stats":
        stats = session.get_stats()
        mode_emoji = "🟢" if stats["mode"] == "online" else "🔴"
        text = (
            f"📊 *İSTATİSTİKLER*\n━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💬 Mesaj: *{stats['message_count']}*\n"
            f"🔍 Arama: *{stats['search_count']}*\n"
            f"💻 Kod: *{stats['code_count']}*\n"
            f"{mode_emoji} Mod: *{stats['mode'].upper()}*"
        )
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())

    elif query.data == "menu_help":
        await query.edit_message_text(
            "❓ *YARDIM*\n\nDetaylı yardım için /help komutunu kullanın.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_main_menu_keyboard()
        )

    elif query.data == "toggle_mode":
        new_mode = MODE_OFFLINE if session.mode == MODE_ONLINE else MODE_ONLINE
        session.set_mode(new_mode)
        await query.edit_message_text(
            "⚙️ *AYARLAR*\n━━━━━━━━━━━━━━━━━━━━\n\nAyarları değiştirmek için butonları kullanın:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_settings_keyboard(session)
        )

    elif query.data == "toggle_jarvis":
        session.toggle_jarvis_mode()
        await query.edit_message_text(
            "⚙️ *AYARLAR*\n━━━━━━━━━━━━━━━━━━━━\n\nAyarları değiştirmek için butonları kullanın:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_settings_keyboard(session)
        )

    elif query.data == "clear_history":
        session.clear_history()
        await query.edit_message_text(
            "🗑️ *Geçmiş temizlendi!*\n\nKonuşma geçmişi başarıyla silindi.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_settings_keyboard(session)
        )


# ============== MESSAGE HANDLER ==============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    text = update.message.text

    session.add_message("user", text)
    await update.message.chat.send_action(ChatAction.TYPING)

    if session.mode == MODE_ONLINE:
        response = get_ai_response(session.messages, session.jarvis_mode)
    else:
        response = get_offline_response(text, session.jarvis_mode)

    session.add_message("assistant", response)

    # Split long messages
    if len(response) > 4096:
        for i in range(0, len(response), 4096):
            await update.message.reply_text(response[i:i+4096], parse_mode=ParseMode.MARKDOWN)
    else:
        try:
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text(response)


# ============== DARWIN-ES KOMUTLARI ==============

async def darwin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /darwin command - DARWIN-ES istatistikleri."""
    from utils.darwin_bridge import darwin
    stats = darwin.get_stats()

    top_str = "\n".join([
        f"  {s['id']}. {s['name']} ({s['usage_pct']}, başarı: {s['success_rate']})"
        for s in stats['top_strategies']
    ])

    parents_str = "\n".join([
        f"  P{p['id']}: fitness={p['fitness']}, aktif={p['active_strategies']}"
        for p in stats['parents_summary']
    ])

    text = (
        "🧬 *DARWIN-ES İSTATİSTİKLERİ*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔄 Nesil: *{stats['generation']}*\n"
        f"📊 Toplam Değerlendirme: *{stats['total_evaluations']}*\n"
        f"👥 µ={stats['mu']}, λ={stats['lambda']}\n\n"
        f"🏆 *En Çok Kullanılan Stratejiler:*\n{top_str}\n\n"
        f"🧬 *Parent Durumları:*\n{parents_str}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def strategies_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /strategies command - Aktif stratejiler."""
    from utils.darwin_bridge import darwin
    strategies = darwin.get_active_strategies()

    if not strategies:
        await update.message.reply_text("⚠️ Henüz aktif strateji yok.")
        return

    lines = []
    for s in strategies:
        emoji = "✅" if s['usage'] > 0 else "⬜"
        lines.append(f"{emoji} `{s['id']:2d}` *{s['name']}* — kullanım: {s['usage']}, başarı: {s['success_rate']}")

    text = (
        "🎯 *AKTİF STRATEJİLER*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        + "\n".join(lines)
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def dataset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /dataset command - Anthropic dataset durumu."""
    text = (
        "📦 *ANTHROPIC DATASET DURUMU*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "*Mevcut Datasetler:*\n"
        "1️⃣ `Anthropic/hh-rlhf` — 169K konuşma (RLHF)\n"
        "2️⃣ `Anthropic/values-in-the-wild` — 3307 değer\n"
        "3️⃣ `Anthropic/model-written-evals` — 3.25K eval\n"
        "4️⃣ `Anthropic/persuasion` — 3.94K kayıt\n\n"
        "*Entegrasyon:*\n"
        "• RLHF Trainer: DARWIN-ES fitness optimizasyonu\n"
        "• Values Engine: Yanıt kalite değerlendirmesi\n"
        "• Offline önbellek: SQLite tabanlı\n\n"
        "_İndirmek için Termux'ta:_\n"
        "`python -c \"from datasets.anthropic_loader import AnthropicDatasetLoader; import asyncio; asyncio.run(AnthropicDatasetLoader().download_dataset('hh-rlhf'))\"`"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ============== DOCUMENT HANDLER ==============

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document/file uploads."""
    user = update.effective_user
    session = session_manager.get_session(user.id)
    document = update.message.document

    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        file = await document.get_file()
        file_bytes = await file.download_as_bytearray()
        content = file_bytes.decode("utf-8", errors="ignore")

        # Limit content
        if len(content) > 3000:
            content = content[:3000] + "\n...[kırpıldı]"

        prompt = f"Kullanıcı şu dosyayı gönderdi ({document.file_name}):\n\n{content}\n\nBu dosyayı analiz et ve özetle."
        session.add_message("user", prompt)

        if session.mode == MODE_ONLINE:
            response = get_ai_response(session.messages, session.jarvis_mode)
        else:
            response = f"📄 *Dosya Alındı:* `{document.file_name}`\n\n⚠️ Offline modda dosya analizi yapılamıyor. Online moda geçmek için /mode online yazın."

        session.add_message("assistant", response)
        await update.message.reply_text(response[:4096], parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Dosya okuma hatası: {str(e)}")
