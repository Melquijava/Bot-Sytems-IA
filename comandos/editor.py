import discord
from discord.ext import commands

class EditorView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            label="Abrir Editor",
            url="https://editor.systemsbsi.com",  # Substitua pelo link real
            style=discord.ButtonStyle.link
        ))

class Editor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="editor")
    async def editor_command(self, ctx):
        embed = discord.Embed(
            title="Editor Front-End Exclusivo",
            description=(
                "**Teste HTML, CSS e JS em tempo real!**\n\n"
                "Clique no botão abaixo para acessar a ferramenta oficial da comunidade Systems_BSI."
            ),
            color=discord.Color.blue()
        )
        embed.set_footer(text="*Powered by Systems_BSI* • **Desenvolvido por RA Corporation**")

        await ctx.send(embed=embed, view=EditorView())

def setup(bot):
    bot.add_cog(Editor(bot))
