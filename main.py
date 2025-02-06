from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, JobQueue
from datetime import datetime, timedelta

# Xona holati va foydalanuvchilar ro'yxati
room_status = None
user_jobs = {}

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
        
        # 10 minutdan keyin foydalanuvchini eslatish
        job = context.job_queue.run_once(send_exit_reminder, timedelta(minutes=1), context=update.message.from_user.id)
        user_jobs[update.message.from_user.id] = job

# Xonadan chiqish
async def exit(update: Update, context: CallbackContext) -> None:
    global room_status
    
    if room_status == update.message.from_user.first_name:
        room_status = None
        # Agar foydalanuvchi xonadan chiqsa, eslatmani bekor qilish
        if update.message.from_user.id in user_jobs:
            user_jobs[update.message.from_user.id].schedule_removal()
            del user_jobs[update.message.from_user.id]
        await update.message.reply_text("Siz xonadan chiqdingiz.")
    elif room_status is None:
        await update.message.reply_text("Xona allaqachon bo'sh.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o'qiyotgan emassiz!")

# Foydalanuvchiga eslatma yuborish (10 minutdan so'ng)
async def send_exit_reminder(context: CallbackContext) -> None:
    user_id = context.job.context
    await context.bot.send_message(user_id, "Xonadan chiqdingizmi? /exit ni unutmang!")

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
