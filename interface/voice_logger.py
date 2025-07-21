import os
import discord
from discord.ext import commands
import datetime

voice_states = {}

class VoiceLogger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.log_channel_id = int(os.getenv('LOG_CHANNEL_ID'))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        log_channel = self.bot.get_channel(self.log_channel_id)
        if not log_channel:
            print(f"ERRO: Canal de log com ID {self.log_channel_id} não encontrado.")
            return

        if before.channel is None and after.channel is not None:
            voice_states[member.id] = datetime.datetime.now(datetime.timezone.utc)

            embed_entrada = discord.Embed(
                description=f'✅ **{member.display_name}** entrou no canal de voz **{after.channel.name}**.',
                color=discord.Color.green()
            )
            await log_channel.send(embed=embed_entrada)

        elif before.channel is not None and after.channel is None:
            if member.id in voice_states:
                entrada_dt = voice_states.pop(member.id)
                saida_dt = datetime.datetime.now(datetime.timezone.utc)
                duracao = saida_dt - entrada_dt

                fuso_horario_br = datetime.timezone(datetime.timedelta(hours=-3))
                horario_entrada_str = entrada_dt.astimezone(fuso_horario_br).strftime('%H:%M:%S')
                horario_saida_str = saida_dt.astimezone(fuso_horario_br).strftime('%H:%M:%S')

                total_seconds = int(duracao.total_seconds())
                horas, remainder = divmod(total_seconds, 3600)
                minutos, segundos = divmod(remainder, 60)

                descricao_saida = (
                    f"| 🧑 **Nome**: {member.display_name}\n"
                    f"| 🎧 **Canal**: {before.channel.name}\n"
                    f"| 🕒 **Entrada**: {horario_entrada_str}\n"
                    f"| 🕒 **Saída**: {horario_saida_str}\n"
                    f"| ⌛ **Tempo total**: {horas}h {minutos}min {segundos}s"
                )

                embed_saida = discord.Embed(
                    title="🔴 Registro de Saída de Voz",
                    description=descricao_saida,
                    color=discord.Color.red(),
                    timestamp=datetime.datetime.now()
                )
                embed_saida.set_thumbnail(url=member.display_avatar.url)
                embed_saida.set_footer(text=f"ID do Usuário: {member.id}")

                await log_channel.send(embed=embed_saida)
            else:
                embed_simples = discord.Embed(
                    description=f'❌ **{member.display_name}** saiu do canal **{before.channel.name}** (tempo não rastreado).',
                    color=discord.Color.orange()
                )
                await log_channel.send(embed=embed_simples)

# Setup padrão de COG
async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceLogger(bot))
