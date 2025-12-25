import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ===== CONFIG =====
ACCESS_CODE = "python123"
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Vérification du token
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN manquant. Vérifie la variable d'environnement sur Render.")

users_verified = set()

# ===== COMMANDES =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue dans le bot *Lucky Jet Predictor* 🚀\n\n"
        "🔐 Veuillez entrer votre *code d'accès* pour continuer.",
        parse_mode="Markdown"
    )

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    code = update.message.text.strip()

    if user_id in users_verified:
        return  # déjà vérifié

    if code == ACCESS_CODE:
        users_verified.add(user_id)
        keyboard = [
            [InlineKeyboardButton("🎯 Nouvelle prédiction", callback_data="predict")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "✅ *Bienvenue sur Lucky Jet Predictor*\n\n"
            "📊 Appuie sur *Nouvelle prédiction* pour recevoir une estimation.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("❌ Code incorrect. Réessaie.")

async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in users_verified:
        await query.message.reply_text("🔐 Accès refusé. Entre d'abord le code.")
        return

    crash_value = round(random.uniform(1.00, 60.00), 2)
    probability = random.randint(5, 95)

    await query.message.reply_text(
        f"🚀 *Prédiction Lucky Jet*\n\n"
        f"💥 Crash estimé à : *{crash_value}x*\n"
        f"📈 Probabilité : *{probability}%*\n\n"
        f"⏰ Heure actuelle utilisée pour la prédiction.",
        parse_mode="Markdown"
    )

# ===== MAIN =====
def main():
    # ✅ ApplicationBuilder utilisé à la place d'Updater
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(prediction, pattern="^predict$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    print("🤖 Bot Lucky Jet Predictor lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
