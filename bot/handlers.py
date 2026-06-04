
from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from database.models import SessionLocal
from database.crud import create_message, create_group, get_groups, delete_group, delete_all_groups, get_group_by_link
from config import Config

router = Router()

def is_admin(user_id: int):
    return user_id == Config.ADMIN_ID

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("Welcome Admin! You can use commands like /msg, /gp, /time, /editgp to control the userbots.")

@router.message(Command("msg"))
async def msg_cmd(message: types.Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    if not command.args:
        await message.answer("Please provide the text: /msg <text>")
        return
    
    db = SessionLocal()
    create_message(db, command.args)
    db.close()
    await message.answer(f"Message saved: {command.args}")

@router.message(Command("gp"))
async def gp_cmd(message: types.Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    
    db = SessionLocal()
    if not command.args:
        groups = get_groups(db)
        if not groups:
            await message.answer("No groups found in database.")
        else:
            links = "\n".join([g.link for g in groups])
            await message.answer(f"Current Groups:\n{links}")
    else:
        links = [link.strip() for link in command.args.split(",")]
        added_count = 0
        for link in links:
            if not get_group_by_link(db, link):
                create_group(db, link)
                added_count += 1
        await message.answer(f"Added {added_count} groups to the database.")
    db.close()

@router.message(Command("editgp"))
async def editgp_cmd(message: types.Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    
    if not command.args:
        await message.answer("Usage: /editgp remove <link> or /editgp clear")
        return
    
    args = command.args.split()
    db = SessionLocal()
    if args[0] == "remove" and len(args) > 1:
        if delete_group(db, args[1]):
            await message.answer(f"Removed group: {args[1]}")
        else:
            await message.answer(f"Group not found: {args[1]}")
    elif args[0] == "clear":
        delete_all_groups(db)
        await message.answer("Cleared all groups.")
    else:
        await message.answer("Invalid usage. Use /editgp remove <link> or /editgp clear")
    db.close()

@router.message(Command("time"))
async def time_cmd(message: types.Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return
    
    if not command.args:
        await message.answer("Please provide the time: /time <minutes>min")
        return
    
    # This command will be handled in the main scheduler loop
    # For now, we just acknowledge it
    await message.answer(f"Setting interval to {command.args}. Please restart the bot to apply changes if not using a dynamic scheduler.")
