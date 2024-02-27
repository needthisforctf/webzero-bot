'''
Bot is used to declare a bot object and pass a token to it. 
Then Dispatcher hooks up to bot and starts polling it (see below). Dispatcher's job is to provide interface to hook handlers. 
types is used for type hinting like this: async def cmd_start(message: types.Message)
F is the filter function: https://mastergroosha.github.io/aiogram-3-guide/filters-and-middlewares/
'''
import asyncio # it's all async
from aiohttp import web # for healthcheck
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode # to specify Markdown_V2 or HTML as parsing mode without dragging all enums 
import helpers # our helper functions
from routers import message_monitor # importing routers

logging.basicConfig(level=logging.INFO)
# Running polling

async def run_health_check_server():
    app = web.Application()
    app.router.add_get('/healthcheck', (lambda requests: web.Response(text='Okay')))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 12345)
    await site.start()

async def bot():
    # Initialization
    token = helpers.get_arg('token')
    bot = Bot(token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    # Router hookup
    dp.include_routers(message_monitor.router) # check imports above

    # Initializing the bot 
    await bot.delete_webhook(drop_pending_updates=True) # yeah, we have polling, but the method is still available
    await dp.start_polling(bot)

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(bot())
        task2 = tg.create_task(run_health_check_server())

if __name__ == "__main__":
    asyncio.run(main())
