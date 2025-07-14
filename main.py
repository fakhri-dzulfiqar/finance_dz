import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler
)
from telegram import Update
from telegram.ext import ContextTypes

# Import handlers
from handlers.start import start_cmd
from handlers.export import export_cmd, export_excel
from handlers.grafik import grafik_cmd, grafik
from handlers.ringkasan import ringkasan_cmd, ringkasan
from handlers.transaksi import transaksi_handler
from handlers.help import help_command

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# --- Inline Button Callback ---
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'ringkasan':
        await ringkasan(update, context)
    elif query.data == 'grafik':
        await grafik(update, context)
    elif query.data == 'export':
        await export_excel(update, context)
    elif query.data == 'help':
        await help_command(update, context)

# --- Main ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command & message handlers
    app.add_handler(start_cmd)
    app.add_handler(export_cmd)
    app.add_handler(grafik_cmd)
    app.add_handler(ringkasan_cmd)
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(transaksi_handler)

    # Register inline button handler
    app.add_handler(CallbackQueryHandler(button_callback))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
