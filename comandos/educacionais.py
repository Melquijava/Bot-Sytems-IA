from discord.ext import commands
import random
import discord

class Educacionais(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.resposta_certa = None 
        

    @commands.command(name="aula_programacao")
    async def aula_programacao(self, ctx):
        aulas_programacao = [
            "💻 [Curso básico de Python – Curso em Vídeo](https://www.youtube.com/watch?v=S9uPNppGsGo)",
            "📘 [Banco de Dados para Iniciantes – Bóson Treinamentos](https://www.youtube.com/watch?v=Ofktstne-utM)",
            "🌐 [HTML + CSS do Zero – Danki Code](https://www.youtube.com/watch?v=3oSIqIq3N3M)",
            "⚙️ [Git e GitHub do Zero – Curso em Vídeo](https://www.youtube.com/watch?v=xEKo29OWILE)",
            "📙 [Curso de Lógica de Programação – Curso em Vídeo](https://www.youtube.com/watch?v=UmmTf6_4tJk)",
            "🧠 [Curso de Python com Projetos – Hashtag](https://www.youtube.com/watch?v=QSZC7X5tqNQ)",
            "📚 [Curso de Algoritmos – Curso em Vídeo](https://www.youtube.com/watch?v=5oC6avFCxnU)",
            "🌍 [HTML5 Completo – CFBCursos](https://www.youtube.com/watch?v=nPEaPFt1ykI)",
            "🎨 [CSS3 Completo – CFBCursos](https://www.youtube.com/watch?v=1-w1RfGJov4)",
            "📗 [SQL para Iniciantes – Bóson](https://www.youtube.com/watch?v=HtSuA80QTyo)",
            "📜 [Curso de Shell Script – Bóson](https://www.youtube.com/watch?v=9mAM2ly92lc)"
        ]
        await ctx.send(f"Aqui vai uma aula de **programação** pra você estudar hoje, salve o link pois essa mensagem será apagada em 30 segundos!\n{random.choice(aulas_programacao)}", delete_after=30)


    @commands.command(name="aula_hacking")
    async def aula_hacking(self, ctx):
        aulas_hacking = [
            "🛡️ [Introdução à Cibersegurança – Cisco NetAcad](https://www.netacad.com/pt-br/courses/cybersecurity/introduction-cybersecurity)",
            "🔒 [Hack The Box Academy (Lab Free)](https://academy.hackthebox.com/)",
            "🧩 [Criptografia – Bóson Treinamentos](https://www.youtube.com/watch?v=EpLMKrN9UE0)",
            "🔐 [Power BI para Iniciantes – Hashtag Treinamentos](https://www.youtube.com/watch?v=CMY1dzMo6o)",
            "🔧 [Redes TCP/IP para Iniciantes – Curso Gratuito](https://www.youtube.com/watch?v=uyM2ZL5jg88)",
            "🌐 [Redes de Computadores – Curso Básico](https://www.youtube.com/watch?v=YjzXq6U5iQI)",
            "🔗 [APIs REST com Node.js – Balta.io](https://www.youtube.com/watch?v=qsDvJrGMSUY)",
            "🐧 [Introdução ao Linux – Bóson Treinamentos](https://www.youtube.com/watch?v=QFgIFKzGH8w)"
        ]
        await ctx.send(f"Aqui vai uma aula de **hacking / cibersegurança** pra você estudar hoje, salve o link pois essa mensagem será apagada em 30 segundos!\n{random.choice(aulas_hacking)}", delete_after=30)


    @commands.command(name="quiz")
    async def quiz(self, ctx):
        perguntas = [
            {
                "pergunta": "Qual a linguagem mais usada para scripts de automação?",
                "opcoes": "A) Java\nB) Python\nC) C++\nD) Ruby",
                "resposta": "B"
            },
            {
                "pergunta": "O que é SQL?",
                "opcoes": "A) Linguagem de estilo\nB) Protocolo de rede\nC) Linguagem de consulta\nD) API de Java",
                "resposta": "C"
            },
            {
                "pergunta": "Qual desses é um sistema operacional?",
                "opcoes": "A) Chrome\nB) Linux\nC) GitHub\nD) HTML",
                "resposta": "B"
            },
            {
                "pergunta": "O que significa HTML?",
                "opcoes": "A) Hyper Trainer Markup Language\nB) HyperText Markup Language\nC) HighText Machine Language\nD) None",
                "resposta": "B"
            },
            {
                "pergunta": "Qual comando git clona um repositório?",
                "opcoes": "A) git pull\nB) git fork\nC) git clone\nD) git copy",
                "resposta": "C"
            },
            {
                "pergunta": "Qual é a função de um firewall?",
                "opcoes": "A) Aumentar a velocidade da internet\nB) Bloquear sites\nC) Proteger a rede contra acessos não autorizados\nD) Gerar energia",
                "resposta": "C"
            },
            {
                "pergunta": "O que faz o comando 'ls' no Linux?",
                "opcoes": "A) Remove arquivos\nB) Lista arquivos\nC) Copia diretórios\nD) Atualiza o sistema",
                "resposta": "B"
            },
            {
                "pergunta": "Qual desses não é um banco de dados relacional?",
                "opcoes": "A) MySQL\nB) MongoDB\nC) PostgreSQL\nD) Oracle",
                "resposta": "B"
            },
            {
                "pergunta": "Qual linguagem é mais usada no desenvolvimento web?",
                "opcoes": "A) Python\nB) JavaScript\nC) C\nD) Go",
                "resposta": "B"
            },
            {
                "pergunta": "Qual ferramenta é usada para versionamento de código?",
                "opcoes": "A) Docker\nB) Git\nC) npm\nD) Jenkins",
                "resposta": "B"
            },
            {
                "pergunta": "O que faz um analista de dados?",
                "opcoes": "A) Escreve artigos\nB) Analisa informações para apoiar decisões\nC) Cadastra usuários\nD) Monta PCs",
                "resposta": "B"
            },
            {
                "pergunta": "Em qual camada OSI está o protocolo TCP?",
                "opcoes": "A) Aplicação\nB) Transporte\nC) Sessão\nD) Física",
                "resposta": "B"
            },
            {
                "pergunta": "O que é phishing?",
                "opcoes": "A) Técnica de backup\nB) Golpe de engenharia social\nC) Banco de dados\nD) Ferramenta de monitoramento",
                "resposta": "B"
            },
            {
                "pergunta": "Qual desses não é um sistema de gerenciamento de banco de dados?",
                "opcoes": "A) SQLite\nB) PostgreSQL\nC) Ubuntu\nD) MariaDB",
                "resposta": "C"
            },
            {
                "pergunta": "Qual comando compila um programa em C?",
                "opcoes": "A) run cfile\nB) gcc cfile.c\nC) bash cfile\nD) make run",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é o navegador padrão do Windows?",
                "opcoes": "A) Firefox\nB) Safari\nC) Edge\nD) Chrome",
                "resposta": "C"
            },
            {
                "pergunta": "O que representa uma 'chave primária' em um banco de dados?",
                "opcoes": "A) Uma senha\nB) Um índice aleatório\nC) Identificador único\nD) Chave de criptografia",
                "resposta": "C"
            },
            {
                "pergunta": "Qual desses é um protocolo de segurança?",
                "opcoes": "A) HTTP\nB) FTP\nC) SSH\nD) SMTP",
                "resposta": "C"
            },
            {
                "pergunta": "Qual função do Python exibe algo no terminal?",
                "opcoes": "A) echo()\nB) display()\nC) print()\nD) show()",
                "resposta": "C"
            },
            {
                "pergunta": "Qual comando exibe seu IP no Windows?",
                "opcoes": "A) ipconfig\nB) get-ip\nC) ifconfig\nD) netstat",
                "resposta": "A"
            },
            {
                "pergunta": "O que é um 'fork' no Git?",
                "opcoes": "A) Criar um novo branch\nB) Clonar um repositório\nC) Criar uma cópia independente de um repositório\nD) Mesclar branches",
                "resposta": "C"
            },
            {
                "pergunta": "Qual é a principal função de um servidor web?",
                "opcoes": "A) Armazenar arquivos\nB) Hospedar sites e aplicações web\nC) Proteger redes\nD) Gerenciar usuários",
                "resposta": "B"
            },
            {
                "pergunta": "O que é uma API?",
                "opcoes": "A) Aplicação de rede\nB) Interface de Programação de Aplicações\nC) Protocolo de Internet\nD) Banco de Dados",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'git commit'?",
                "opcoes": "A) Enviar alterações para o repositório remoto\nB) Criar um novo branch\nC) Salvar alterações no repositório local\nD) Clonar um repositório",
                "resposta": "C"
            },
            {
                "pergunta": "O que é um 'bug' em programação?",
                "opcoes": "A) Um tipo de software\nB) Um erro ou falha no código\nC) Uma ferramenta de teste\nD) Um protocolo de rede",
                "resposta": "B"
            },
            {
                "pergunta": "Qual linguagem é usada para estilizar páginas web?",
                "opcoes": "A) HTML\nB) CSS\nC) JavaScript\nD) Python",
                "resposta": "B"
            },
            {
                "pergunta": "O que é um 'loop' em programação?",
                "opcoes": "A) Uma função matemática\nB) Um ciclo de repetição de código\nC) Um tipo de dado\nD) Uma estrutura de dados",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'npm install'?",
                "opcoes": "A) Instalar pacotes Node.js\nB) Atualizar o sistema\nC) Compilar código\nD) Criar um novo projeto",
                "resposta": "A"
            },
            {
                "pergunta": "O que é um 'framework'?",
                "opcoes": "A) Um tipo de banco de dados\nB) Uma biblioteca de código reutilizável\nC) Um protocolo de rede\nD) Um sistema operacional",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a principal função do Docker?",
                "opcoes": "A) Gerenciar usuários\nB) Criar containers para aplicações\nC) Proteger redes\nD) Hospedar sites",
                "resposta": "B"
            },
            {
                "pergunta": "O que é um 'endpoint' em uma API?",
                "opcoes": "A) Um ponto de acesso à rede\nB) Uma URL que recebe requisições\nC) Um tipo de dado\nD) Uma função matemática",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'git push'?",
                "opcoes": "A) Enviar alterações para o repositório remoto\nB) Clonar um repositório\nC) Criar um novo branch\nD) Mesclar branches",
                "resposta": "A"
            },
            {
                "pergunta": "O que é um 'algoritmo'?",
                "opcoes": "A) Um tipo de software\nB) Uma sequência de passos para resolver um problema\nC) Um protocolo de rede\nD) Um banco de dados",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'ping'?",
                "opcoes": "A) Enviar arquivos\nB) Testar conectividade com outro host\nC) Listar arquivos\nD) Atualizar o sistema",
                "resposta": "B"
            },
            {
                "pergunta": "O que é um 'script'?",
                "opcoes": "A) Um tipo de banco de dados\nB) Um programa escrito em uma linguagem de script\nC) Uma ferramenta de teste\nD) Um protocolo de rede",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a principal função do Git?",
                "opcoes": "A) Proteger redes\nB) Gerenciar usuários\nC) Controlar versões de código-fonte\nD) Hospedar sites",
                "resposta": "C"
            },
            {
                "pergunta": "O que é um 'merge' no Git?",
                "opcoes": "A) Criar um novo branch\nB) Mesclar alterações de diferentes branches\nC) Clonar um repositório\nD) Enviar alterações para o repositório remoto",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'curl'?",
                "opcoes": "A) Enviar emails\nB) Transferir dados de ou para um servidor\nC) Listar arquivos\nD) Atualizar o sistema",
                "resposta": "B"
            },
            {
                "pergunta": "O que é uma 'variável' em programação?",
                "opcoes": "A) Um tipo de dado\nB) Um espaço na memória para armazenar valores\nC) Uma função matemática\nD) Um protocolo de rede",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a principal função do Node.js?",
                "opcoes": "A) Proteger redes\nB) Criar aplicações web escaláveis usando JavaScript no servidor\nC) Gerenciar usuários\nD) Hospedar sites estáticos",
                "resposta": "B"
            },
            {
                "pergunta": "O que é um 'repository' no Git?",
                "opcoes": "A) Um tipo de banco de dados\nB) Um local onde o código-fonte é armazenado e versionado\nC) Uma ferramenta de teste\nD) Um protocolo de rede",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'git status'?",
                "opcoes": "A) Enviar alterações para o repositório remoto\nB) Exibir o estado atual do repositório local\nC) Clonar um repositório\nD) Criar um novo branch",
                "resposta": "B"
            },
            {
                "pergunta": "O que é um 'commit' no Git?",
                "opcoes": "A) Enviar alterações para o repositório remoto\nB) Salvar alterações no repositório local com uma mensagem descritiva\nC) Clonar um repositório\nD) Criar um novo branch",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a função do comando 'git branch'?",
                "opcoes": "A) Enviar alterações para o repositório remoto\nB) Criar, listar ou excluir branches no repositório local\nC) Clonar um repositório\nD) Mesclar branches",
                "resposta": "B"
            },
            {
                "pergunta": "O que é um 'framework' de front-end?",
                "opcoes": "A) Uma biblioteca de código reutilizável para desenvolvimento web\nB) Um tipo de banco de dados\nC) Um protocolo de rede\nD) Um sistema operacional",
                "resposta": "A"
            },
            {
                "pergunta": "Qual é a função do comando 'git log'?",
                "opcoes": "A) Exibir o histórico de commits do repositório\nB) Enviar alterações para o repositório remoto\nC) Clonar um repositório\nD) Criar um novo branch",
                "resposta": "A"
            },
            {
                "pergunta": "O que é um 'container' no Docker?",
                "opcoes": "A) Um tipo de banco de dados\nB) Uma unidade leve e portátil que contém uma aplicação e suas dependências\nC) Um protocolo de rede\nD) Um sistema operacional",
                "resposta": "B"
            },
            {
                "pergunta": "Qual é a principal função do React?",
                "opcoes": "A) Proteger redes\nB) Criar interfaces de usuário interativas usando JavaScript\nC) Gerenciar usuários\nD) Hospedar sites estáticos",
                "resposta": "B"
            },
        ]

        q = random.choice(perguntas)
        self.resposta_certa = q["resposta"].lower()  # salva para checagem depois
        await ctx.send(f"🧪 **Quiz:**\n{q['pergunta']}\n{q['opcoes']}\nResponda com A, B, C ou D. Pense rápido, você tem 30 segundos!",
                       delete_after=30)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Verifica se uma resposta está sendo aguardada
        if self.resposta_certa:
            conteudo = message.content.strip().lower()
            if conteudo in ["a", "b", "c", "d"]:
                if conteudo == self.resposta_certa:
                    await message.channel.send("✅ Resposta correta, parabéns!")
                else:
                    await message.channel.send(f"❌ Resposta incorreta. A certa era **{self.resposta_certa.upper()}**.")
                self.resposta_certa = None  # limpa para não repetir
                

async def setup(bot):
    await bot.add_cog(Educacionais(bot))