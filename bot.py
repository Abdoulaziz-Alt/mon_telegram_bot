import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN manquant. Vérifie la variable d'environnement sur Render.")

# ===== COMMANDES =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎯 Nouvelle prédiction", callback_data="predict")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bienvenue dans le bot *Lucky Jet Predictor* 🚀\n\n"
        "Appuie sur *Nouvelle prédiction* pour recevoir une estimation.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    crash_value = round(random.uniform(1.00, 60.00), 2)
    await query.message.reply_text(
        f"🚀 *Prédiction Lucky Jet*\n\n"
        f"💥 Crash estimé à : *{crash_value}x*",
        parse_mode="Markdown"
    )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(prediction, pattern="^predict$"))

    print("🤖 Bot Lucky Jet Predictor lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
