import os
import dotenv
import pixeldrain
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


dotenv.load_dotenv()

Bot = Client(
    "Pixeldrain-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """Hello {},
Please send a media for pixeldrain.com stream link. \
You can also send pixeldrain media ID or link to get more info.

Made by @FayasNoushad"""

BUTTON = InlineKeyboardButton(text="Feedback", url="https://telegram.me/FayasNoushad")


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup([[BUTTON]])
    )
    

def get_id(text):
    if text.startswith("http"):
        if text.endswith("/"):
            id = text.split("/")[-2]
        else:
            id = text.split("/")[-1]
    elif "/" not in text:
        id = text
    else:
        return None
    return id


async def send_data(id, message):
    # pixeldrain data
    try:
        data = pixeldrain.info(id)
    except Exception as error:
        data = None
    text = ""
    if data:
        text += f"**File Name:** `{data['name']}`" + "\n"
    text += f"**Download Page:** `https://pixeldrain.com/u/{id}`" + "\n"
    text += f"**Direct Download Link:** `https://pixeldrain.com/api/file/{id}`" + "\n"
    if data:
        text += f"**Upload Date:** `{data['date_upload']}`" + "\n"
        text += f"**Last View Date:** `{data['date_last_view']}`" + "\n"
        text += f"**Size:** `{data['size']}`" + "\n"
        text += f"**Total Views:** `{data['views']}`" + "\n"
        text += f"**Bandwidth Used:** `{data['bandwidth_used']}`" + "\n"
        text += f"**Mime Type:** `{data['mime_type']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Open Link",
                    url=f"https://pixeldrain.com/u/{id}"
                ),
                InlineKeyboardButton(
                    text="Share Link",
                    url=f"https://telegram.me/share/url?url=https://pixeldrain.com/u/{id}"
                )
            ],
            [BUTTON]
        ]
    )
    
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


@Bot.on_message(filters.private & filters.text)
async def info(bot, update):
    try:
        id = get_id(update.text)
        if id is None:
            return
    except:
        return
    
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    await send_data(id, message)


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    
    logs = []
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    
    try:
        # download
        try:
            await message.edit_text(
                text="`Downloading...`",
                disable_web_page_preview=True
            )
        except:
            pass
        media = await update.download()
        logs.append("Download Successfully")
        
        # upload
        try:
            await message.edit_text(
                text="`Uploading...`",
                disable_web_page_preview=True
            )
        except:
            pass
        response = pixeldrain.upload_file(media)
        # sleep
        
        
        try:
            os.remove(media)
        except:
            pass
        try:
            await message.edit_text(
                text="`Uploaded Successfully!`",
                disable_web_page_preview=True
            )
        except:
            pass
        logs.append("Upload Successfully")
        
        # after upload
        if response["success"]:
            logs.append("Success is True")
            await send_data(response["id"], message)
        else:
            logs.append("Success is False")
            value = response["value"]
            error = response["message"]
            await message.edit_text(
                text=f"**Error {value}:-** `{error}`",
                disable_web_page_preview=True
            )
            
    except Exception as error:
        await message.edit_text(
            text=f"Error :- `{error}`"+"\n\n"+'\n'.join(logs),
            disable_web_page_preview=True
        )


Bot.run()
