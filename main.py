
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # Fixed class name
from config import Config
from bot.handlers import router
from database.models import init_db
from userbot.worker import Worker
from fastapi import FastAPI
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)

# Health check server for Render Free Tier
app = FastAPI()

@app.get("/")
async def health_check():
    return {"status": "running"}

async def start_bot():
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
    scheduler = AsyncIOScheduler() # Fixed class name
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

async def main():
    # Run both the Health Check Server and the Telegram Bot
    port = int(os.getenv("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    
    # Run server and bot concurrently
    await asyncio.gather(
        server.serve(),
        start_bot()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
