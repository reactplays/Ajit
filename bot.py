import logging
import sqlite3
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ChatJoinRequestHandler, MessageHandler, filters, ContextTypes
)

# ─── CONFIG ───────────────────────────────────────────────
BOT_TOKEN = os.getenv("8814260946:AAFCBD4RRciHpGXAJMUrYVFgiZZHGHV1Dc8")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN env var not set")

ADMIN_ID = 8387890264
CHANNEL_IDS = [-1001544229917, -1001209826602]
DB_PATH = "users.db"

WHATSAPP_LINK = "https://wa.me/919596493523"
BACKUP_CHANNEL = "https://t.me/+JvigXCD_ts9hNjhl"
OWNER_USERNAME = "https://t.me/DevilAjitMods"
IOS_POST = "https://t.me/iOSZERO_WINiOS/5781"
ANDROID_POST = "https://t.me/BGMILOADER_TG/7657"

# ─── LOGGING ──────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── DATABASE ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_user(user):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user.id, user.username, user.first_name))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT user_id FROM users").fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_user_count():
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return count

def get_user_info(user_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT user_id, username, first_name, joined_at FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    conn.close()
    return row

def remove_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

def manual_add_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id, None, "Manual"))
    conn.commit()
    conn.close()

# ─── AUTO ACCEPT + WELCOME ────────────────────────────────
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    req = update.chat_join_request
    user = req.from_user

    await context.bot.approve_chat_join_request(
        chat_id=req.chat.id,
        user_id=user.id
    )

    save_user(user)

    try:
        keyboard = [
            [
                InlineKeyboardButton("💬 Paid Hack Free", url=OWNER_USERNAME),
                InlineKeyboardButton("📢 Backup Channel", url=BACKUP_CHANNEL)
            ]
        ]
        await context.bot.send_message(
            chat_id=user.id,
            text=(
                f"✅ *Request Approved* 🤝\n\n"
                f"Welcome *{user.first_name}* 🎮\n"
                f"Here We're for the Ultimate Experience of Mobile Gaming World 👑\n\n"
                "━━━━━━━━━━━━━━━━━━━\n"
                "👤 Contact Owner Directly 👨‍💼\n"
                "📌 Join our Backup Channel, Never miss an update 🔗"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        logger.warning(f"Could not send welcome to {user.id}: {e}")

    logger.info(f"Approved + welcomed: {user.id}")

# ─── /start ───────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user)

    await update.message.reply_text(
        f"👋 *Welcome, {user.first_name}!*\n\n"
        "👨🏻‍🔧 Use contact button or /help",
        parse_mode="Markdown"
    )

# ─── /help ────────────────────────────────────────────────
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hey *{user.first_name}*, I'm Auto Reply Bot 🤖\n"
        "Here are your Commands\n\n"
        "/iOS — iOS Users\n"
        "/Android — Android Users\n"
        "/Owner — Contact Owner",
        parse_mode="Markdown"
    )

# ─── /iOS ─────────────────────────────────────────────────
async def ios_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📲 View Post", url=IOS_POST)],
        [InlineKeyboardButton("💬 Paid Hack Free", url=OWNER_USERNAME)]
    ]
    await update.message.reply_text(
        "Bhai, full safe hai IOS HACK 👍\n\n"
        "👇 Gameplay / Feedback Check:\n"
        f"{IOS_POST}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

# ─── /Android ─────────────────────────────────────────────
async def android_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("📲 View Post", url=ANDROID_POST)],
        [InlineKeyboardButton("💬 Paid Hack Free", url=OWNER_USERNAME)]
    ]
    await update.message.reply_text(
        "Bhai, full safe hai Android HACK 👍\n\n"
        "👇 Gameplay / Feedback Check:\n"
        f"{ANDROID_POST}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

# ─── /Owner ───────────────────────────────────────────────
async def owner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("💬 Telegram", url=OWNER_USERNAME)],
        [InlineKeyboardButton("📲 WhatsApp", url=WHATSAPP_LINK)]
    ]
    await update.message.reply_text(
        f"*{user.first_name}*, contact us here 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ─── /announce (ADMIN ONLY) ───────────────────────────────
# Usage:
#   Text only:              /announce Your message here
#   With custom button:     /announce Your message | Button Text | https://link.com
#   With image/video:       Reply to a photo/video and type /announce Your message
async def announce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied.")
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ *Usage:*\n\n"
            "Text only:\n`/announce Your message`\n\n"
            "With custom button:\n`/announce Your message | Button Text | https://link.com`\n\n"
            "With image/video:\nReply to a photo/video and type `/announce Your message`",
            parse_mode="Markdown"
        )
        return

    full_text = " ".join(context.args)

    # Parse custom button if provided
    parts = full_text.split("|")
    message = parts[0].strip()
    custom_keyboard = None

    if len(parts) == 3:
        btn_text = parts[1].strip()
        btn_url = parts[2].strip()
        custom_keyboard = [[InlineKeyboardButton(btn_text, url=btn_url)]]
    else:
        custom_keyboard = [[InlineKeyboardButton("💬 Paid Hack Free", url=OWNER_USERNAME)]]

    markup = InlineKeyboardMarkup(custom_keyboard)
    users = get_all_users()
    sent, failed = 0, 0

    status_msg = await update.message.reply_text(f"📤 Broadcasting to {len(users)} users...")

    # Check if replying to a photo or video
    reply = update.message.reply_to_message

    for uid in users:
        try:
            if reply and reply.photo:
                await context.bot.send_photo(
                    chat_id=uid,
                    photo=reply.photo[-1].file_id,
                    caption=f"📢 *Announcement*\n\n{message}",
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            elif reply and reply.video:
                await context.bot.send_video(
                    chat_id=uid,
                    video=reply.video.file_id,
                    caption=f"📢 *Announcement*\n\n{message}",
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            else:
                await context.bot.send_message(
                    chat_id=uid,
                    text=f"📢 *Announcement*\n\n{message}",
                    parse_mode="Markdown",
                    reply_markup=markup
                )
            sent += 1
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ *Broadcast Done!*\n\n"
        f"📨 Sent: {sent}\n"
        f"❌ Failed: {failed}",
        parse_mode="Markdown"
    )

# ─── /stats (ADMIN ONLY) ──────────────────────────────────
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied.")
        return

    count = get_user_count()
    await update.message.reply_text(
        f"📊 *Bot Stats*\n\n"
        f"👥 Total Users: `{count}`",
        parse_mode="Markdown"
    )

# ─── /adduser (ADMIN ONLY) ────────────────────────────────
async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/adduser 123456789`", parse_mode="Markdown")
        return

    try:
        uid = int(context.args[0])
        manual_add_user(uid)
        await update.message.reply_text(f"✅ User `{uid}` added to DB.", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ Invalid ID. Numbers only.")

# ─── /removeuser (ADMIN ONLY) ─────────────────────────────
async def removeuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/removeuser 123456789`", parse_mode="Markdown")
        return

    try:
        uid = int(context.args[0])
        remove_user(uid)
        await update.message.reply_text(f"✅ User `{uid}` removed from DB.", parse_mode="Markdown")
    except ValueError:
        await update.message.reply_text("❌ Invalid ID. Numbers only.")

# ─── /userinfo (ADMIN ONLY) ───────────────────────────────
async def userinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Usage: `/userinfo 123456789`", parse_mode="Markdown")
        return

    try:
        uid = int(context.args[0])
        row = get_user_info(uid)
        if row:
            await update.message.reply_text(
                f"👤 *User Info*\n\n"
                f"🆔 ID: `{row[0]}`\n"
                f"👤 Name: {row[2]}\n"
                f"🔗 Username: @{row[1] if row[1] else 'hidden'}\n"
                f"📅 Joined: {row[3]}",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ User not found in DB.")
    except ValueError:
        await update.message.reply_text("❌ Invalid ID. Numbers only.")

# ─── AUTO REPLY ───────────────────────────────────────────
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower() if update.message.text else ""
    user = update.effective_user

    if any(k in text for k in ["buy", "purchase", "hack"]):
        await owner_cmd(update, context)

    elif "android" in text:
        await android_cmd(update, context)

    elif "ios" in text:
        await ios_cmd(update, context)

    elif any(k in text for k in ["hi", "hey", "hello"]):
        await update.message.reply_text(
            f"Hey *{user.first_name}*! 👋\n\nUse /help to see available commands.",
            parse_mode="Markdown"
        )

    else:
        await update.message.reply_text(
            f"*{user.first_name}*, I didn't get that 🤖\n\nUse /help to see available commands.",
            parse_mode="Markdown"
        )

# ─── MAIN ─────────────────────────────────────────────────
def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("iOS", ios_cmd))
    app.add_handler(CommandHandler("Android", android_cmd))
    app.add_handler(CommandHandler("Owner", owner_cmd))
    app.add_handler(CommandHandler("announce", announce))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("adduser", adduser))
    app.add_handler(CommandHandler("removeuser", removeuser))
    app.add_handler(CommandHandler("userinfo", userinfo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    logger.info("Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
