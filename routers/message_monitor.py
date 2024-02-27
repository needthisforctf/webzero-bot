import asyncio
from aiogram import Router, F # Routers are under DP, F is a magic filter
from aiogram.types import Message # for type hinting
# from aiogram.filters import Command, Filter # to specify things like /start or /hello
from aiogram.enums import MessageEntityType # we want to check message entity types
from aiogram.exceptions import TelegramBadRequest
from nftparser import fetch2check as f2c
from helpers import link_normalizer

router = Router()
router.message.filter(F.chat.type != "private")
async def del_msg(msg: Message):
    try:
        await msg.delete()
        await msg.answer(f'Removed spam by {"<code>@"+msg.from_user.username+"</code>" or msg.from_user.full_name}')
    except TelegramBadRequest as e:
        await msg.answer(f"Bot doesn't have rights to remove <a href=\"{msg.get_url()}\">the message™.</a>")

@router.message(F.entities[...].type == MessageEntityType.URL)# if message contains an URL anywhere…
async def link_squash(message: Message):
    link_coros = [
        f2c(link_normalizer(e.extract_from(message.text))) # extract and check the link, returns True if it's a spam
        for e in message.entities  # among entities
        if e.type == 'url' # that are url
        ]
    for coro in asyncio.as_completed(link_coros):
        if (await coro):
                await del_msg(message)
                break
            
@router.message(F.entities[...].type == MessageEntityType.TEXT_LINK)
async def textlink_squash(message: Message):
    textlink_coros = [
        f2c(link_normalizer(e.url))
        for e in message.entities
        if e.type == 'text_link'
    ]

    for coro in asyncio.as_completed(textlink_coros):
        if (await coro):
            await del_msg(message)
            break

# TODOS
# Make urls fetchable from network
# Actually implement actions: banning, muting, deleting            