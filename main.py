from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue
import asyncio

# Xona holati
room_status = None  # Xona bo'sh, agar kimdir kirsa, ularning ismi bo'ladi
users_in_room = set()  # Xonada hozirda bo'lgan foydalanuvchilarni saqlash

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
    global room_status, users_in_room
    
    if room_status:
        await update.message.reply_text(f"Xona band. {room_status} hozir namoz o'qiyapti.")
    else:
        room_status = update.message.from_user.first_name  # Namoz o'qiyotgan kishining ismi
        users_in_room.add(update.message.from_user.id)  # Xonaga kirgan foydalanuvchini saqlash
        await update.message.reply_text(f"Siz xonaga kirdingiz. Hozirda {room_status} namoz o'qiydi.")
        # Har 10 daqiqada foydalanuvchiga xabar yuborish
        context.job_queue.run_once(remind_exit, 60, context=update.message.from_user.id)

# Xonadan chiqish
async def exit(update: Update, context: CallbackContext) -> None:
    global room_status, users_in_room
    
    if room_status == update.message.from_user.first_name:
        room_status = None  # Xonani bo'shatish
        users_in_room.remove(update.message.from_user.id)  # Foydalanuvchini xonadan olib tashlash
        await update.message.reply_text(f"Siz xonadan chiqdingiz.")
    elif room_status is None:
        await update.message.reply_text("Xona allaqachon bo'sh.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o'qiyotgan emassiz!")

# Har 10 daqiqada foydalanuvchiga eslatma yuborish
async def remind_exit(context: CallbackContext) -> None:
    user_id = context.job.context
    user = await context.bot.get_chat(user_id)
    await user.send_message("Xonadan chiqdingizmi? Chiqqan bo'lsangiz, /exit ni unutmang!")

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
