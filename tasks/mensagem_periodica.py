from discord.ext import tasks, commands

class Mensagem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enviar_mensagem.start()

    @tasks.loop(hours=12)
    async def enviar_mensagem(self):
        canal_id = 1360845409454526564  
        canal = self.bot.get_channel(canal_id)

        if canal:
            mensagem = (
                "# **Fique por dentro das novidades do Systems_BSI!**\n\n"
                "📲 Siga a gente no **Instagram** e acompanhe os conteúdos exclusivos: \n"
                "[Instagram Oficial](https://instagram.com/systems_bsi)\n\n"
                "💻 Acesse nosso **site** para conferir projetos, eventos e materiais:\n"
                "[Nosso Site](https://systemsbsi.com)\n\n"
                "Junte-se à nossa comunidade em todas as redes e cresça junto com a gente!"
            )
            await canal.send(mensagem)

async def setup(bot):
    await bot.add_cog(Mensagem(bot))
