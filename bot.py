import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("ERREUR : BOT_TOKEN manquant")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue !\n\n"
        "Bot de prédictions *simulées* (démo).\n"
        "Clique pour recevoir une prédiction."
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    prob = random.randint(60, 95)
    mult = round(random.uniform(1.5, 5.0), 2)
    time_now = datetime.now().strftime("%H:%M:%S")

    await query.message.reply_text(
        f"🔮 Prédiction simulée\n\n"
        f"🕒 Heure : {time_now}\n"
        f"📊 Probabilité : {prob}%\n"
        f"✈️ Multiplicateur : x{mult}\n\n"
        f"⚠️ Simulation uniquement"
    )

app = ApplicationBuilder().token(TOKEN).build()

keyboard = [[InlineKeyboardButton("🔮 Nouvelle prédiction", callback_data="predict")]]
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(predict, pattern="predict"))

app.run_polling()
