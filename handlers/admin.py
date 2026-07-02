from aiogram import Router, F, Bot
from aiogram.types import Message
from config import settings
from handlers.customer import USER_DATA
from services.openai_service import OpenAIService

admin_router = Router()
ai_service = OpenAIService()

def is_admin(message: Message) -> bool:
    return message.from_user.id == settings.ADMIN_ID

@admin_router.message(F.text, is_admin)
async def handle_admin_reply(message: Message, bot: Bot):
    text = message.text.strip()

    # Change mode command. Format: /setmode 12345678 manual
    if text.startswith("/setmode"):
        try:
            _, tgt_id, target_mode = text.split()
            tgt_id = int(tgt_id)
            if tgt_id in USER_DATA:
                USER_DATA[tgt_id]["mode"] = target_mode.lower()
                await message.reply(f"✅ Customer {tgt_id} set to mode: {target_mode}")
            else:
                await message.reply("❌ User has not clicked /start yet.")
            return
        except ValueError:
            await message.reply("❌ Use: `/setmode [User_ID] [auto/manual/ai]`")
            return

    # Relay mechanism. Format: 12345678 -> Hello
    if "->" in text:
        try:
            target_id_str, admin_payload = text.split("->", 1)
            target_user_id = int(target_id_str.strip())
            
            await bot.send_message(chat_id=target_user_id, text=admin_payload.strip())
            await message.reply("📬 Message sent to user.")
            return
        except Exception as e:
            await message.reply(f"❌ Failed to send: {str(e)}")
            return

@admin_router.message(F.text)
async def route_customer_messages(message: Message, bot: Bot):
    user_id = message.from_user.id
    
    # Quick register if they skipped /start
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {
            "username": message.from_user.username,
            "full_name": message.from_user.full_name,
            "mode": "ai",
            "history": []
        }

    customer = USER_DATA[user_id]
    customer["history"].append({"role": "user", "content": message.text})

    if customer["mode"] == "manual":
        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"📥 **[MANUAL INTERCEPT]** from `{user_id}`\n"
                 f"User: @{customer['username'] or 'No Username'}\n"
                 f"Message: {message.text}\n\n"
                 f"💡 Reply with: `{user_id} -> Your response`"
        )
        
    elif customer["mode"] == "ai":
        # Pull last 6 exchanges from memory history
        recent_history = customer["history"][-6:]
        ai_reply = await ai_service.generate_response(message.text, recent_history)
        
        customer["history"].append({"role": "assistant", "content": ai_reply})
        await message.answer(ai_reply)

    elif customer["mode"] == "auto":
        faq_reply = "Thank you for reaching out! Our team has been notified, and our admin @Expertlovet will review your request shortly."
        await message.answer(faq_reply)
        await bot.send_message(
            chat_id=settings.ADMIN_ID,
            text=f"🔔 **[AUTO NOTIFICATION]** Inquiry from @{customer['username'] or user_id}:\n\"{message.text}\""
        )
