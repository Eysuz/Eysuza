import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime, timedelta

# Xona holati
room_status = None  # Xona bo'sh, agar kimdir kirsa, ularning ismi bo'ladi
room_occupants = {}  # Foydalanuvchi ismlari va kirish vaqti

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
    global room_status, room_occupants
    
    if room_status:
        await update.message.reply_text(f"Xona band. {room_status} hozir namoz o'qiyapti.")
    else:
        room_status = update.message.from_user.first_name  # Namoz o'qiyotgan kishining ismi
        room_occupants[update.message.from_user.id] = datetime.now()  # Kirish vaqti
        await update.message.reply_text(f"Siz xonaga kirdingiz. Hozirda {room_status} namoz o'qiydi.")
        
        # 10 daqiqada bir foydalanuvchiga chiqish haqida eslatma yuborish
        context.job_queue.run_repeating(check_exit, interval=600, first=600, context=update.message.from_user.id)

# Xonadan chiqish
async def exit(update: Update, context: CallbackContext) -> None:
    global room_status, room_occupants
    
    if room_status == update.message.from_user.first_name:
        room_status = None  # Xonani bo'shatish
        room_occupants.pop(update.message.from_user.id, None)  # Foydalanuvchini olib tashlash
        await update.message.reply_text(f"Siz xonadan chiqdingiz.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o'qiyotgan emassiz!")

# Xonadan chiqish haqida eslatma
async def check_exit(context: CallbackContext) -> None:
    user_id = context.job.context
    
    # Foydalanuvchi mavjudligini tekshirish
    if user_id in room_occupants:
        # Foydalanuvchi nomini olish
        user_name = await context.bot.get_chat(user_id).first_name
        # Eslatma yuborish
        await context.bot.send_message(user_id, f"{user_name}, Xonadan chiqdingizmi? Agar chiqqan bo'lsangiz, /exit ni unutmang.")

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
