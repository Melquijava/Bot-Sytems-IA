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
    19: {"dia": "Pré-Evento – Domingo", "emoji": "👋", "eventos": [("18:00", "Abertura oficial do canal e boas-vindas."), ("19:00", "Publicação das Regras Gerais e do FAQ."), ("20:00", "Último lembrete para inscrições.")]},
    20: {"dia": "Dia 1 – Segunda-feira", "emoji": "💡", "eventos": [("09:00", "Lançamento dos 5 primeiros desafios."), ("18:00", "Lembrete de prazo."), ("23:59", "Encerramento das submissões do Dia 1.")]},
    21: {"dia": "Dia 2 – Terça-feira", "emoji": "🎨", "eventos": [("09:00", "Liberação dos desafios."), ("12:00", "Divulgação do placar parcial do Dia 1."), ("23:59", "Encerramento das submissões do Dia 2.")]},
    22: {"dia": "Dia 3 – Quarta-feira", "emoji": "🔍", "eventos": [("09:00", "Desafios de criptografia e Easter Egg."), ("12:00", "Placar acumulado (Dia 1 + 2)."), ("23:59", "Encerramento das submissões do Dia 3.")]},
    23: {"dia": "Dia 4 – Quinta-feira", "emoji": "👩‍💻", "eventos": [("09:00", "Desafios de codificação."), ("12:00", "Atualização do placar."), ("23:59", "Encerramento das submissões do Dia 4.")]},
    24: {"dia": "Dia 5 – Sexta-feira", "emoji": "🚀", "eventos": [("09:00", "Desafios finais."), ("18:00", "Último lembrete de prazo."), ("23:59", "Fechamento de todas as submissões.")]},
    26: {"dia": "Dia 7 – Domingo", "emoji": "🏆", "eventos": [("Manhã", "Avaliação dos projetos bônus."), ("15:00", "Anúncio do TOP 10 oficial!"), ("Pós-evento", "Publicação de destaques.")]}
}


class DesafioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.placar_message_id = None
        self.avisos_enviados_hoje = []
        self.enviar_cronograma_diario.start()
        self.verificar_avisos.start()

    def carregar_pontos(self):
        if not os.path.exists(PONTOS_FILENAME): return {}
        try:
            with open(PONTOS_FILENAME, 'r', encoding='utf-8') as f: return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): return {}

    def salvar_pontos(self, pontos):
        with open(PONTOS_FILENAME, 'w', encoding='utf-8') as f: json.dump(pontos, f, indent=4)

    def tem_cargo_staff(self, autor):
        cargos_permitidos = [cargo.strip() for cargo in CARGO_STAFF_NOME.split(',')]
        cargos_autor = [role.name for role in autor.roles]
        return any(cargo in cargos_autor for cargo in cargos_permitidos)

    @commands.command(name="cronograma_completo")
    @commands.has_permissions(administrator=True)
    async def cronograma_completo(self, ctx):
        embed = discord.Embed(title="🏆 Cronograma Completo - Semana de Desafios", color=discord.Color.blue())
        for dia_num, info in CRONOGRAMA_DADOS.items():
            valor = "\n".join([f"**{hora}** – {desc}" for hora, desc in info["eventos"]])
            embed.add_field(name=f"{info['emoji']} {info['dia']}", value=valor, inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="addpontos")
    async def add_pontos(self, ctx, membro: discord.Member, pontos_str: str):
        if not self.tem_cargo_staff(ctx.author):
            await ctx.send(f"❌ Você não tem permissão para usar este comando. Cargos necessários: `{CARGO_STAFF_NOME}`.")
            return

        try: pontos_a_add = float(pontos_str.replace(',', '.'))
        except ValueError:
            await ctx.send("❌ Formato de pontos inválido. Use números (ex: `10` ou `1.5`).")
            return

        cargo_inscrito = ctx.guild.get_role(CARGO_INSCRITO_ID)
        if not cargo_inscrito:
            await ctx.send(f"❌ **Erro de Configuração:** O cargo de inscrito com ID `{CARGO_INSCRITO_ID}` não foi encontrado.")
            return
        if cargo_inscrito not in membro.roles:
            await ctx.send(f"❌ O membro {membro.mention} não está inscrito no evento (não possui o cargo `{cargo_inscrito.name}`).")
            return

        pontos_db = self.carregar_pontos()
        id_membro = str(membro.id)
        
        pontos_db[id_membro] = pontos_db.get(id_membro, 0) + pontos_a_add
        self.salvar_pontos(pontos_db)
        
        await ctx.send(f"✅ **{pontos_a_add:.2f}** pontos adicionados para {membro.mention}. Pontuação total: **{pontos_db[id_membro]:.2f}**.")
        await self.atualizar_placar()

    @commands.command(name="removepontos")
    async def remove_pontos(self, ctx, membro: discord.Member, pontos_str: str):
        if not self.tem_cargo_staff(ctx.author):
            await ctx.send(f"❌ Você não tem permissão para usar este comando. Cargos necessários: `{CARGO_STAFF_NOME}`.")
            return

        try: pontos_a_remover = float(pontos_str.replace(',', '.'))
        except ValueError:
            await ctx.send("❌ Formato de pontos inválido. Use números (ex: `10` ou `1.5`).")
            return

        pontos_db = self.carregar_pontos()
        id_membro = str(membro.id)

        if id_membro not in pontos_db:
            await ctx.send(f"❌ O membro {membro.mention} não possui pontos registrados para remover.")
            return
        
        pontos_db[id_membro] -= pontos_a_remover
        if pontos_db[id_membro] < 0:
            pontos_db[id_membro] = 0
        
        self.salvar_pontos(pontos_db)
        
        await ctx.send(f"✅ **{pontos_a_remover:.2f}** pontos removidos de {membro.mention}. Pontuação total: **{pontos_db[id_membro]:.2f}**.")
        await self.atualizar_placar()

    @commands.command(name="placar")
    async def placar(self, ctx):
        await self.atualizar_placar(canal_id=ctx.channel.id, force_new_message=True)

    @commands.command(name="anunciar_vencedores")
    async def anunciar_vencedores(self, ctx):
        if not self.tem_cargo_staff(ctx.author):
            await ctx.send(f"❌ Você não tem permissão para usar este comando. Cargos necessários: `{CARGO_STAFF_NOME}`.")
            return

        pontos_db = self.carregar_pontos()
        if not pontos_db:
            await ctx.send("Ainda não há pontuações registradas para anunciar os vencedores.")
            return

        sorted_placar = sorted(pontos_db.items(), key=lambda item: item[1], reverse=True)
        
        embed = discord.Embed(title="🏆🎉 RESULTADO FINAL - SEMANA DE DESAFIOS! 🎉🏆", description="Parabéns a todos os participantes!", color=discord.Color.gold())
        top_3_desc = ""
        for i, (membro_id, pontos) in enumerate(sorted_placar[:3]):
            membro = ctx.guild.get_member(int(membro_id))
            medalhas = ["🥇", "🥈", "🥉"]
            top_3_desc += f"{medalhas[i]} **{membro.mention if membro else f'ID:{membro_id}'}** - {pontos:.2f} pontos\n"
        embed.add_field(name="PÓDIO DOS VENCEDORES", value=top_3_desc if top_3_desc else "Ninguém no pódio.", inline=False)

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
        if not (DATA_INICIO_EVENTO <= hoje <= DATA_FIM_EVENTO): return

        info_dia = CRONOGRAMA_DADOS.get(hoje.day)
        if info_dia:
            canal = self.bot.get_channel(CANAL_CRONOGRAMA_ID)
            self.avisos_enviados_hoje.clear()
            embed = discord.Embed(title=f"{info_dia['emoji']} Cronograma de Hoje: {info_dia['dia']}", color=discord.Color.random())
            embed.description = "\n".join([f"**{hora}** – {desc}" for hora, desc in info_dia["eventos"]])
            embed.set_footer(text="Preparem-se e boa sorte a todos!")
            await canal.send(content="@everyone", embed=embed)

    @tasks.loop(minutes=1)
    async def verificar_avisos(self):
        agora = datetime.now(FUSO_HORARIO)
        hoje, info_dia = agora.date(), CRONOGRAMA_DADOS.get(agora.day)
        if not (DATA_INICIO_EVENTO <= hoje <= DATA_FIM_EVENTO) or not info_dia: return

        canal = self.bot.get_channel(CANAL_CRONOGRAMA_ID)
        for hora_str, desc in info_dia["eventos"]:
            if ":" in hora_str:
                hora, minuto = map(int, hora_str.split(':'))
                if agora.hour == hora and agora.minute == minuto and hora_str not in self.avisos_enviados_hoje:
                    embed = discord.Embed(title=f"🔔 Lembrete de Atividade!", description=f"**Agora ({hora_str}):** {desc}", color=discord.Color.yellow())
                    await canal.send(embed=embed)
                    self.avisos_enviados_hoje.append(hora_str)

    async def atualizar_placar(self, canal_id=None, force_new_message=False):
        canal_alvo_id = canal_id or CANAL_PLACAR_ID
        canal = self.bot.get_channel(canal_alvo_id)
        if not canal: return

        pontos_db = self.carregar_pontos()
        embed = discord.Embed(title="🏆 Placar do Desafio - Top 10", timestamp=datetime.now(FUSO_HORARIO))
        if not pontos_db:
            embed.description = "Ainda não há pontos registrados. A competição está prestes a começar!"
            embed.color = discord.Color.greyple()
        else:
            sorted_placar = sorted(pontos_db.items(), key=lambda item: item[1], reverse=True)
            embed.color = discord.Color.purple()
            descricao_placar = ""
            for i, (membro_id, pontos) in enumerate(sorted_placar[:10]):
                membro = canal.guild.get_member(int(membro_id))
                medalhas, posicao = ["🥇", "🥈", "🥉"], ""
                posicao = medalhas[i] if i < 3 else f"**{i+1}º**"
                descricao_placar += f"{posicao} {membro.mention if membro else f'ID:{membro_id}'} - **{pontos:.2f} pontos**\n"
            embed.description = descricao_placar or "Nenhuma pontuação registrada ainda."

        if force_new_message:
            await canal.send(embed=embed)
            return

        try:
            if self.placar_message_id and canal_id is None:
                msg = await canal.fetch_message(self.placar_message_id)
                await msg.edit(embed=embed)
            else: raise discord.NotFound
        except (discord.NotFound, discord.HTTPException):
            async for message in canal.history(limit=10):
                if message.author == self.bot.user: await message.delete()
            msg = await canal.send(embed=embed)
            if canal_id is None: self.placar_message_id = msg.id

async def setup(bot):
    await bot.add_cog(DesafioCog(bot))