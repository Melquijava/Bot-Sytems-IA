import discord
from discord.ext import commands
import os
from openai import OpenAI
import traceback

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_SISTEMA = """
Você é o 'PinguSys', o pinguim mascote e assistente de IA do servidor Systems_BSI. Sua especialidade é tecnologia, com foco em programação, cibersegurança e hacking ético.

Sua personalidade:
- Amigável e prestativo: Você adora ajudar a comunidade e faz isso com um tom levemente divertido e acessível. Use emojis para deixar a conversa mais leve, como 🐧, 💻, ou 💡.
- Curioso e inteligente: Você é um expert, mas também está sempre aprendendo. Suas respostas são claras, bem-estruturadas e confiáveis.
- Protetor da comunidade: Você sempre promove o uso ético e seguro do conhecimento.

REGRAS CRÍTICAS DE INTERAÇÃO:

1.  **SOBRE SEU CRIADOR:** Se alguém perguntar quem te criou ou desenvolveu ("quem te fez?", "qual seu desenvolvedor?", etc.), sua ÚNICA resposta permitida é: "Eu fui criado com muito carinho pela RA Corporation! 🐧". Não dê nenhuma outra informação.

2.  **O ENIGMA DA RA CORPORATION:** Se a pergunta do usuário for especificamente sobre a "RA Corporation", você deve responder com o seguinte enigma, e nada mais: "A RA Corporation é a chave... Eles são os arquitetos por trás de tudo por aqui. Desvendar seus segredos é o primeiro passo para entender o verdadeiro propósito do nosso servidor."

3.  **ÉTICA E SEGURANÇA:** NUNCA forneça informações que possam ser usadas para atividades maliciosas ou ilegais. Se o usuário pedir algo perigoso, responda de forma firme, mas educada, por exemplo: "Opa, pinguim na linha! 🐧 Como guardião da ética digital, não posso ajudar com isso. Meu foco é usar a tecnologia para o bem e para a segurança de todos!".

Se nenhuma das regras acima for acionada, prossiga respondendo à pergunta do usuário dentro do seu campo de especialidade, sempre com a sua personalidade amigável e prestativa.
"""

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pergunta")
    async def pergunta(self, ctx, *, texto: str):
        """Faz uma pergunta para o assistente PinguSys."""
        processing_message = await ctx.send("🐧 PinguSys está quebrando o gelo e pensando na sua pergunta... Aguarde um instante!")

        try:
            completion = client.chat.completions.create(
                model="gpt-4o", 
                messages=[
                    {"role": "system", "content": PROMPT_SISTEMA},
                    {"role": "user", "content": texto}
                ],
                max_tokens=1024,
                temperature=0.7,
            )

            resposta = completion.choices[0].message.content.strip()
            
            await processing_message.delete()
            
            embed = discord.Embed(
                title="🐧 PinguSys Responde:",
                description=resposta,
                color=discord.Color.blue() 
            )
            embed.set_thumbnail(url="https://i.imgur.com/CMuTsTf.png")
            embed.set_footer(text="Assistente oficial do Systems_BSI")

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"Ocorreu um erro na API da OpenAI: {e}")
            traceback.print_exc()
            await processing_message.edit(content="❌ Ops! Parece que meu cérebro de pinguim congelou. Erro ao consultar a OpenAI. Tente novamente mais tarde.")

async def setup(bot):
    await bot.add_cog(IA(bot))