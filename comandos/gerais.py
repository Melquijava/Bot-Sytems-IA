import discord
from discord.ext import commands
import random

class Gerais(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ajuda")
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="📘 Bem-vindo ao Systems_BSI!",
            description=(
                "Aqui estão os comandos e utilidades disponíveis no nosso bot.\n"
                "Clique nos botões abaixo para interagir ou navegar pelos recursos:"
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url="https://i.imgur.com/omtFl1y.png")
        embed.set_footer(text="Desenvolvido por Systems_BSI")

        view = AjudaView()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="desafio")
    async def desafio(self, ctx):
        desafios = [
            "🔢 **Desafio:** Escreva um código que inverta uma string sem usar funções prontas.",
            "📁 **Desafio:** Crie um script que liste todos os arquivos `.txt` em uma pasta.",
            "🔐 **Desafio:** Faça uma função que valide uma senha (mínimo 8 caracteres, 1 número, 1 letra maiúscula).",
            "🧮 **Desafio:** Crie uma função recursiva que calcule o fatorial de um número.",
            "📊 **Desafio:** Escreva um código que calcule a média de uma lista de números.",
            "🐍 **Desafio:** Faça um programa que detecte se uma palavra é um palíndromo (ex: ‘arara’, ‘ana’).",
            "🌐 **Desafio:** Crie um script que faça uma requisição HTTP e exiba o status da resposta.",
            "📅 **Desafio:** Desenvolva um calendário simples que exiba o mês atual e permita navegar entre meses.",
            "📝 **Desafio:** Escreva um programa que leia um arquivo de texto e conte quantas vezes cada palavra aparece.",
            "🎲 **Desafio:** Crie um jogo simples de adivinhação onde o usuário tenta adivinhar um número aleatório entre 1 e 100.",
            "📈 **Desafio:** Faça um script que leia dados de um arquivo CSV e calcule a soma de uma coluna específica.",
            "🔄 **Desafio:** Implemente uma função que receba duas listas e retorne uma lista com os elementos únicos de ambas.",
            "🖼️ **Desafio:** Crie um programa que baixe uma imagem da internet e a salve no seu computador.",
            "📚 **Desafio:** Escreva um código que leia um arquivo JSON e exiba os dados de forma organizada.",
            "🔗 **Desafio:** Desenvolva um script que extraia todos os links de uma página web e os exiba.",
            "🧩 **Desafio:** Implemente um algoritmo de ordenação (como Bubble Sort ou Quick Sort) em uma lista de números.",
            "🎨 **Desafio:** Crie um gerador de senhas aleatórias com letras, números e símbolos.",
            "📖 **Desafio:** Escreva um programa que leia um livro digital (ePub ou PDF) e conte o número de páginas.",
            "🕹️ **Desafio:** Desenvolva um jogo de texto onde o usuário deve escolher entre diferentes opções para avançar na história.",
            "🔍 **Desafio:** Crie um script que busque por uma palavra específica em um arquivo de texto e exiba as linhas onde ela aparece.",
            "💾 **Desafio:** Implemente um sistema simples de CRUD (Create, Read, Update, Delete) usando um banco de dados SQLite.",
            "🌟 **Desafio:** Desenvolva um bot simples que responda a comandos básicos no Discord, como `!olá` ou `!ajuda`.",
            "📊 **Desafio:** Crie um gráfico simples usando uma biblioteca como Matplotlib ou Plotly para visualizar dados aleatórios.",
            "🧩 **Desafio:** Escreva um programa que resolva o jogo da velha (Tic Tac Toe) jogando contra o computador.",
            "🔄 **Desafio:** Implemente uma função que converta números romanos para inteiros e vice-versa.",
            "🌐 **Desafio:** Crie um script que verifique se um site está online ou offline, fazendo uma requisição HTTP.",
            "📅 **Desafio:** Desenvolva um programa que calcule a diferença entre duas datas em dias, meses e anos.",
            "📝 **Desafio:** Escreva um código que gere um resumo de um texto longo, mantendo as ideias principais.",
            "🎲 **Desafio:** Crie um jogo de dados onde o usuário pode rolar um ou mais dados e ver o resultado.",
            "📚 **Desafio:** Implemente um sistema de anotações onde o usuário pode adicionar, listar e remover anotações.",
            "🔗 **Desafio:** Desenvolva um script que verifique a validade de URLs em uma lista e retorne as válidas.",
            "🖼️ **Desafio:** Crie um programa que aplique um filtro simples em uma imagem (como preto e branco ou sépia).",
            "📖 **Desafio:** Escreva um código que gere citações aleatórias de livros famosos.",
            "🕹️ **Desafio:** Desenvolva um jogo de adivinhação de palavras, onde o usuário deve descobrir uma palavra secreta letra por letra.",
            "🔍 **Desafio:** Crie um script que analise um log de servidor e conte o número de acessos por IP.",
            "💾 **Desafio:** Implemente um sistema de autenticação simples onde o usuário pode se registrar e fazer login.",
            "🌟 **Desafio:** Desenvolva um bot que envie uma mensagem aleatória de motivação ou humor quando solicitado.",
            "📊 **Desafio:** Crie um programa que leia dados de um arquivo Excel e gere gráficos com esses dados.",
            "🧩 **Desafio:** Escreva um código que resolva um quebra-cabeça simples, como o jogo 15 (15-puzzle).",
            "🔄 **Desafio:** Implemente uma função que converta temperaturas entre Celsius, Fahrenheit e Kelvin."
        ]
        await ctx.send(random.choice(desafios), ephemeral=True, delete_after=120)

    @commands.command(name="dica")
    async def dica(self, ctx):
        dicas = [
            "🧠 **Dica:** Pratique todos os dias, mesmo que por 20 minutos. A consistência supera a intensidade.",
            "📚 **Dica:** Aprenda Git e GitHub — controle de versão é essencial pra qualquer dev.",
            "🔐 **Dica:** Nunca use senhas repetidas. Use um gerenciador como Bitwarden ou 1Password.",
            "🧰 **Dica:** Use o site [roadmap.sh](https://roadmap.sh/) para guiar seus estudos em programação.",
            "🚀 **Dica:** Faça projetos pequenos e publique no GitHub. É melhor que 10 certificados.",
            "🕵️‍♂️ **Dica:** Curioso sobre hacking ético? Comece estudando redes e Linux básico primeiro.",
            "💡 **Dica:** Participe de comunidades online como Stack Overflow, Reddit ou Discord para aprender com outros devs.",
            "📖 **Dica:** Leia a documentação das linguagens e frameworks que você usa. É lá que estão os segredos!",
            "🎯 **Dica:** Defina metas claras e alcançáveis. Por exemplo, aprender uma nova linguagem em 3 meses.",
            "🛠️ **Dica:** Familiarize-se com ferramentas de desenvolvimento como Docker, Postman e Visual Studio Code.",
            "🌐 **Dica:** Aprenda os fundamentos de HTML, CSS e JavaScript. Eles são a base da web.",
            "📈 **Dica:** Aprenda sobre bancos de dados relacionais e não relacionais. SQL é um must!",
            "🤝 **Dica:** Colabore em projetos open source. É uma ótima forma de aprender e fazer networking.",
            "📅 **Dica:** Organize seu tempo de estudo com técnicas como Pomodoro ou Kanban.",
            "📝 **Dica:** Mantenha um diário de programação. Anote o que aprendeu e os desafios que enfrentou.",
            "🎓 **Dica:** Assista a cursos online, mas não se esqueça de praticar o que aprendeu. A teoria sem prática não vale nada.",
            "🔍 **Dica:** Sempre busque entender o porquê das coisas. Não decore soluções, entenda os conceitos.",
            "💬 **Dica:** Não tenha medo de perguntar. A comunidade é cheia de pessoas dispostas a ajudar.",
            "🖥️ **Dica:** Aprenda sobre testes automatizados. Eles são essenciais para garantir a qualidade do código.",
            "📊 **Dica:** Familiarize-se com ferramentas de análise de código como SonarQube ou ESLint.",
            "🌱 **Dica:** Nunca pare de aprender. A tecnologia muda rápido, e você também deve mudar com ela.",
            "🧩 **Dica:** Aprenda sobre design patterns. Eles ajudam a escrever código mais limpo e reutilizável.",
            "🔗 **Dica:** Contribua com a comunidade. Responder perguntas em fóruns ou ajudar iniciantes é uma ótima forma de aprender."
            ]
        await ctx.send(random.choice(dicas), ephemeral=True, delete_after=120)


class AjudaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📚 Comandos", style=discord.ButtonStyle.primary, custom_id="cmd_comandos")
    async def comandos(self, interaction: discord.Interaction, button: discord.ui.Button):
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

    @discord.ui.button(label="🧑‍💻 Meu Perfil", style=discord.ButtonStyle.secondary, custom_id="cmd_perfil")
    async def perfil(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "🔗 Use `!perfil` para visualizar seu perfil.\n"
            "📝 Use `!setgithub <url>` e `!setlinkedin <url>` para cadastrar seus links.",
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
    await bot.add_cog(Gerais(bot))
