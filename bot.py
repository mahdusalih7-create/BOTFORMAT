import os
import subprocess
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    
    if message.video.file_size > 50 * 1024 * 1024:
        bot.send_message(chat_id, "الفيديو كبير جدًا، حاول فيديو أصغر من 50MB")
        return

    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    video_path = "temp_video.mp4"
    voice_path = "voice.ogg"

    with open(video_path, 'wb') as f:
        f.write(downloaded_file)
    
    bot.send_message(chat_id, "جاري تحويل الفيديو إلى رسالة صوتية...")

    # تحويل الفيديو إلى OGG مباشرة باستخدام ffmpeg
    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-vn",            # بدون الفيديو
        "-c:a", "libopus", # صيغة teleram الصوتية
        "-b:a", "64k",
        voice_path,
        "-y"              # استبدال إذا موجود
    ])

    with open(voice_path, "rb") as v:
        bot.send_voice(chat_id, v, caption="ها هي الرسالة الصوتية!")

    os.remove(video_path)
    os.remove(voice_path)

bot.infinity_polling()
