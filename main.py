import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = [
    "comandos.gerais",
    "comandos.perfil",
    "comandos.educacionais",
    "tasks.mensagem_periodica",
    "tasks.noticias_hacker",
    "interface.painel",
    "interface.boas_vindas",
    "interface.voice_logger",
    "comandos.comandos_extras",
    "comandos.editor",
    "comandos.ia",
    "comandos.eventos",
]

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Comandos de barra sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"❌ Erro ao sincronizar comandos de barra: {e}")

async def main():
    async with bot:
        for ext in EXTENSIONS:
            try:
                await bot.load_extension(ext)
                print(f"✅ Extensão carregada: {ext}")
            except Exception as e:
                print(f"❌ Erro ao carregar {ext}: {e}")
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
