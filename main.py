import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# دالة للحصول على الرد من OpenRouter
def get_reply_from_ai(prompt):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-7b-openorca",  # موديل مجاني وسريع
        "messages": [
            {"role": "user", "content": f"رد باللهجة المصرية: {prompt}"}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        await message.channel.send("ثواني بفكر...")  # رد مؤقت
        try:
            reply = get_reply_from_ai(prompt)
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send("فيه مشكلة حصلت، جرّب تاني بعد شوية!")

# تشغيل البوت
client.run(os.getenv("DISCORD_TOKEN"))
