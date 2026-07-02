import logging
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ⚠️ PUT YOUR NEW TOKEN HERE (after revoke)
TOKEN = "8737206208:AAEINhgDkzsSFbBGo-fmO4FgMTHfhMJYADs"

ADMIN_ID = 8335116442

logging.basicConfig(level=logging.INFO)


# ---------- Helpers ----------
async def fetch_text(url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=20) as resp:
                return await resp.text()
    except Exception as e:
        return f"API Error: {e}"


# ---------- Commands ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Started!\n\n"
        "Commands:\n"
        "/adhar <num>\n"
        "/pan <num>\n"
        "/name <text>\n"
        "/website <id>\n"
        "/num <phone>\n"
        "/email <email>"
    )


async def adhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /adhar 123456789012")

    num = context.args[0]
    url = f"https://allinone-ofl0.onrender.com/all-in-one?q={num}"
    result = await fetch_text(url)
    await update.message.reply_text(result)


async def pan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /pan ABCDE1234F")

    pan_no = context.args[0]
    url = f"https://allinone-ofl0.onrender.com/all-in-one?q={pan_no}"
    result = await fetch_text(url)
    await update.message.reply_text(result)


async def num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /num 1234567890")

    phone = context.args[0]
    url = f"https://tg-to-num-rate-limit.onrender.com/TG/user/={phone}"
    result = await fetch_text(url)
    await update.message.reply_text(result)


async def website(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /website <id>")

    wid = context.args[0]
    await update.message.reply_text(
        f"Website Info Request:\nID: {wid}\n(Not configured fully yet)"
    )


# ---------- Main ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("adhar", adhar))
    app.add_handler(CommandHandler("pan", pan))
    app.add_handler(CommandHandler("num", num))
    app.add_handler(CommandHandler("website", website))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
