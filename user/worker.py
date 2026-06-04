
import asyncio
import random
import re
from pyrogram import Client
from database.models import SessionLocal
from database.crud import get_message, get_groups
from config import Config

def spin_text(text: str) -> str:
    """
    Simple spintax parser for {word1|word2|word3} format.
    """
    def replace(match):
        options = match.group(1).split('|')
        return random.choice(options)
    
    pattern = r'\{([^{}]+)\}'
    while re.search(pattern, text):
        text = re.sub(pattern, replace, text)
    return text

async def send_notifications(bot, text):
    try:
        await bot.send_message(Config.ADMIN_ID, text)
    except Exception as e:
        print(f"Failed to send notification to admin: {e}")

class Worker:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.clients = []
        for i, session_string in enumerate(Config.SESSION_STRINGS):
            if session_string:
                client = Client(
                    name=f"worker_{i}",
                    api_id=Config.API_ID,
                    api_hash=Config.API_HASH,
                    session_string=session_string,
                    in_memory=True
                )
                self.clients.append(client)

    async def start_clients(self):
        for client in self.clients:
            await client.start()

    async def stop_clients(self):
        for client in self.clients:
            await client.stop()

    async def run_task(self):
        if not self.clients:
            await send_notifications(self.bot, "Error: No userbot clients configured!")
            return

        db = SessionLocal()
        message_obj = get_message(db)
        groups = get_groups(db)
        db.close()

        if not message_obj or not groups:
            await send_notifications(self.bot, "Warning: Message or Groups list is empty. Skipping task.")
            return

        raw_text = message_obj.text
        
        # Shuffle groups for each run to be less predictable
        group_list = [g.link for g in groups]
        random.shuffle(group_list)

        for idx, group_link in enumerate(group_list):
            # Account Rotation: Choose client in round-robin or random
            client = random.choice(self.clients)
            
            # Spin text for each message
            text_to_send = spin_text(raw_text)
            
            try:
                # Resolve group link (can be @username or join link)
                chat = await client.get_chat(group_link)
                await client.send_message(chat.id, text_to_send)
                await send_notifications(self.bot, f"send {idx + 1} done to {group_link}")
            except Exception as e:
                await send_notifications(self.bot, f"fail send {idx + 1} to {group_link}: {str(e)}")
            
            # Random Delay between groups
            if idx < len(group_list) - 1:
                delay = random.randint(Config.MIN_RANDOM_DELAY, Config.MAX_RANDOM_DELAY)
                await asyncio.sleep(delay)
