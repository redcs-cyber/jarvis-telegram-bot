"""
Jarvis AI Assistant - Telegram Bot
===================================
Professional AI assistant with online/offline modes,
Jarvis personality, web search, code execution, and more.
"""
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN, BOT_NAME, BOT_VERSION
from handlers.command_handlers import (
    start_command,
    help_command,
    jarvis_command,
    clear_command,
    search_command,
    code_command,
    translate_command,
    mode_command,
    settings_command,
    stats_command,
    calc_command,
    qr_command,
    weather_command,
    news_command,
    darwin_command,
    strategies_command,
    dataset_command,
    button_callback,
    handle_message,
    handle_document,
)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    print(f"""
╔══════════════════════════════════════════╗
║                                          ║
║     🤖 {BOT_NAME}             ║
║        Version {BOT_VERSION}                  ║
║                                          ║
║     Status: ONLINE                       ║
║     Mode: Ready                          ║
║                                          ║
╚══════════════════════════════════════════╝
    """)

    # Build application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("jarvis", jarvis_command))
    app.add_handler(CommandHandler("clear", clear_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("code", code_command))
    app.add_handler(CommandHandler("translate", translate_command))
    app.add_handler(CommandHandler("mode", mode_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("calc", calc_command))
    app.add_handler(CommandHandler("qr", qr_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("darwin", darwin_command))
    app.add_handler(CommandHandler("strategies", strategies_command))
    app.add_handler(CommandHandler("dataset", dataset_command))

    # Callback query handler (inline buttons)
    app.add_handler(CallbackQueryHandler(button_callback))

    # Message handlers
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    logger.info(f"{BOT_NAME} v{BOT_VERSION} başlatılıyor...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
