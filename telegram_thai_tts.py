import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from pythaitts import TTS
import threading
from dotenv import load_dotenv
load_dotenv()


# === SETUP YOUR TELEGRAM BOT TOKEN ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === INIT THAI TTS ENGINE ===
tts = TTS(
    pretrained="khanomtan",
    version="1.0",
    mode="best_model",
    device="cpu"
)

def listen_for_exit():
    while True:
        user_input = input("Press [q] to quit: ").strip().lower()
        if user_input == "q":
            print("[🚪] Exiting bot...")
            os._exit(0)  # Immediate kill

# Start exit listener in background thread
threading.Thread(target=listen_for_exit, daemon=True).start()

# === FUNCTION TO CONVERT TEXT TO SPEECH & PLAY ===
def speak(text):
    print(f"[🔈 TTS] Speaking: {text}")
    tts.tts(
        text=text,
        speaker_idx="Tsyncone",     # Thai female voice
        # speaker_idx="Tsynctwo",     # Thai male voice
        language_idx="th-th",
        return_type="file",
        filename="thai_output.wav"
    )
    # os.system("ffplay -nodisp -autoexit  thai_output.wav")
# Slow it down by 0.8x
    os.system("ffmpeg -y -i thai_output.wav -filter:a atempo=0.75 slow_output.wav && ffplay -nodisp -autoexit slow_output.wav")

# === HANDLE INCOMING MESSAGES ===
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user.full_name
    print(f"[📩 Telegram] From {user}: {text}")
    speak(text)

# === BOT MAIN LOOP ===
async def main():
    print("[🤖] Telegram Thai TTS Bot is starting...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))
    await app.run_polling()

# === RUN BOT ===
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())

