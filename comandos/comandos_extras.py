from discord.ext import commands
import discord

class ComandosExtras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="programacao")
    async def programacao(self, ctx):
        await ctx.send(
            "💻 **Canais sobre Programação:**\n"
            "🔹 <#1409539828537753651> – Cursos gratuitos\n"
            "🔹 <#1372577665764298822> – Dicas e recursos de dev\n"
            "🔹 <#1360844187637121065> – Compartilhe seus projetos\n",
            delete_after=120
        )

    @commands.command(name="cyber-security")
    async def hacking(self, ctx):
        await ctx.send(
            "🧠 **Canais sobre Ciber segurança:**\n"
            "🔹 <#1396295340738482307> – Chat específico para o assunto\n"
            "🔹 <#1409811288300982272> – Cursos sobre Cyber-security\n"
            "🔹 <#1367945980342833234> – Laboratórios e simulações\n",
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