from pyrogram import Client
from pytgcalls import PyTgCalls

# 🧠 Master Single-Queue Dictionary
music_queue = {}

# 🤖 Main Bot Client (Commands ke liye)
app = Client(
    "AnnonMusicBot",
    api_id=123456,              # ⚠️ Apni API ID dalo
    api_hash="YOUR_API_HASH",   # ⚠️ Apna API HASH dalo
    bot_token="YOUR_BOT_TOKEN", # ⚠️ Apna Bot Token dalo
    plugins=dict(root="plugins")
)

# 👤 Assistant Client (Voice Chat join karne ke liye)
assistant = Client(
    "AnnonAssistant",
    api_id=123456,                # ⚠️ Apni API ID dalo
    api_hash="YOUR_API_HASH",     # ⚠️ Apna API HASH dalo
    session_string="YOUR_SESSION" # ⚠️ 271-byte wala naya Session String
)

# 📞 PyTgCalls Client Engine
call = PyTgCalls(assistant)
