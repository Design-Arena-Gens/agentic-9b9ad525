import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("المساعدة 📚", callback_data='help'),
            InlineKeyboardButton("معلومات ℹ️", callback_data='info')
        ],
        [
            InlineKeyboardButton("الإعدادات ⚙️", callback_data='settings')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'مرحباً! 👋\n\n'
        'أنا بوت تيليغرام متعدد الوظائف.\n\n'
        'استخدم الأزرار أدناه للتنقل:',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = """
🤖 الأوامر المتاحة:

/start - بدء البوت
/help - عرض هذه الرسالة
/info - معلومات عن البوت
/echo - إعادة إرسال رسالتك
/stats - إحصائيات الاستخدام
/weather - الطقس (مثال: /weather Cairo)

📝 يمكنك أيضاً إرسال رسائل نصية وسأرد عليك!
    """
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display bot information."""
    info_text = """
ℹ️ معلومات البوت:

🔹 الاسم: بوت تيليغرام Python
🔹 الإصدار: 1.0.0
🔹 اللغة: Python 3.11
🔹 المكتبة: python-telegram-bot

✨ الميزات:
- واجهة تفاعلية
- أزرار مخصصة
- دعم اللغة العربية
- معالجة الرسائل
- إحصائيات الاستخدام
    """
    await update.message.reply_text(info_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    if context.args:
        message = ' '.join(context.args)
        await update.message.reply_text(f'📢 {message}')
    else:
        await update.message.reply_text('استخدم: /echo <رسالتك>')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display usage statistics."""
    user = update.effective_user
    stats_text = f"""
📊 إحصائيات الاستخدام:

👤 المستخدم: {user.first_name}
🆔 المعرف: {user.id}
💬 الرسائل: {context.user_data.get('message_count', 0)}

✅ البوت يعمل بشكل طبيعي
    """
    await update.message.reply_text(stats_text)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display weather information (mock)."""
    if context.args:
        city = ' '.join(context.args)
        weather_text = f"""
🌤️ الطقس في {city}:

🌡️ درجة الحرارة: 25°C
💧 الرطوبة: 60%
🌬️ الرياح: 15 كم/س
☁️ الحالة: غائم جزئياً

(هذا مثال تجريبي)
        """
        await update.message.reply_text(weather_text)
    else:
        await update.message.reply_text('استخدم: /weather <المدينة>')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
🤖 الأوامر المتاحة:

/start - بدء البوت
/help - المساعدة
/info - معلومات
/echo - إعادة الإرسال
/stats - الإحصائيات
/weather - الطقس
        """
        await query.edit_message_text(help_text)

    elif query.data == 'info':
        info_text = """
ℹ️ معلومات البوت:

🔹 بوت تيليغرام متعدد الوظائف
🔹 مبني بلغة Python
🔹 يدعم اللغة العربية
🔹 واجهة تفاعلية سهلة
        """
        await query.edit_message_text(info_text)

    elif query.data == 'settings':
        settings_text = """
⚙️ الإعدادات:

✅ اللغة: العربية
✅ الإشعارات: مفعلة
✅ الوضع: عادي

لتغيير الإعدادات، اتصل بالمطور.
        """
        await query.edit_message_text(settings_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    # Count messages
    if 'message_count' not in context.user_data:
        context.user_data['message_count'] = 0
    context.user_data['message_count'] += 1

    message_text = update.message.text.lower()

    # Simple responses
    if 'مرحبا' in message_text or 'السلام' in message_text:
        await update.message.reply_text('مرحباً بك! 👋 كيف يمكنني مساعدتك؟')
    elif 'شكرا' in message_text:
        await update.message.reply_text('العفو! 😊 سعيد بمساعدتك')
    elif 'كيف حالك' in message_text:
        await update.message.reply_text('أنا بخير، شكراً! 🤖 كيف يمكنني مساعدتك؟')
    else:
        await update.message.reply_text(
            f'تلقيت رسالتك: "{update.message.text}"\n\n'
            'استخدم /help لرؤية الأوامر المتاحة.'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f'Update {update} caused error {context.error}')

def main():
    """Start the bot."""
    # Get token from environment variable
    token = os.environ.get('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ خطأ: لم يتم العثور على TELEGRAM_BOT_TOKEN في المتغيرات البيئية")
        print("📝 للتشغيل، قم بتعيين التوكن:")
        print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
        return

    # Create application
    application = Application.builder().token(token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Start bot
    print("🚀 البوت يعمل الآن...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
