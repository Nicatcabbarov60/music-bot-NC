# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant
import asyncio
from DaisyXMusic.helpers.decorators import authorized_users_only
from DaisyXMusic.helpers.decorators import errors
from DaisyXMusic.services.callsmusic import client as USER
from DaisyXMusic.config import SUDO_USERS

@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Məni ilk öncə qrupun admini edin.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "UhuMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "Qrupa qatıldım.")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>userbot artıq qrupa qoşuldu</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🔴 Flood gözləmə xətası 🔴 \n{user.first_name}, bot həddindən çox qrupda məşğul olduğu üçün səsli söhbətə qoşula bilmədi! Və ya userbot(səsli söhbətə qoşulan musiqi plugini)-un qrupda ban olunmadığına əmin olun."
            "\n\nƏgər yuxarıdakılardan heç biri işinizə yaramadısa botu əl ilə qrupa əlavə edin və ya @UhuMusicSupport -a daxil olub dəstək istəyin.</b>",
        )
        return
    await message.reply_text(
        "<b>helper userbot joined your chat</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            f"<b>Userbot qrupdan çıxa bilmədi! Flood ola bilər. Zəhmət olmasa biraz sonra cəhd edin.."
            "\n\nvə ya manual olaraq məni qrupdan ata bilərsiniz./b>",
        )
        return
    
@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left=0
        failed=0
        lol = await message.reply("Assistant Leaving all chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left+1
                await lol.edit(f"Userbot ayrılır... Left: {left} chats. Failed: {failed} chats.")
            except:
                failed=failed+1
                await lol.edit(f"Assistant leaving... Left: {left} chats. Failed: {failed} chats.")
            await asyncio.sleep(0.7)
        await client.send_message(message.chat.id, f"Left {left} chats. Failed {failed} chats.")
    
    
@Client.on_message(filters.command(["userbotjoinchannel","ubjoinc"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Is chat even linked")
      return    
    chat_id = chid
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Məni ilk öncə kanalda admin edin.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "UhuMusic"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "Qoşuldum...")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>Userbot artıq kanala qoşuldu</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🔴 Flood gözləmə xətası 🔴 \n{user.first_name}, bot həddindən çox qrupda məşğul olduğu üçün səsli söhbətə qoşula bilmədi! Və ya userbot(səsli söhbətə qoşulan musiqi plugini)-un qrupda ban olunmadığına əmin olun."
            "\n\nƏgər yuxarıdakılardan heç biri işinizə yaramadısa botu əl ilə qrupa əlavə edin və ya @UhuMusicSupport -a daxil olub dəstək istəyin.</b>",
        )
        return
    await message.reply_text(
        "<b>userbot artıq qrupa qoşuldu.</b>",
    )
    
