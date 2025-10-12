import discord
from discord.ext import commands
from discord import ui 
from datetime import datetime, timezone


CANAL_INSCRICOES_ID = 1427010033622847664
CANAL_LOG_INSCRICOES_ID = 1427010916259598407
CARGO_INSCRITO_ID = 1427011343659307068


DEADLINE_INSCRICOES = datetime(2025, 10, 19, 23, 59, 59, tzinfo=timezone.utc)

class FormularioInscricao(ui.Modal, title="Inscrição para o Desafio Systems BSI"):

    nome = ui.TextInput(label="Nome Completo", placeholder="Seu nome como aparecerá no certificado", required=True, style=discord.TextStyle.short)
    
    email = ui.TextInput(label="E-mail", placeholder="Seu melhor e-mail para contato", required=True, style=discord.TextStyle.short)
    
    telefone = ui.TextInput(label="Telefone (com DDD)", placeholder="(Opcional) Para grupos de comunicação rápida", required=False, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        cargo = interaction.guild.get_role(CARGO_INSCRITO_ID)
        if not cargo:
            await interaction.response.send_message("❌ Erro de configuração: O cargo de inscrito não foi encontrado. Contate um admin.", ephemeral=True)
            return
        
        canal_log = interaction.guild.get_channel(CANAL_LOG_INSCRICOES_ID)
        if not canal_log:
            await interaction.response.send_message("❌ Erro de configuração: O canal de logs não foi encontrado. Contate um admin.", ephemeral=True)
            return

        if cargo in interaction.user.roles:
            await interaction.response.send_message("✅ Você já está inscrito no evento!", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(cargo)

            log_embed = discord.Embed(
                title="📝 Nova Inscrição Recebida!",
                color=discord.Color.green(),
                timestamp=datetime.now(timezone.utc)
            )
            log_embed.set_thumbnail(url=interaction.user.display_avatar.url)
            log_embed.add_field(name="👤 Discord", value=f"{interaction.user.mention} (`{interaction.user.id}`)", inline=False)
            log_embed.add_field(name="✍️ Nome Completo", value=self.nome.value, inline=False)
            log_embed.add_field(name="📧 E-mail", value=self.email.value, inline=False)
            
            if self.telefone.value:
                log_embed.add_field(name="📞 Telefone", value=self.telefone.value, inline=False)

            await canal_log.send(embed=log_embed)

            await interaction.response.send_message(f"🎉 Inscrição confirmada com sucesso, {self.nome.value}! Você recebeu o cargo de '{cargo.name}'. Boa sorte!", ephemeral=True)

        except Exception as e:
            print(f"Erro ao processar inscrição: {e}")
            await interaction.response.send_message("❌ Ocorreu um erro ao processar sua inscrição. Tente novamente ou contate um admin.", ephemeral=True)


class VistaInscricao(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Inscrever-se no Desafio!", style=discord.ButtonStyle.success, custom_id="botao_inscricao_desafio", emoji="🚀")
    async def botao_inscrever(self, interaction: discord.Interaction, button: ui.Button):
        if datetime.now(timezone.utc) > DEADLINE_INSCRICOES:
            button.disabled = True
            await interaction.response.send_message("⏳ As inscrições para o desafio foram encerradas. Fique de olho para os próximos eventos!", ephemeral=True)
            await interaction.message.edit(view=self)
            return
        
        await interaction.response.send_modal(FormularioInscricao())

class EventosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(VistaInscricao())

    @commands.command(name="iniciar_inscricoes")
    async def iniciar_inscricoes(self, ctx):
        """Cria a mensagem de inscrição para o evento de desafios."""
        canal_destino = self.bot.get_channel(CANAL_INSCRICOES_ID)
        if not canal_destino:
            await ctx.send("❌ Erro: Canal de inscrições não encontrado. Verifique o ID no código.")
            return

        embed = discord.Embed(
            title="🏆 Desafio Semanal Systems BSI - Inscrições Abertas! 🏆",
            description=(
                "Prepare-se para uma semana intensa de desafios de programação e cibersegurança! Mostre suas habilidades, ganhe pontos e concorra a prêmios incríveis.\n\n"
                "**Clique no botão abaixo para garantir sua vaga!**"
            ),
            color=0x00aaff
        )
        embed.add_field(name="🗓️ Cronograma do Evento", value=(
            "**Inscrições:** Até 19 de Outubro\n"
            "**Desafios:** 20 a 24 de Outubro\n"
            "**Desafio Final (Opcional):** 25 de Outubro\n"
            "**Resultados:** 26 de Outubro"
        ), inline=False)
        embed.add_field(name="🎁 Premiação", value=(
            "🥇 **1º, 2º e 3º Lugar:** Prêmios especiais + Cargo Exclusivo + Certificado\n"
            "🏅 **Top 10:** Cargo Exclusivo + Certificado de Participação"
        ), inline=False)
        embed.set_footer(text="Não perca essa chance de evoluir e ser reconhecido!")
        embed.set_image(url="https://i.imgur.com/IunHuBk.jpeg") 

        await canal_destino.send(embed=embed, view=VistaInscricao())
        await ctx.send(f"✅ Mensagem de inscrição enviada com sucesso para o canal {canal_destino.mention}!")


async def setup(bot):
    await bot.add_cog(EventosCog(bot))