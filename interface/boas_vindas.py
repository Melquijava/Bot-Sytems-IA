import discord
from discord.ext import commands
from datetime import datetime

# IDs dos canais
CANAL_BEM_VINDO_ID = 1360818765646008432  # Canal de entrada
CANAL_SAIDA_ID = 1360834026214129894      # Canal de saída

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = self.bot.get_channel(CANAL_BEM_VINDO_ID)
        if canal:
            embed = discord.Embed(
                title=f"👋 Bem-vindo(a), {member.name}!",
                description="Sinta-se em casa no servidor **Systems_BSI**! 🚀\n\nApresente-se e mostre quem você é!",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_image(url="https://i.postimg.cc/6pJx5ZjQ/Bem-vindo-ao-Systems-2.png")
            embed.set_footer(text="Seu aprendizado começa agora.")
            await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = self.bot.get_channel(CANAL_SAIDA_ID)
        data_entrada = member.joined_at
        data_saida = datetime.utcnow()

        if data_entrada:
            tempo_total = data_saida - data_entrada
            dias_totais = tempo_total.days
            meses = dias_totais // 30
            dias = dias_totais % 30
            permanencia = f"{meses} mês(es) e {dias} dia(s)"
        else:
            permanencia = "Não disponível"

        embed = discord.Embed(
            title="⚠️ Membro saiu do servidor",
            color=discord.Color.red(),
            timestamp=data_saida
        )

        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="👤 Nome de exibição", value=member.name, inline=True)
        embed.add_field(name="🔒 Nome username", value=member.global_name or member.name, inline=True)
        embed.add_field(name="🆔 ID do usuário", value=f"`{member.id}`", inline=False)
        embed.add_field(name="⏱️ Tempo no servidor", value=permanencia, inline=False)
        embed.set_footer(text="Monitoramento automático • Systems_BSI")

        if canal:
            await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BoasVindas(bot))
