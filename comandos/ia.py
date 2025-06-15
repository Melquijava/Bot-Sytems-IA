import discord
from discord.ext import commands
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pergunta")
    async def pergunta(self, ctx, *, texto):
        await ctx.send("⏳ O Systems IA está processando sua pergunta, aguarde...", delete_after=10)

        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um profissional educado e direto, seu maior foco é responder perguntas sobre programação e hacker ético."},
                    {"role": "user", "content": texto}
                ],
                max_tokens=500,
                temperature=0.7
            )

            resposta = completion.choices[0].message.content.strip()
            await ctx.send(f"🤖 **System_BSI IA:**\n{resposta}", delete_after=120)

        except Exception as e:
            await ctx.send("❌ Erro ao consultar a OpenAI. Verifique o token ou limite da API.", delete_after=10)
            import traceback
            traceback.print_exc()

async def setup(bot):
    await bot.add_cog(IA(bot))
    