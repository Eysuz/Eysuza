from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Xona holati
room_status = None

# Botni boshlash
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Namoz o'qish xonasiga kirish va chiqish uchun quyidagi buyruqlarni ishlating:\n"
        "/enter - Xonaga kirish\n"
        "/exit - Xonadan chiqish\n"
        "/status - Xona holatini ko'rish"
    )

# Xona holatini ko'rsatish
async def status(update: Update, context: CallbackContext) -> None:
    if room_status:
        await update.message.reply_text(f"Xona band. Hozirda {room_status} namoz o'qiyapti.")
    else:
        await update.message.reply_text("Xona bo'sh. Hozirda hech kim namoz o'qimayapti.")

# Xonaga kirish
async def enter(update: Update, context: CallbackContext) -> None:
    global room_status
    
    if room_status:
        await update.message.reply_text(f"Xona band. {room_status} hozir namoz o'qiyapti.")
    else:
        room_status = update.message.from_user.first_name
        await update.message.reply_text(f"Siz xonaga kirdingiz. Hozirda {room_status} namoz o'qiydi.")

# Xonadan chiqish
async def exit(update: Update, context: CallbackContext) -> None:
    global room_status
    
    if room_status == update.message.from_user.first_name:
        room_status = None
        await update.message.reply_text("Siz xonadan chiqdingiz.")
    elif room_status is None:
        await update.message.reply_text("Xona allaqachon bo'sh.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o'qiyotgan emassiz!")

def main():
    application = ApplicationBuilder().token("8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k").build()

    # Komandalar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("enter", enter))
    application.add_handler(CommandHandler("exit", exit))

    # Webhook o'rnatish
    application.run_webhook(
        listen="0.0.0.0",
        port=8443,
        url_path="8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k",
        webhook_url=f"https://namoz-xona-bandligi.onrender.com/8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k"
    )

if __name__ == '__main__':
    main()
