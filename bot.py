import os
from telebot import TeleBot
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = TeleBot(TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    chat_id = message.chat.id
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    video_path = "temp_video.mp4"
    
    with open(video_path, 'wb') as f:
        f.write(downloaded_file)
    
    bot.send_message(chat_id, "جاري تحويل الفيديو إلى صوت...")
    
    # استخراج الصوت من الفيديو
    clip = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    clip.audio.write_audiofile(audio_path)
    
    # تحويل إلى رسالة صوتية بصيغة .ogg (مطابقة لتليجرام)
    voice = AudioSegment.from_wav(audio_path)
    voice.export("voice.ogg", format="ogg")
    
    # إرسال الصوت كبصمة/رسالة صوتية
    with open("voice.ogg", "rb") as v:
        bot.send_voice(chat_id, v, caption="ها هي الرسالة الصوتية!")
    
    # تنظيف الملفات المؤقتة
    os.remove(video_path)
    os.remove(audio_path)
    os.remove("voice.ogg")

bot.infinity_polling()
