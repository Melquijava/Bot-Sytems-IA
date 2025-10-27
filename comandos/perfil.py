import discord
from discord.ext import commands
import json
import os

VOLUME_PATH = "/app/data"
PERFIS_FILE_PATH = os.path.join(VOLUME_PATH, "perfis.json")

def carregar_perfis():
    os.makedirs(VOLUME_PATH, exist_ok=True)
    try:
        with open(PERFIS_FILE_PATH, 'r') as f:
            return {int(k): v for k, v in json.load(f).items()}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_perfis(perfis_data):
    with open(PERFIS_FILE_PATH, 'w') as f:
        json.dump(perfis_data, f, indent=4)

class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.perfis = carregar_perfis()

    @commands.command(name="github")
    async def github(self, ctx, link:str=None):
        if not link:
            await ctx.send(f"🔗 Envie o link do seu GitHub assim: `!github https://github.com/seuuser`", delete_after=30)
            return

        self.perfis.setdefault(ctx.author.id, {})["github"] = link
        salvar_perfis(self.perfis)
        await ctx.send("✅ GitHub salvo com sucesso!", delete_after=10)

    @commands.command(name="linkedin")
    async def linkedin(self, ctx, link:str=None):
        if not link:
            await ctx.send(f"🔗 Envie o link do seu LinkedIn assim: `!linkedin https://linkedin.com/in/seuuser`", delete_after=30)
            return

        self.perfis.setdefault(ctx.author.id, {})["linkedin"] = link
        salvar_perfis(self.perfis) 
        await ctx.send("✅ LinkedIn salvo com sucesso!", delete_after=10)

    @commands.command(name="perfil")
    async def perfil(self, ctx):
        self.perfis = carregar_perfis()
        dados = self.perfis.get(ctx.author.id, {})
        
        embed = discord.Embed(title=f"Perfil de {ctx.author.display_name}", color=discord.Color.green())
        embed.add_field(name="GitHub", value=dados.get("github", "Não cadastrado"), inline=False)
        embed.add_field(name="LinkedIn", value=dados.get("linkedin", "Não cadastrado"), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Perfil(bot))