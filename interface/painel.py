import discord
from discord.ext import commands

class PainelSistemaBSI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="painel")
    async def painel(self, ctx):
        embed = discord.Embed(
            title="🌐 Painel Interativo • Systems_BSI",
            description=(
                "Bem-vindo ao nosso servidor!\n"
                "Explore recursos, conecte-se com a comunidade e evolua com a gente.\n\n"
                "Clique nos botões abaixo para navegar ou executar comandos instantaneamente."
            ),
            color=discord.Color.blurple()
        )
        embed.set_image(url="https://i.imgur.com/7edJCEr.jpeg")
        embed.set_footer(text="Desenvolvido por Systems_BSI • discord.gg/systems")

        view = PainelInterativoView()
        await ctx.send(embed=embed, view=view)

class PainelInterativoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📚 Ver Comandos", style=discord.ButtonStyle.primary, custom_id="ver_comandos")
    async def ver_comandos(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "**📘 Comandos disponíveis:**\n"
            "🔹 `!aula` – Aula gratuita de TI\n"
            "🔹 `!quiz` – Quiz interativo\n"
            "🔹 `!pergunta <texto>` – IA responde sua dúvida\n"
            "🔹 `!dica` – Dica aleatória de tecnologia\n"
            "🔹 `!desafio` – Desafio técnico diário\n"
            "🔹 `!perfil` – Ver seus links GitHub/LinkedIn\n"
            "🔹 `!setgithub` / `!setlinkedin` – Cadastrar seus links\n"
            "🔹 `!programacao` – Recomenda canais de programação\n"
            "🔹 `!hacking` – Recomenda canais de hacking ético\n"
            "🔹 `!prompts-ia` – Recomenda canais de IA e prompts",
            ephemeral=True
        )
        
    @discord.ui.button(label="📞 Suporte", style=discord.ButtonStyle.danger, custom_id="suporte")
    async def suporte(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        admin_role_ids = [
            1360819794882072697, 
            1366601103063384134,  
            1367617789468348627   
        ]

        categoria = discord.utils.get(guild.categories, name="━━━━━━❰･ᴀᴛᴇɴᴅɪᴍᴇɴᴛᴏ･❱━━━━━")
        if not categoria:
            await interaction.response.send_message("❌ Categoria 'Atendimento' não encontrada.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        }

        for role_id in admin_role_ids:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        existing = discord.utils.get(guild.text_channels, name=f"suporte-{user.name.lower()}")
        if existing:
            await interaction.response.send_message(
                f"❗ Você já possui um canal de suporte aberto: {existing.mention}",
                ephemeral=True
            )
            return

        canal = await guild.create_text_channel(
            name=f"suporte-{user.name}",
            overwrites=overwrites,
            reason="Canal de suporte automático",
            category=categoria
        )

        await interaction.response.send_message(f"✅ Canal de suporte criado: {canal.mention}", ephemeral=True)
        await canal.send(f"📞 Olá {user.mention}, nossa equipe irá te atender em breve.")


async def setup(bot):
    await bot.add_cog(PainelSistemaBSI(bot))
