from pyrogram import Client
from pytgcalls import PyTgCalls

music_queue = {}

app = Client(
    "AnnonMusicBot",
    api_id=123456,              # ⚠️ Apni API ID
    api_hash="YOUR_API_HASH",   # ⚠️ Apna API HASH
    bot_token="YOUR_BOT_TOKEN", # ⚠️ Apna Bot Token
    plugins=dict(root="plugins")
)

assistant = Client(
    "AnnonAssistant",
    api_id=123456,                # ⚠️ Apni API ID
    api_hash="YOUR_API_HASH",     # ⚠️ Apna API HASH
    session_string="YOUR_SESSION" # ⚠️ Sabse latest wala Session String
)

call = PyTgCalls(assistant)
