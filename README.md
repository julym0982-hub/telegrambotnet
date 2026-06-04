
# Telegram Userbot Controller (Automation Bot)

This project implements a Telegram Userbot Controller, designed to automate sending messages to multiple Telegram groups using a set of userbot accounts. It features an Admin Control Bot for easy management, a robust queue and reporting system, and crucial anti-ban/anti-spam measures to ensure account safety.

## Features

1.  **Admin Control Bot (via aiogram)**:
    *   `/msg <text>`: Save the message text to be broadcasted to groups.
    *   `/gp <link1>, <link2>, ...`: Add Telegram group links to the database. These links are persistent.
    *   `/gp`: Display all currently saved group links.
    *   `/editgp remove <link>`: Remove a specific group link.
    *   `/editgp clear`: Clear all saved group links.
    *   `/time <minutes>min`: Set the interval for message broadcasting (e.g., `/time 5min`).

2.  **Queue & Reporting System**:
    *   Messages are sent to groups sequentially, one by one.
    *   Admin receives "send X done" notifications upon successful delivery.
    *   Admin receives "fail send X" notifications if an error occurs, and the process continues to the next group.

3.  **Anti-Ban & Anti-Spam Measures (Crucial for Userbot Safety)**:
    *   **Random Delays**: A random delay of 10 to 30 seconds is introduced between sending messages to different groups (`time.sleep(random.randint(10, 30))`).
    *   **Message Spinning/Variation**: Supports Spintax format (`{Hello|Hi} there!`) to vary message content, making each message unique and reducing the likelihood of being flagged as spam.
    *   **Account Rotation (Multi-Client)**: Utilizes multiple Pyrogram userbot accounts (clients) in a round-robin or random fashion to distribute sending load and minimize the risk of a single account being banned.

## Project Structure

```
telegram_userbot_controller/
├── bot/
│   └── handlers.py             # Admin Bot command handlers
├── database/
│   ├── crud.py                 # Database Create, Read, Update, Delete operations
│   └── models.py               # SQLAlchemy models for Message and Group
├── userbot/
│   └── worker.py               # Userbot logic, message sending, anti-spam measures
├── config.py                   # Configuration settings and environment variable loading
├── main.py                     # Main entry point, initializes bot, worker, and scheduler
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment configuration
└── .env.example                # Example environment variables file
```

## Prerequisites

Before you begin, ensure you have the following:

*   **Python 3.9+** installed.
*   **Telegram Bot Token**: Obtain this from BotFather on Telegram.
*   **Telegram API ID & API Hash**: Get these from [my.telegram.org](https://my.telegram.org/).
*   **Admin User ID**: Your personal Telegram User ID, which will be the only ID allowed to control the bot.
*   **Pyrogram Session Strings**: You will need to generate session strings for each userbot account you wish to use. See the "Generating Pyrogram Session Strings" section below.

## Local Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/telegram-userbot-controller.git # Replace with your repo URL
    cd telegram_userbot_controller
    ```

2.  **Create a virtual environment and install dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Create a `.env` file in the root directory of the project based on `.env.example` and fill in your credentials:
    ```ini
    BOT_TOKEN=YOUR_BOT_TOKEN
    ADMIN_ID=YOUR_TELEGRAM_ADMIN_USER_ID
    API_ID=YOUR_TELEGRAM_API_ID
    API_HASH=YOUR_TELEGRAM_API_HASH
    SESSION_STRINGS=SESSION_STRING_1,SESSION_STRING_2,SESSION_STRING_3 # Comma-separated session strings
    DEFAULT_SEND_INTERVAL_MINUTES=5
    MIN_RANDOM_DELAY=10
    MAX_RANDOM_DELAY=30
    ```
    *   `BOT_TOKEN`: The token for your Admin Bot from BotFather.
    *   `ADMIN_ID`: Your Telegram user ID (numeric).
    *   `API_ID`, `API_HASH`: Your API credentials from my.telegram.org.
    *   `SESSION_STRINGS`: Comma-separated Pyrogram session strings for your userbot accounts. **This is crucial for account rotation.**
    *   `DEFAULT_SEND_INTERVAL_MINUTES`: How often the userbot will attempt to send messages (default: 5 minutes).
    *   `MIN_RANDOM_DELAY`, `MAX_RANDOM_DELAY`: The range for random delays between sending messages to groups (in seconds).

4.  **Generating Pyrogram Session Strings**:
    You need to generate a session string for each userbot account. Create a temporary Python script (e.g., `generate_session.py`):
    ```python
    from pyrogram import Client
    import asyncio
    from config import Config

    async def generate_session():
        api_id = Config.API_ID
        api_hash = Config.API_HASH
        
        # Replace 'my_account_session' with a unique name for each session
        # Run this script for each account you want to add.
        async with Client("my_account_session", api_id, api_hash) as app:
            print(f"Session string for 'my_account_session': {app.export_session_string()}")

    if __name__ == "__main__":
        asyncio.run(generate_session())
    ```
    Run this script for each userbot account. It will prompt you for your phone number and the OTP. Copy the generated session string and add it to the `SESSION_STRINGS` environment variable in your `.env` file (comma-separated for multiple sessions).

5.  **Run the Bot**:
    ```bash
    python main.py
    ```
    Your Admin Bot will start, and the userbots will be ready to send messages according to the schedule.

## Usage

Interact with your Admin Bot on Telegram using the commands listed in the Features section. Ensure you are using the Telegram account specified as `ADMIN_ID` in your configuration.

## Deployment on Render

Render provides a convenient platform for deploying Python applications. This project includes a `render.yaml` file for easy deployment as a Worker service.

1.  **Create a Render Account**: If you don't have one, sign up at [render.com](https://render.com/).

2.  **Fork this Repository**: Fork the project to your own GitHub account. This allows Render to access your code.

3.  **Create a New Worker on Render**:
    *   Go to your Render Dashboard.
    *   Click "New" -> "Worker".
    *   Select "Build and deploy from a Git repository".
    *   Connect your GitHub account and select your forked repository.

4.  **Configure the Worker**:
    Render will detect the `render.yaml` file and pre-fill most settings. Verify the following:
    *   **Name**: `telegram-userbot-controller` (or your preferred name)
    *   **Environment**: `Python`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `python main.py`

5.  **Set Environment Variables**:
    This is critical. In the Render dashboard for your service, navigate to "Environment" and add the following environment variables. **Do not hardcode sensitive information in `config.py` for production deployments.**

    | Key                             | Value                                       | Description                                                               |
    | :------------------------------ | :------------------------------------------ | :------------------------------------------------------------------------ |
    | `BOT_TOKEN`                     | `YOUR_BOT_TOKEN`                            | Token for your Admin Bot from BotFather.                                  |
    | `ADMIN_ID`                      | `YOUR_TELEGRAM_ADMIN_USER_ID`               | Your Telegram user ID (numeric).                                          |
    | `API_ID`                        | `YOUR_TELEGRAM_API_ID`                      | Your API ID from my.telegram.org.                                         |
    | `API_HASH`                      | `YOUR_TELEGRAM_API_HASH`                    | Your API Hash from my.telegram.org.                                       |
    | `SESSION_STRINGS`               | `SESSION_STRING_1,SESSION_STRING_2,...`     | Comma-separated Pyrogram session strings for your userbot accounts.       |
    | `DATABASE_URL`                  | `sqlite:///./database/bot.db`               | (Default, usually doesn't need change for SQLite)                         |
    | `DEFAULT_SEND_INTERVAL_MINUTES` | `5`                                         | How often the userbot will attempt to send messages (in minutes).         |
    | `MIN_RANDOM_DELAY`              | `10`                                        | Minimum random delay between group messages (in seconds).                 |
    | `MAX_RANDOM_DELAY`              | `30`                                        | Maximum random delay between group messages (in seconds).                 |

6.  **Disk Persistence for SQLite**:
    The `render.yaml` file includes a `disk` configuration to ensure your SQLite database (`bot.db`) persists across deployments and restarts. This is mounted to `/home/render/project/src/database`.

7.  **Deploy**: Click "Create Worker". Render will build and deploy your application. You can monitor the deployment logs in the Render dashboard.

## Generating Pyrogram Session Strings (for Render Deployment)

Since you cannot run the `generate_session.py` script directly on Render's build environment (it requires interactive input), you should generate these session strings **locally** first and then add them to the `SESSION_STRINGS` environment variable on Render.

Follow step 4 in the "Local Setup" section to generate your session strings, then copy them to the `SESSION_STRINGS` environment variable in your Render service settings.

## Troubleshooting

*   **Bot not responding**: Check your `BOT_TOKEN` and `ADMIN_ID` in Render environment variables. Ensure the bot is running on Render and there are no errors in the logs.
*   **Userbot not sending messages**: Verify `API_ID`, `API_HASH`, and `SESSION_STRINGS`. Ensure the userbot accounts are not banned or restricted by Telegram. Check Render logs for Pyrogram errors.
*   **Database issues**: Ensure the disk is correctly mounted on Render and the `DATABASE_URL` is correct. For SQLite, the provided `render.yaml` should handle persistence.
*   **Scheduler not running**: Check `DEFAULT_SEND_INTERVAL_MINUTES` and ensure the `main.py` process is active on Render.

---

**Author**: Manus AI
**Date**: June 04, 2026
