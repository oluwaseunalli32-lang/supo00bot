from openai import AsyncOpenAI
from config import settings

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY.get_secret_value())
        self.system_prompt = (
            "You are the Professional Sales and Customer Support Assistant for 'Expert L💰💰', "
            "operating out of Nigeria. Owner: Expert L (@Expertlovet). Business Hours: 24/7.\n\n"
            "SERVICES OFFERED:\n"
            "1. Telegram Advertising: Channel/group promotion, targeted campaigns, sponsored posts, audience growth.\n"
            "2. Telegram Bot Development: Custom support bots, AI bots, automation, payment/subscription setups, API integrations.\n\n"
            "STEPS:\n"
            "- Greet professionally and politely.\n"
            "- Ask which service they want.\n"
            "- If Advertising: Explain features, ask for goals.\n"
            "- If Bot Dev: Ask for specs/features.\n"
            "- Keep a friendly, helpful tone. Encourage connection. Escalate complex or custom pricing requests to Admin."
        )

    async def generate_response(self, text_content: str, history: list) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]
        for msg in history:
            messages.append({"role": msg['role'], "content": msg['content']})
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
