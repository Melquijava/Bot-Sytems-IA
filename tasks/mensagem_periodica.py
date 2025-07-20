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
                "👋 **Seja bem-vindo(a) ao Systems_BSI!**\n\n"
                "📌 Se você chegou agora, não deixe de se apresentar no canal <#1360818765646008436>!\n"
                "🔗 Compartilhe seu GitHub e LinkedIn no canal <#1360826916268937412> para fazer networking com a comunidade!\n"
                "🤖 Use o canal <#1383291276803440711> para explorar os comandos do nosso bot e aproveitar todos os recursos disponíveis.\n\n"
                "🚀 Estamos felizes em ter você aqui. Bora evoluir junto!"
            )
            await canal.send(mensagem)

async def setup(bot):
    await bot.add_cog(Mensagem(bot))