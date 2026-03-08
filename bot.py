import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # تنزيل الفيديو
    video_file = await update.message.video.get_file()
    file_path = f"{user_id}_video.mp4"
    await video_file.download_to_drive(file_path)

    # تحويل الفيديو إلى بصمة صوتية (Voice Message)
    voice_path = f"{user_id}_voice.ogg"
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", file_path, "-vn", "-ar", "48000", "-ac", "1", "-c:a", "libopus", voice_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # إرسال الرسالة الصوتية
        await update.message.reply_voice(
            voice=open(voice_path, "rb"),
            caption="تم تحويل الفيديو الى بصمة صوتية 🎙️\nصانع البوت ----» @wi6j1"
        )

    except Exception as e:
        await update.message.reply_text(
            f"حدث خطأ أثناء التحويل: {e}\nصانع البوت ----» @wi6j1"
        )

    finally:
        # حذف الملفات المؤقتة
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(voice_path):
            os.remove(voice_path)

# إعداد التطبيق
app = ApplicationBuilder().token(TOKEN).build()

# إضافة handler للفيديو
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

# تشغيل البوت
app.run_polling()
