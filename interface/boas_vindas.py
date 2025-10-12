import discord
from discord.ext import commands
from datetime import datetime, timezone
import os
from openai import AsyncOpenAI

CANAL_BEM_VINDO_ID = 1360818765646008432 
CANAL_SAIDA_ID = 1360834026214129894 

URL_IMAGEM_PINGUSYS = "https://i.imgur.com/CMuTsTf.png" 

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class BoasVindas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def gerar_mensagem_boas_vindas(self, nome_membro):
        """Gera mensagem personalizada com IA."""
        prompt = f"""
        Você é o PinguSys, o mascote pinguim tech do servidor 'Systems_BSI'.
        Um novo membro chamado '{nome_membro}' acabou de entrar.
        Gere uma mensagem de boas-vindas curta, muito animada, acolhedora e usando emojis (🐧, 💻, 🚀).
        Convide-o para se apresentar a comunidade. Mantenha um tom divertido.
        Não use aspas na resposta.
        """
        try:
            completion = await aclient.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=150,
                temperature=0.8,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro ao gerar boas-vindas com IA: {e}")
            return f"Olá {nome_membro}! O PinguSys está compilando... mas seja muito bem-vindo ao Systems_BSI! 🐧 Apresente-se para a galera!"

    @commands.Cog.listener()
    async def on_member_join(self, member):
        canal = self.bot.get_channel(CANAL_BEM_VINDO_ID)
        if canal:
            descricao_ia = await self.gerar_mensagem_boas_vindas(member.name)

            embed = discord.Embed(
                title=f"🐧 PinguSys dá as boas-vindas a {member.name}!",
                description=descricao_ia,
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_image(url="https://i.postimg.cc/6pJx5ZjQ/Bem-vindo-ao-Systems-2.png")
            
            embed.set_footer(text="Systems_BSI • Comunidade Tech", icon_url=URL_IMAGEM_PINGUSYS)
            
            await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        canal = self.bot.get_channel(CANAL_SAIDA_ID)
        data_entrada = member.joined_at
        data_saida = datetime.now(timezone.utc)

        if data_entrada:
            tempo_total = data_saida - data_entrada
            dias_totais = tempo_total.days
            meses = dias_totais // 30
            dias = dias_totais % 30
            permanencia = f"{meses} mês(es) e {dias} dia(s)"
        else:
            permanencia = "Não disponível"

        nome_username = member.global_name if member.global_name else member.name

        embed = discord.Embed(
            title="⚠️ Membro saiu do servidor",
            color=discord.Color.red(),
            timestamp=data_saida
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="👤 Nome de exibição", value=member.name, inline=True)
        embed.add_field(name="🔒 Nome username", value=nome_username, inline=True)
        embed.add_field(name="🆔 ID do usuário", value=f"`{member.id}`", inline=False)
        embed.add_field(name="⏱️ Tempo no servidor", value=permanencia, inline=False)
        embed.set_footer(text="Monitoramento automático • Systems_BSI")

        if canal:
            await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BoasVindas(bot))