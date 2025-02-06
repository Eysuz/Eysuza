import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue

# Xona holati
room_status = {}
reminder_jobs = {}

# Botni boshlash
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Namoz o'qish xonasiga kirish va chiqish uchun quyidagi buyruqlarni ishlating:\n"
        "/enter - Xonaga kirish\n"
        "/exit - Xonadan chiqish\n"
        "/status - Xona holatini ko'rish"
    )

# Xona holatini ko'rsatish
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    if chat_id in room_status and room_status[chat_id]:
        await update.message.reply_text(f"Xona band. Hozirda {room_status[chat_id]} namoz o'qiyapti.")
    else:
        await update.message.reply_text("Xona bo'sh. Hozirda hech kim namoz o'qimayapti.")

# Xonaga kirish
async def enter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global room_status
    
    chat_id = update.message.chat_id
    if chat_id in room_status and room_status[chat_id]:
        await update.message.reply_text(f"Xona band. {room_status[chat_id]} hozir namoz o'qiyapti.")
    else:
        room_status[chat_id] = update.message.from_user.first_name
        await update.message.reply_text(f"Siz xonaga kirdingiz. Hozirda {room_status[chat_id]} namoz o'qiydi.")

        # Har 10 minutda eslatma yuborish
        job_queue = context.job_queue
        job = job_queue.run_repeating(reminder, interval=600, first=600, chat_id=chat_id)
        reminder_jobs[chat_id] = job

# Xonadan chiqish
async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global room_status
    
    chat_id = update.message.chat_id
    if chat_id in room_status and room_status[chat_id] == update.message.from_user.first_name:
        room_status[chat_id] = None
        await update.message.reply_text("Siz xonadan chiqdingiz.")

        # Eslatma ishini to'xtatish
        if chat_id in reminder_jobs:
            reminder_jobs[chat_id].schedule_removal()
            del reminder_jobs[chat_id]
    elif chat_id not in room_status or room_status[chat_id] is None:
        await update.message.reply_text("Xona allaqachon bo'sh.")
    else:
        await update.message.reply_text("Siz bu xonada namoz o'qiyotgan emassiz!")

# Eslatma funksiyasi
async def reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=context.job.chat_id, text="Xonadan chiqdingizmi? Chiqqan bo'lsangiz /exit ni unutmang!")

def main():
    # Tokenni muhit o'zgaruvchisi orqali olish
    token = os.getenv("8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k")
    
    application = Application.builder().token("8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k").build()

    # Komandalar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("enter", enter))
    application.add_handler(CommandHandler("exit", exit))

    # Webhook URL va port
    port = int(os.environ.get('PORT', 8443))
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k",
        webhook_url="https://namoz-xona-bandligi.onrender.com/8009301844:AAG9boXMfRWVZbbN7L6O32M_zq5mWmjBC8k"
    )

if __name__ == '__main__':
    main()
