import discord
import openai
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"رد على السؤال باللهجة المصرية: {prompt}"}
            ]
        )

        reply = response["choices"][0]["message"]["content"]
        await message.channel.send(reply)

client.run(os.getenv("DISCORD_TOKEN"))
