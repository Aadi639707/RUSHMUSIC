from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# 🖼️ Start Image URL
START_IMG_URL = "https://telegra.ph/file/0c9a2f643e2f5b8f2f451.jpg"

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    bot_name = client.me.first_name
    bot_username = client.me.username
    
        caption_text = (
        f"ʜᴇʏ {message.from_user.mention} , 🥀\n\n"
        f"⊙ ᴛʜɪs ɪs ˹ {bot_name} ˼ !\n\n"
        f"➻ ᴀ ғᴀsᴛ & ᴘᴏᴡᴇʀғᴜʟ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs.\n\n"
        f"⊙ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs."
        )

    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⁺", url=f"https://t.me/{bot_username}?startgroup=true")],
        [InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_menu")],
        [
            InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ↗", url="https://t.me/rushdeveloper"), 
            InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ ↗", url="https://t.me/rushbots")       
        ]
    ])
    
    try:
        await message.reply_photo(photo=START_IMG_URL, caption=caption_text, reply_markup=buttons)
    except Exception:
        await message.reply_text(text=caption_text, reply_markup=buttons)
  
