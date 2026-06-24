import os
import urllib.parse
import asyncio
import aiohttp
import json
import base64
import pyDes
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import MediaStream
from core import call, music_queue

os.makedirs("downloads", exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0",
    "Accept": "application/json, text/plain, */*"
}

DES_KEY = b"38346591"

def decrypt_url(encrypted_url):
    try:
        encrypted_url = encrypted_url.strip()
        missing_padding = len(encrypted_url) % 4
        if missing_padding: encrypted_url += '=' * (4 - missing_padding)
        crypto = pyDes.des(DES_KEY, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
        decrypted_bytes = crypto.decrypt(base64.b64decode(encrypted_url), padmode=pyDes.PAD_PKCS5)
        return decrypted_bytes.decode('utf-8')
    except:
        return None

@Client.on_message(filters.command("play") & filters.group)
async def play_command(client: Client, message: Message):
    if len(message.command) < 2: return await message.reply_text("ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ.")
    
    chat_id = message.chat.id
    query = message.text.split(None, 1)[1]
    processing_msg = await message.reply_text("sᴇᴀʀᴄʜɪɴɢ ᴅɪʀᴇᴄᴛʟʏ ᴏɴ ᴊɪᴏsᴀᴀᴠɴ...")

    try:
        encoded_query = urllib.parse.quote(query)
        song_id = None
        
        search_url = f"https://www.jiosaavn.com/api.php?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query={encoded_query}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=HEADERS, timeout=10) as resp:
                search_data = json.loads(await resp.text())
                song_id = search_data["songs"]["data"][0]["id"]
                
            details_url = f"https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids={song_id}"
            
            async with session.get(details_url, headers=HEADERS, timeout=10) as resp:
                details_data = json.loads(await resp.text())
                track = details_data[song_id]
                title = track.get("song", "Unknown").replace("&quot;", '"')
                duration = int(track.get("duration", 0))
                thumbnail = track.get("image", "").replace("150x150", "500x500")
                
                encrypted_media_url = track.get("encrypted_media_url", "")
                preview_url = track.get("media_preview_url", "")
                stream_urls_to_try = []
                
                if encrypted_media_url:
                    dec_url = decrypt_url(encrypted_media_url)
                    if dec_url:
                        stream_urls_to_try.append(dec_url.replace("_96.mp4", "_320.mp4").replace("_96_p.mp4", "_320.mp4"))
                        stream_urls_to_try.append(dec_url.replace("_96.mp4", "_160.mp4").replace("_96_p.mp4", "_160.mp4"))
                        stream_urls_to_try.append(dec_url)
                        
                if preview_url:
                    stream_urls_to_try.append(preview_url.replace("preview.saavncdn.com", "aac.saavncdn.com").replace("_96_p", "_320"))
                    stream_urls_to_try.append(preview_url.replace("preview.saavncdn.com", "aac.saavncdn.com"))

            await processing_msg.edit_text(f"⬇️ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʜᴅ: {title}...")
            file_path = f"downloads/{chat_id}_{song_id}.m4a"
            
            if not os.path.exists(file_path):
                for stream_url in stream_urls_to_try:
                    try:
                        async with session.get(stream_url, headers=HEADERS) as dl_resp:
                            if dl_resp.status == 200:
                                with open(file_path, "wb") as f: f.write(await dl_resp.read())
                                break 
                    except: continue

        if chat_id not in music_queue: music_queue[chat_id] = []
        song_details = {"title": title, "file_path": file_path, "duration": duration, "thumbnail": thumbnail, "requester": message.from_user.mention}
        music_queue[chat_id].append(song_details)

        bot_username = client.me.username
        play_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("▷", callback_data="resume"), InlineKeyboardButton("II", callback_data="pause"), InlineKeyboardButton("⏭", callback_data="skip"), InlineKeyboardButton("⏹", callback_data="stop")],
            [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ↗", url="https://t.me/rushdeveloper"), InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ↗", url="https://t.me/rushbots")],
            [InlineKeyboardButton("+ ᴀᴅᴅ ᴍᴇ +", url=f"https://t.me/{bot_username}?startgroup=true")]
        ])

        if len(music_queue[chat_id]) == 1:
            await call.play(chat_id, MediaStream(file_path))
            play_text = f"▶️ <b>sᴛᴀʀᴛᴇᴅ sᴛʀᴇᴀᴍɪɴɢ</b>\n\nᴛɪᴛʟᴇ : {title}\nᴅᴜʀᴀᴛɪᴏɴ : {duration} sᴇᴄᴏɴᴅs\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {song_details['requester']}"
            await message.reply_photo(photo=thumbnail, caption=play_text, reply_markup=play_buttons)
            await processing_msg.delete()
        else:
            position = len(music_queue[chat_id]) - 1
            queue_text = f"ᴀᴅᴅᴇᴅ ᴛᴏ ǫᴜᴇᴜᴇ ᴀᴛ #{position}\n\nᴛɪᴛʟᴇ : {title}\nᴅᴜʀᴀᴛɪᴏɴ : {duration} sᴇᴄᴏɴᴅs\nʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {song_details['requester']}"
            await processing_msg.edit_text(text=queue_text, reply_markup=play_buttons)

    except Exception as e:
        await processing_msg.edit_text(f"ᴇʀʀᴏʀ: {str(e)[:100]}")
              
