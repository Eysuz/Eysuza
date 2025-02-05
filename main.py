import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime

# Xona holati
room_status = None  # Xona bo'sh, agar kimdir kirsa, ularning ismi bo'ladi
room_occupants = {}  # Foydalanuvchi ID va ularning kirish vaqti

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
        await update.message.reply_text(f"Xona band. Hozirda {room_status} namoz o‘qiyapti.")
    else:
        await update.message.reply_text("Xona bo‘sh. Hozirda hech kim namoz o‘qimayapti.")

# Xonaga kirish
async def enter(update: Update, context: CallbackContext) -> None:
    global room_status, room_occupants

    if room_status:
        await update.message.reply_text(f"Xona band. {room_status} hozir namoz o‘qiyapti.")
    else:
        user_id = update.message.from_user.id
        user_name = update.message.from_user.first_name
        
        room_status = user_name  # Xonadagi shaxs ismi
        room_occupants[user_id] = datetime.now()  # Kirish vaqti

        await update.message.reply_text(f"Siz xonaga kirdingiz. Hozirda {user_name} namoz o‘qiydi.")
        
        # 10 daqiqadan keyin eslatma berish uchun job qo‘shish
        context.job_queue.run_once(check_exit, when=600, chat_id=update.message.chat_id, name=str(user_id))

# Xonadan chiqish
async def exit(update: Update, context: CallbackContext) -> None:
    global room_status, room_occupants

    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if room_status == user_name:
        room_status = None  # Xonani bo‘shatish
        room_occupants.pop(user_id, None)  # Foydalanuvchini o‘chirish

        # Agar eslatma uchun job mavjud bo‘lsa, uni o‘chirish
        current_jobs = context.job_queue.jobs()
        for job in current_jobs:
            if job.name == str(user_id):
                job.schedule_removal()

        await update.message.reply_text("Siz xonadan chiqdingiz.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o‘qiyotgan emassiz!")

# Xonadan chiqish haqida eslatma
async def check_exit(context: CallbackContext) -> None:
    job = context.job
    user_id = job.chat_id
    await context.bot.send_message(user_id, "Xonadan chiqdingizmi? Agar chiqqan bo‘lsangiz, /exit ni unutmang.")

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
