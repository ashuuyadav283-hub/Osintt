import logging
import aiohttp
import asyncio
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- CONFIGURATION ---
TOKEN = "8737206208:AAHY-O4lSnnm1BHIyzGANcCZuCXKZF4incU"
ADMIN_ID = 8335116442

logging.basicConfig(level=logging.INFO)

# --- HELPER FUNCTION ---
async def fetch_data(url: str) -> str:
    """Fetches data from the provided API URL."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as resp:
                return await resp.text()
    except Exception as e:
        return f"❌ API Error: {e}"

def format_response(raw_text: str) -> str:
    """Attempts to parse JSON gracefully to return a clean message."""
    try:
        data = json.loads(raw_text)
        # Customize this parsing based on the exact structure of your API
        if data.get("result", {}).get("success") == False:
            msg = data["result"].get("msg", "No records found.")
            return f"❌ {msg}\n\nby @Destroyerx10"
        
        # Pretty print successful JSON
        clean_info = json.dumps(data, indent=2)
        return f"✅ **Data Found:**\n```json\n{clean_info}\n```\n\nby @Destroyerx10"
    except Exception:
        # Fallback to raw text if it's not JSON
        return f"{raw_text}\n\nby @Destroyerx10"

# --- COMMAND HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = (
        "🤖 **Welcome to the Lookup Bot!**\n\n"
        "✦ ᴀᴀᴅʜᴀʀ → ɪɴꜰᴏ ✦ (`/aadhar <num>`)\n"
        "✦ ᴘᴀɴ → ɪɴꜰᴏ ✦ (`/pan <num>`)\n"
        "✦ ɴᴀᴍᴇ → ɪɴꜰᴏ ✦ (`/name <text>`)\n"
        "✦ ᴡᴇʙꜱɪᴛᴇ → ɪɴꜰᴏ ✦ (`/webinfo <url>`)\n"
        "✦ ᴇᴍᴀɪʟ → ɴᴜᴍ ✦ (`/email <email>`)\n"
        "✦ ɴᴜᴍ → ꜰᴜʟʟ ɪɴꜰᴏ ✦ (`/num <phone>`)\n"
        "✦ ᴡᴇʙꜱɪᴛᴇ → ɪᴅ & ᴘᴀꜱꜱᴡᴏʀᴅ ✦ (`/webcreds <url>`)\n"
        "✦ ᴛᴇʟᴇɢʀᴀᴍ → ɴᴜᴍ ✦ (`/tg <id>`)\n\n"
        "by @Destroyerx10"
    )
    await update.message.reply_markdown(menu)

async def handle_lookup(update: Update, context: ContextTypes.DEFAULT_TYPE, api_url_template: str, usage_msg: str):
    """Generic handler for processing the commands."""
    if not context.args:
        await update.message.reply_text(usage_msg)
        return

    query = context.args[0]
    url = api_url_template.format(query=query)
    
    # Send a temporary loading message
    loading_msg = await update.message.reply_text("⏳ Fetching data, please wait...")
    
    raw_result = await fetch_data(url)
    final_text = format_response(raw_result)
    
    # Edit the loading message with the final result
    await loading_msg.edit_text(final_text, parse_mode='Markdown')

# Individual Command Wrappers
async def aadhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/aadhar?q={query}", "Usage: /aadhar <number>")

async def pan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/pan?q={query}", "Usage: /pan <number>")

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/name?q={query}", "Usage: /name <text>")

async def webinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/webinfo?q={query}", "Usage: /webinfo <domain>")

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/email?q={query}", "Usage: /email <address>")

async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/num?q={query}", "Usage: /num <phone>")

async def webcreds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/webcreds?q={query}", "Usage: /webcreds <domain>")

async def tg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_lookup(update, context, "https://api.example.com/tg?q={query}", "Usage: /tg <id>")

# --- MAIN LOOP ---
def main():
    # Fix for Python 3.14+ Render environments
    asyncio.set_event_loop(asyncio.new_event_loop())
    
    app = ApplicationBuilder().token(TOKEN).build()

    # Register Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("aadhar", aadhar))
    app.add_handler(CommandHandler("pan", pan))
    app.add_handler(CommandHandler("name", name))
    app.add_handler(CommandHandler("webinfo", webinfo))
    app.add_handler(CommandHandler("email", email))
    app.add_handler(CommandHandler("num", num))
    app.add_handler(CommandHandler("webcreds", webcreds))
    app.add_handler(CommandHandler("tg", tg))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
