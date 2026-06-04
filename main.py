
import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncioScheduler
from config import Config
from bot.handlers import router
from database.models import init_db
from userbot.worker import Worker

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize Database
    init_db()

    # Initialize Admin Bot
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # Initialize Worker
    worker = Worker(bot)
    await worker.start_clients()

    # Initialize Scheduler
    scheduler = AsyncioScheduler()
    # Add the worker task to run every X minutes
    scheduler.add_job(
        worker.run_task,
        "interval",
        minutes=Config.DEFAULT_SEND_INTERVAL_MINUTES,
        id="broadcast_job"
    )
    scheduler.start()

    logging.info("Bot and Scheduler started...")

    try:
        # Start Polling
        await dp.start_polling(bot)
    finally:
        await worker.stop_clients()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
