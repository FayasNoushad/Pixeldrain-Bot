import os
import pixeldrain
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Pixeldrain-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention}, Please send a media for pixeldrain.com stream link.\n\nMade by @FayasNoushad",
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.media)
async def media_filter(bot, update):
    
    logs = ""
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    
    try:
        # download
        await message.edit_text(
            text="`Downloading...`",
            disable_web_page_preview=True
        )
        media = await update.download()
        logs += "Download Successfully"
        
        # upload
        await message.edit_text(
            text="`Uploading...`",
            disable_web_page_preview=True
        )
        response = pixeldrain.upload_file(media)
        
        try:
            os.remove(media)
        except:
            pass
        
        await message.edit_text(
            text="`Uploaded Successfully!`",
            disable_web_page_preview=True
        )
        logs += "\n" + "Upload Successfully"
        
        # not success
        if response["success"] is False:
            await message.edit_text(
                text=f"**Error {response.status_code}:-** `I can't fetch information of your file.`",
                disable_web_page_preview=True
            )
            return
    except Exception as error:
        if "MESSAGE_NOT_MODIFIED" in error:
            pass
        else:
            await message.edit_text(
                text=f"Error :- `{error}`\n\n`{logs}`",
                disable_web_page_preview=True
            )
            return
    
    # pixeldrain data
    data = pixeldrain.info(response.json()["id"])
    text = f"**File Name:** `{data['name']}`" + "\n"
    text += f"**Download Page:** `https://pixeldrain.com/u/{data['id']}`" + "\n"
    text += f"**Direct Download Link:** `https://pixeldrain.com/api/file/{data['id']}`" + "\n"
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
                    url=f"https://pixeldrain.com/u/{data['id']}"
                ),
                InlineKeyboardButton(
                    text="Share Link",
                    url=f"https://telegram.me/share/url?url=https://pixeldrain.com/u/{data['id']}"
                )
            ],
            [
                InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/FayasNoushad")
            ]
        ]
    )
    
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
