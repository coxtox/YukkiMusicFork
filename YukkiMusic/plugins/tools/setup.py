#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio

from pyrogram import filters

from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import maintenance_off, maintenance_on


async def chk_need_auth(timeout: int = 7):
    try:
        cmd = "yt-dlp --username oauth2 --password '' -F https://youtu.be/MCbM1PwjA5Y?si=LmWZ13qboKDMYtad"
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

        return stdout.decode(), stderr.decode(), process.returncode

    except asyncio.TimeoutError:
        process.kill()
        return None, None, None


@app.on_message(filters.command("setup") & SUDOERS)
async def setup_ytdlp(client, message):
    m = await message.reply_text(
        "ᴄʜᴇᴄᴋɪɴɢ ɪғ ʏᴛ-ᴅʟᴘ ɴᴇᴇᴅs ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ....", disable_web_page_preview=True
    )
    a, b, c = await chk_need_auth()

    if c == 0:
        await m.edit_text(
            "**ʏᴛ-ᴅʟᴘ ᴅᴏᴇs ɴᴏᴛ ʀᴇǫᴜɪʀᴇ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ.**",
            disable_web_page_preview=True,
        )
        return await maintenance_off()

    if b and "Login with password is not supported" in b:
        return await m.edit_text(
            "**ʏᴛ-ᴅʟᴘ ᴏᴀᴜᴛʜ2 ɪs ɴᴏᴛ ɪɴsᴛᴀʟʟᴇᴅ.**\n"
            "ᴘʟᴇᴀsᴇ ᴄᴏɴᴛᴀᴄᴛ ᴀᴛ [sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ](https://t.me/TheTeamVk).",
            disable_web_page_preview=True,
        )

    await m.edit_text(
        "> **ɴᴇᴇᴅᴇᴅ ʏᴛ-ᴅʟᴘ ᴀᴜᴛʜ**\n\n> ᴇɴᴀʙʟɪɴɢ **ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ**. ᴡʜɪʟᴇ ʏᴏᴜ ᴄᴏᴍᴘʟᴇᴛᴇ ʏᴏᴜʀ ᴀᴜᴛʜᴇɴᴛɪᴄᴀᴛɪᴏɴ, ʏᴏᴜʀ ʙᴏᴛ ᴡɪʟʟ ʙᴇ ɪɴ **ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ**. ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅɪsᴀʙʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴜsᴇ`/maintenance disable`.\n\n> ɪғ ʏᴏᴜ ɴᴇᴇᴅ ᴀɴʏ ʜᴇʟᴘ, [ᴄᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ](https://t.me/TheTeamVk).",
        disable_web_page_preview=True,
    )

    await maintenance_on()
