from discord.ext import commands
import discord

perfis = {} 

class Perfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="github")
    async def github(self, ctx, link=None):
        if not link:
            await ctx.send("📎 Envie o link do seu GitHub assim: `!github https://github.com/seuuser`",
                           delete_after=30)
            return
        perfis.setdefault(ctx.author.id, {})["github"] = link
        await ctx.send("✅ GitHub salvo com sucesso!",
                       delete_after=10)

    @commands.command(name="linkedin")
    async def linkedin(self, ctx, link=None):
        if not link:
            await ctx.send("📎 Envie o link do seu LinkedIn assim: `!linkedin https://linkedin.com/in/seuuser`",
                           delete_after=30)
            return
        perfis.setdefault(ctx.author.id, {})["linkedin"] = link
        await ctx.send("✅ LinkedIn salvo com sucesso!",
                       delete_after=10)

    @commands.command(name="perfil")
    async def perfil(self, ctx):
        dados = perfis.get(ctx.author.id, {})
        embed = discord.Embed(title=f"📇 Perfil de {ctx.author.display_name}", color=discord.Color.green())
        embed.add_field(name="GitHub", value=dados.get("github", "Não cadastrado"), inline=False)
        embed.add_field(name="LinkedIn", value=dados.get("linkedin", "Não cadastrado"), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Perfil(bot))
