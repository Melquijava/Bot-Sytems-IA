from discord.ext import commands
import discord

class ComandosExtras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="programacao")
    async def programacao(self, ctx):
        await ctx.send(
            "💻 **Canais sobre Programação:**\n"
            "🔹 <#1366547081459929120> – Cursos gratuitos\n"
            "🔹 <#1367647336062390292> – Dicas e recursos de dev\n"
            "🔹 <#1360844187637121065> – Compartilhe seus projetos\n",
            delete_after=120
        )

    @commands.command(name="hacking")
    async def hacking(self, ctx):
        await ctx.send(
            "🧠 **Canais sobre Hacking Ético:**\n"
            "🔹 <#1367945980342833234> – Técnicas, ferramentas e desafios\n"
            "🔹 <#1368067478248361988> – Cursos sobre hacking ético\n"
            "🔹 <#1372577665764298822> – Laboratórios e simulações\n",
            delete_after=120
        )

    @commands.command(name="prompts-ia")
    async def prompts_ia(self, ctx):
        await ctx.send(
            "🤖 **Canais sobre IA e Prompts:**\n"
            "🔹 <#1368094028372901999> – Compartilhamento de prompts úteis\n"
            "🔹 <#1383248301683376169> – Cursos de IA e ferramentas\n"
            "🔹 <#1368078619708100668> – Exemplos e bots de IA\n",
            delete_after=120
        )

async def setup(bot):
    await bot.add_cog(ComandosExtras(bot))