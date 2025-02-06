from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Xona holati
room_status = None  # Xona bo'sh, agar kimdir kirsa, ularning ismi bo'ladi

# Botni boshlash
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Assalomu alaykum! Namoz o'qish xonasiga kirish va chiqish uchun quyidagi buyruqlarni ishlating:\n"
                                    "/enter - Xonaga kirish\n"
                                    "/exit - Xonadan chiqish\n"
                                    "/status - Xona holatini ko'rish")

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
        room_status = update.message.from_user.first_name  # Namoz o'qiyotgan kishining ismi
        await update.message.reply_text(f"Siz xonaga kirdingiz. Hozirda {room_status} namoz o'qiydi.")

# Xonadan chiqish
async def exit(update: Update, context: CallbackContext) -> None:
    global room_status
    
    if room_status == update.message.from_user.first_name:
        room_status = None  # Xonani bo'shatish
        await update.message.reply_text(f"Siz xonadan chiqdingiz.")
    elif room_status is None:
        await update.message.reply_text("Xona allaqachon bo'sh.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o'qiyotgan emassiz!")

def main():
    # Tokenni BotFather'dan olingan token bilan almashtiring
    application = Application.builder().token("8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k").build()

    # Komandalar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("enter", enter))
    application.add_handler(CommandHandler("exit", exit))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == '__main__':
    main()
