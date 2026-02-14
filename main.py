import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Koyeb ---
app = Flask('')
@app.route('/')
def home(): return "Downloader Bot is Running!"
def run(): app.run(host='0.0.0.0', port=8000)
def keep_alive(): Thread(target=run).start()

# --- إعداد البوت ---
TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أرسل لي رابط الفيديو (يوتيوب، تيك توك، إنستا) وسأقوم بتحميله لك فوراً بأعلى جودة! 🚀")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith('http'):
        return

    msg = bot.reply_to(message, "⏳ جارِ معالجة الرابط والتحميل... انتظر قليلاً")
    
    # إعدادات yt-dlp للتحميل بأفضل جودة
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video.mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # إرسال الفيديو للمستخدم
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم التحميل بواسطة بوتك الأقوى 🔥")
        
        bot.delete_message(message.chat.id, msg.message_id)
        os.remove('video.mp4') # حذف الفيديو من السيرفر بعد الإرسال لتوفير المساحة
    except Exception as e:
        bot.edit_message_text(f"❌ حدث خطأ: تأكد من الرابط أو حاول لاحقاً.", message.chat.id, msg.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
