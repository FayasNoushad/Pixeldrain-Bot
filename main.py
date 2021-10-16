# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Pixeldrain-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
import pixeldrain


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
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    try:
        await message.edit_text(
            text="`Downloading...`",
            disable_web_page_preview=True
        )
        media = await update.download()
        await message.edit_text(
            text="`Uploading...`",
            disable_web_page_preview=True
        )
        response = pixeldrain.upload_file(media)
        try:
            os.remove(media)
        except:
            pass 
        if not response:
            await message.edit_text(
                text="`I can't upload this file.`",
                disable_web_page_preview=True
            )
            return
    except Exception as error:
        await message.edit_text(
            text=f"Error :- <code>{error}</code>",
            quote=True,
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{response['name']}`" + "\n"
    text += f"**Download Page:** `https://pixeldrain.com/u/{response['id']}`" + "\n"
    text += f"**Direct Download Link:** `https://pixeldrain.com/api/file/{response['id']}`" + "\n"
    text += f"**Upload Date:** `{response['date_upload']}`"
    text += f"**Last View Date:** `{response['date_last_view']}`"
    text += f"**Size:** `{response['size']}`"
    text += f"**Total Views:** `{response['views']}`"
    text += f"**Bandwidth Used:** `{response['bandwidth_used']}`"
    text += f"**Mime Type:** `{response['mime_type']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Open Link",
                    url=f"https://pixeldrain.com/api/file/{response['id']}"
                ),
                InlineKeyboardButton(
                    text="Share Link",
                    url=f"https://telegram.me/share/url?url=https://pixeldrain.com/api/file/{response['id']}"
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
