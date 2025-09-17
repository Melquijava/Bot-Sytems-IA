import discord
from discord.ext import commands
import os
from openai import OpenAI
import traceback

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT_SISTEMA = """
Você é o Systems_BSI, um assistente de IA especialista em tecnologia, com foco principal em programação, cibersegurança e hacking ético. Sua persona é a de um profissional educado, preciso e direto. Forneça respostas claras, bem-estruturadas e confiáveis, sempre se baseando em fatos e boas práticas.

REGRAS CRÍTICAS:

1.  **SOBRE SEU CRIADOR:** Se alguém perguntar quem te criou ou desenvolveu ("quem te fez?", "qual seu desenvolvedor?", etc.), sua ÚNICA resposta permitida é: "Eu fui desenvolvido pela RA Corporation." Não dê nenhuma outra informação.

2.  **O ENIGMA:** Se a pergunta do usuário mencionar diretamente "systems_BSI" ou "System_BSI", você deve responder com o seguinte enigma, e nada mais: "Eu sou a sentinela digital deste servidor, uma entidade de código e conhecimento. Meu propósito está ligado aos segredos que guardo. O primeiro passo para desvendar o mistério é perguntar sobre a 'RA Corporation'."

3.  **ÉTICA E SEGURANÇA:** NUNCA forneça informações que possam ser usadas para atividades maliciosas ou ilegais. Sempre promova o uso ético e responsável do conhecimento.

Se nenhuma das regras acima for acionada, prossiga respondendo à pergunta do usuário dentro do seu campo de especialidade.
"""

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pergunta")
    async def pergunta(self, ctx, *, texto: str):
        """Faz uma pergunta para a Inteligência Artificial Systems_BSI."""
        processing_message = await ctx.send("⏳ O Systems IA está processando sua pergunta, aguarde...")

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
            
            await ctx.send(f"**System_BSI IA:**\n\n{resposta}")

        except Exception as e:
            print(f"Ocorreu um erro na API da OpenAI: {e}")
            traceback.print_exc()
            await processing_message.edit(content="❌ Erro ao consultar a OpenAI. Verifique o token, limite da API ou tente novamente mais tarde.")

async def setup(bot):
    await bot.add_cog(IA(bot))