import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime, time, date, timezone

CANAL_CRONOGRAMA_ID = 1424944981914685440  
CANAL_PLACAR_ID = 1424945024000458883      
CARGO_STAFF_NOME = "CEO, Gerente"     
CARGO_INSCRITO_ID = 1427011343659307068   

DATA_INICIO_EVENTO = date(2025, 10, 19) 
DATA_FIM_EVENTO = date(2025, 10, 26)   

FUSO_HORARIO = timezone.utc


DATA_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", ".")
PONTOS_FILENAME = os.path.join(DATA_DIR, "pontos_desafio.json")


CRONOGRAMA_DADOS = {
    19: {
        "dia": "Pré-Evento – Domingo", "emoji": "👋",
        "eventos": [
            ("18:00", "Abertura oficial do canal e boas-vindas aos participantes."),
            ("19:00", "Publicação das Regras Gerais e do FAQ."),
            ("20:00", "Último lembrete para inscrições e ambientação no Discord.")
        ]
    },
    20: {
        "dia": "Dia 1 – Segunda-feira", "emoji": "💡",
        "eventos": [
            ("09:00", "Lançamento dos 5 primeiros desafios (lógica e raciocínio)."),
            ("18:00", "Lembrete de prazo."),
            ("23:59", "Encerramento das submissões do Dia 1.")
        ]
    },
    21: {
        "dia": "Dia 2 – Terça-feira", "emoji": "🎨",
        "eventos": [
            ("09:00", "Liberação dos desafios (design, mini-vídeo, pesquisa)."),
            ("12:00", "Divulgação do placar parcial do Dia 1 e destaques."),
            ("23:59", "Encerramento das submissões do Dia 2.")
        ]
    },
    22: {
        "dia": "Dia 3 – Quarta-feira", "emoji": "🔍",
        "eventos": [
            ("09:00", "Desafios de criptografia, Easter Egg e construção criativa."),
            ("12:00", "Placar acumulado (Dia 1 + 2)."),
            ("23:59", "Encerramento das submissões do Dia 3.")
        ]
    },
    23: {
        "dia": "Dia 4 – Quinta-feira", "emoji": "👩‍💻",
        "eventos": [
            ("09:00", "Desafios de codificação e interação."),
            ("12:00", "Atualização do placar + enquete interativa."),
            ("23:59", "Encerramento das submissões do Dia 4.")
        ]
    },
    24: {
        "dia": "Dia 5 – Sexta-feira", "emoji": "🚀",
        "eventos": [
            ("09:00", "Desafios finais (análise de dados, pitch de ideias, mini-site)."),
            ("18:00", "Último lembrete de prazo."),
            ("23:59", "Fechamento de todas as submissões individuais."),
        ]
    },
    25: {
        "dia": "Dia 6 – Sábado", "emoji": "🤝",
        "eventos": [
            ("09:00", "(Em caso de Empate) Início da Rodada Bônus em equipe: Criação de uma Rede Social."),
            ("Durante o dia", "Suporte técnico e motivacional."),
            ("23:59", "Entrega final do projeto bônus.")
        ]
    },
    26: {
        "dia": "Dia 7 – Domingo", "emoji": "🏆",
        "eventos": [
            ("Manhã", "Avaliação dos projetos bônus."),
            ("15:00", "Anúncio do TOP 10 oficial e do grande campeão!"),
            ("Pós-evento", "Publicação de destaques e galeria de momentos.")
        ]
    }
}


class DesafioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.placar_message_id = None
        self.avisos_enviados_hoje = []
        self.enviar_cronograma_diario.start()
        self.verificar_avisos.start()

    def carregar_pontos(self):
        if not os.path.exists(PONTOS_FILENAME):
            return {}
        try:
            with open(PONTOS_FILENAME, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def salvar_pontos(self, pontos):
        with open(PONTOS_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(pontos, f, indent=4)

    @commands.command(name="cronograma_completo")
    @commands.has_permissions(administrator=True)
    async def cronograma_completo(self, ctx):
        """Envia o cronograma completo do evento."""
        embed = discord.Embed(
            title="🏆 Cronograma Completo - Semana de Desafios Systems BSI",
            description="Fique por dentro de todas as atividades da nossa semana de competição!",
            color=discord.Color.blue()
        )
        for dia_num, info in CRONOGRAMA_DADOS.items():
            valor = "\n".join([f"**{hora}** – {desc}" for hora, desc in info["eventos"]])
            embed.add_field(name=f"{info['emoji']} {info['dia']}", value=valor, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command(name="addpontos")
    @commands.has_role(CARGO_STAFF_NOME)
    async def add_pontos(self, ctx, membro: discord.Member, pontos_str: str):
        """Adiciona pontos a um participante. Ex: !addpontos @usuario 1.5"""
        try:
            pontos_a_add = float(pontos_str.replace(',', '.'))
        except ValueError:
            await ctx.send("❌ Formato de pontos inválido. Use números (ex: `10` ou `1.5`).")
            return

        cargo_inscrito = ctx.guild.get_role(CARGO_INSCRITO_ID)
        if cargo_inscrito not in membro.roles:
            await ctx.send(f"❌ O membro {membro.mention} não está inscrito no evento.")
            return

        pontos_db = self.carregar_pontos()
        id_membro = str(membro.id)
        
        pontos_db[id_membro] = pontos_db.get(id_membro, 0) + pontos_a_add
        self.salvar_pontos(pontos_db)
        
        await ctx.send(f"✅ **{pontos_a_add}** pontos adicionados para {membro.mention}. Pontuação total: **{pontos_db[id_membro]:.2f}**.")
        await self.atualizar_placar()

    @commands.command(name="placar")
    async def placar(self, ctx):
        """Mostra o placar atual do evento."""
        await self.atualizar_placar(canal_id=ctx.channel.id, force_new_message=True)

    @commands.command(name="anunciar_vencedores")
    @commands.has_role(CARGO_STAFF_NOME)
    async def anunciar_vencedores(self, ctx):
        """Anuncia os vencedores do evento com base no placar final."""
        pontos_db = self.carregar_pontos()
        if not pontos_db:
            await ctx.send("Ainda não há pontuações registradas.")
            return

        sorted_placar = sorted(pontos_db.items(), key=lambda item: item[1], reverse=True)
        
        embed = discord.Embed(
            title="🏆🎉 RESULTADO FINAL - SEMANA DE DESAFIOS! 🎉🏆",
            description="Após uma semana incrível de dedicação e talento, temos nossos campeões! Parabéns a todos os participantes!",
            color=discord.Color.gold()
        )

        top_3_desc = ""
        for i, (membro_id, pontos) in enumerate(sorted_placar[:3]):
            membro = ctx.guild.get_member(int(membro_id))
            medalhas = ["🥇", "🥈", "🥉"]
            top_3_desc += f"{medalhas[i]} **{membro.mention if membro else f'ID:{membro_id}'}** - {pontos:.2f} pontos\n"
        embed.add_field(name="PÓDIO DOS VENCEDORES", value=top_3_desc, inline=False)

        top_10_desc = ""
        for i, (membro_id, pontos) in enumerate(sorted_placar[3:10]):
            membro = ctx.guild.get_member(int(membro_id))
            top_10_desc += f"**{i+4}º** - {membro.mention if membro else f'ID:{membro_id}'} - {pontos:.2f} pontos\n"
        if top_10_desc:
            embed.add_field(name="DESTAQUES DO TOP 10", value=top_10_desc, inline=False)
            
        embed.set_footer(text="Obrigado a todos por tornarem este evento memorável!")
        await ctx.send(content="@everyone", embed=embed)

    @tasks.loop(time=time(8, 0, 0, tzinfo=FUSO_HORARIO))
    async def enviar_cronograma_diario(self):
        hoje = datetime.now(FUSO_HORARIO).date()
        if not (DATA_INICIO_EVENTO <= hoje <= DATA_FIM_EVENTO):
            return

        info_dia = CRONOGRAMA_DADOS.get(hoje.day)
        if info_dia:
            canal = self.bot.get_channel(CANAL_CRONOGRAMA_ID)
            self.avisos_enviados_hoje.clear() 
            
            embed = discord.Embed(
                title=f"{info_dia['emoji']} Cronograma de Hoje: {info_dia['dia']}",
                color=discord.Color.random()
            )
            descricao = "\n".join([f"**{hora}** – {desc}" for hora, desc in info_dia["eventos"]])
            embed.description = descricao
            embed.set_footer(text="Preparem-se e boa sorte a todos!")
            await canal.send(content="@everyone", embed=embed)

    @tasks.loop(minutes=1)
    async def verificar_avisos(self):
        agora = datetime.now(FUSO_HORARIO)
        hoje = agora.date()
        
        if not (DATA_INICIO_EVENTO <= hoje <= DATA_FIM_EVENTO):
            return

        info_dia = CRONOGRAMA_DADOS.get(hoje.day)
        if info_dia and info_dia["eventos"]:
            canal = self.bot.get_channel(CANAL_CRONOGRAMA_ID)
            for hora_str, desc in info_dia["eventos"]:
                if ":" in hora_str:
                    hora, minuto = map(int, hora_str.split(':'))
                    if agora.hour == hora and agora.minute == minuto and hora_str not in self.avisos_enviados_hoje:
                        embed = discord.Embed(
                            title=f"🔔 Lembrete de Atividade!",
                            description=f"**Agora ({hora_str}):** {desc}",
                            color=discord.Color.yellow()
                        )
                        await canal.send(embed=embed)
                        self.avisos_enviados_hoje.append(hora_str)

    async def atualizar_placar(self, canal_id=None, force_new_message=False):
        canal_alvo_id = canal_id or CANAL_PLACAR_ID
        canal = self.bot.get_channel(canal_alvo_id)
        if not canal: return

        pontos_db = self.carregar_pontos()
        
        embed = discord.Embed(
            title="🏆 Placar do Desafio - Top 10",
            timestamp=datetime.now(FUSO_HORARIO)
        )
        
        if not pontos_db:
            embed.description = "Ainda não há pontos registrados. A competição está prestes a começar!"
            embed.color = discord.Color.greyple()
        else:
            sorted_placar = sorted(pontos_db.items(), key=lambda item: item[1], reverse=True)
            embed.color = discord.Color.purple()
            descricao_placar = ""
            for i, (membro_id, pontos) in enumerate(sorted_placar[:10]):
                membro = canal.guild.get_member(int(membro_id))
                medalhas = ["🥇", "🥈", "🥉"]
                posicao = medalhas[i] if i < 3 else f"**{i+1}º**"
                descricao_placar += f"{posicao} {membro.mention if membro else f'ID:{membro_id}'} - **{pontos:.2f} pontos**\n"
            embed.description = descricao_placar

        if force_new_message:
            await canal.send(embed=embed)
            return

        try:
            if self.placar_message_id and canal_id is None: 
                msg = await canal.fetch_message(self.placar_message_id)
                await msg.edit(embed=embed)
            else:
                raise discord.NotFound
        except (discord.NotFound, discord.HTTPException):
            async for message in canal.history(limit=10):
                if message.author == self.bot.user:
                    await message.delete()
            msg = await canal.send(embed=embed)
            if canal_id is None:
                self.placar_message_id = msg.id


async def setup(bot):
    await bot.add_cog(DesafioCog(bot))