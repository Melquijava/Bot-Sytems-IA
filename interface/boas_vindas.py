import discord
from discord.ext import commands

# IDs fixos dos canais (substitua pelos valores reais do seu servidor)
CANAL_BEM_VINDO_ID = 1360818765646008432  # ID do canal #entrada
CANAL_SAIDA_ID = 1360834026214129894     # ID do canal #saida

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = self.bot.get_channel(CANAL_BEM_VINDO_ID)
        if canal:
            embed = discord.Embed(
                title=f"👋 Bem-vindo(a), {member.name}!",
                description="Sinta-se em casa no servidor **Systems_BSI**! 🚀\n\nApresente-se e mostre quem é você!",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_image(url="https://i.postimg.cc/6pJx5ZjQ/Bem-vindo-ao-Systems-2.png")  # Substitua pela sua imagem
            embed.set_footer(text="Seu aprendizado começa agora.")

            await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = self.bot.get_channel(CANAL_SAIDA_ID)
        if canal:
            await canal.send(
    f"⚠️ O membro `{member.name}` saiu do servidor.\n"
    f"🆔 ID do usuário: `{member.id}`"
)

async def setup(bot):
    await bot.add_cog(BoasVindas(bot))
    