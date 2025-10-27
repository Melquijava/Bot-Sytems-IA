import discord
from discord.ext import commands, tasks
import json
import os
import asyncio
from datetime import datetime, timezone

CARGO_INSCRITO_ID = 1432238299740766230     
CARGO_STAFF_NOMES = "Gerente, CEO"   
CARGO_CEO_NOME = "Gerente, CEO"      

CANAL_ENVIOS_ID = 1432187214430863423         # ID do canal #🕸️-envios-de-sites
CANAL_RANKING_ID = 1432201629939142676        # ID do canal #🏆-ranking-halloween
CANAL_LOGS_ID = 1432239849833889953           # ID do canal privado #📜-logs-halloween

PONTOS_POR_EGG_NAO_ENCONTRADO = 5
BONUS_DESIGN = 10
BONUS_INTERATIVO = 5

DATA_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", ".")
HALLOWEEN_FILENAME = os.path.join(DATA_DIR, "halloween_data.json")


class HalloweenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ranking_message_id = None

    def carregar_dados(self):
        if not os.path.exists(HALLOWEEN_FILENAME): return {}
        try:
            with open(HALLOWEEN_FILENAME, 'r', encoding='utf-8') as f: return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): return {}

    def salvar_dados(self, data):
        with open(HALLOWEEN_FILENAME, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)

    def tem_cargo_staff(self, autor, nivel='staff'):
        cargos_permitidos_str = CARGO_CEO_NOME if nivel == 'ceo' else CARGO_STAFF_NOMES
        cargos_permitidos = [cargo.strip() for cargo in cargos_permitidos_str.split(',')]
        cargos_autor = [role.name for role in autor.roles]
        return any(cargo in cargos_autor for cargo in cargos_permitidos)

    async def log_action(self, embed):
        canal_log = self.bot.get_channel(CANAL_LOGS_ID)
        if canal_log: await canal_log.send(embed=embed)

    @commands.command(name="inscrever")
    async def inscrever(self, ctx):
        cargo = ctx.guild.get_role(CARGO_INSCRITO_ID)
        if not cargo: return await ctx.send("❌ Erro de configuração: O cargo de inscrição não foi encontrado.")
        
        if cargo in ctx.author.roles:
            return await ctx.send("👻 Você já está inscrito no Halloween Challenge!", delete_after=10)

        await ctx.author.add_roles(cargo)
        await ctx.send(f"🎃 Bem-vindo ao Halloween Challenge, {ctx.author.mention}! Verifique sua DM para as regras.", delete_after=10)
        
        try:
            dm_embed = discord.Embed(title="🕸️ Instruções do Halloween Challenge 2025 🕸️", description="Aqui está tudo que você precisa saber para participar...", color=0xff4500)
            dm_embed.add_field(name="1. Crie seu Site", value="Desenvolva um site com tema de Halloween e esconda Easter Eggs nele.", inline=False)
            dm_embed.add_field(name="2. Envie seu Projeto", value=f"Use o comando `!enviar <link> <nº de easter eggs>` no servidor para registrar sua submissão.", inline=False)
            dm_embed.add_field(name="3. A Caça", value="A Staff terá 3 minutos para encontrar seus Easter Eggs. Quanto menos encontrarem, mais pontos você ganha!", inline=False)
            await ctx.author.send(embed=dm_embed)
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, não consegui te enviar as regras na DM. Verifique suas configurações de privacidade!", delete_after=15)

        log_embed = discord.Embed(title="✅ Nova Inscrição", description=f"{ctx.author.mention} se inscreveu no evento.", color=discord.Color.green())
        await self.log_action(log_embed)

    @commands.command(name="enviar")
    async def enviar(self, ctx, link: str, quantidade_easter_eggs: int):
        cargo_inscrito = ctx.guild.get_role(CARGO_INSCRITO_ID)
        if not cargo_inscrito or cargo_inscrito not in ctx.author.roles:
            return await ctx.send("❌ Você precisa estar inscrito para enviar um site. Use `!inscrever`.")

        if not link.startswith(('http://', 'https://')):
            return await ctx.send("❌ Por favor, envie um link válido (começando com http:// ou https://).")

        dados = self.carregar_dados()
        dados[str(ctx.author.id)] = {
            "link": link,
            "total_eggs": quantidade_easter_eggs,
            "score": 0
        }
        self.salvar_dados(dados)

        canal_envios = self.bot.get_channel(CANAL_ENVIOS_ID)
        if canal_envios:
            embed = discord.Embed(title=f"🎃 Nova Submissão de {ctx.author.name}!", color=0xff4500)
            embed.add_field(name="🌐 Link do Site", value=link, inline=False)
            embed.add_field(name="🥚 Easter Eggs Declarados", value=str(quantidade_easter_eggs), inline=False)
            embed.set_thumbnail(url=ctx.author.display_avatar.url)
            await canal_envios.send(embed=embed)

        await ctx.send("✅ Submissão registrada com sucesso!")
        log_embed = discord.Embed(title="📝 Novo Envio", description=f"{ctx.author.mention} enviou o site: {link} ({quantidade_easter_eggs} eggs).", color=discord.Color.blue())
        await self.log_action(log_embed)

    @commands.command(name="timer")
    async def timer(self, ctx, tempo_str: str):
        if not self.tem_cargo_staff(ctx.author):
            return await ctx.send("❌ Apenas a Staff pode iniciar o cronômetro.")
        
        try:
            if tempo_str.lower().endswith('m'):
                segundos = int(tempo_str[:-1]) * 60
                unidade = "minuto(s)"
            elif tempo_str.lower().endswith('s'):
                segundos = int(tempo_str[:-1])
                unidade = "segundo(s)"
            else: raise ValueError
        except ValueError:
            return await ctx.send("❌ Formato de tempo inválido. Use `3m` para minutos ou `30s` para segundos.")

        await ctx.send(f"⏱️ Cronômetro iniciado por **{segundos // 60 if unidade == 'minuto(s)' else segundos} {unidade}**! Boa caça, Staff!")
        await asyncio.sleep(segundos)
        await ctx.send(f"⏰ **Tempo esgotado!** Lembre-se de registrar a pontuação com `!registrar`.")

    @commands.command(name="registrar")
    async def registrar(self, ctx, membro: discord.Member, *, args: str):
        if not self.tem_cargo_staff(ctx.author):
            return await ctx.send("❌ Apenas a Staff pode registrar pontos.")

        try:
            partes = args.lower().split()
            params = {}
            bonus = []
            for parte in partes:
                if "=" in parte:
                    key, value = parte.split('=', 1)
                    params[key] = int(value)
                elif parte.startswith('+'):
                    bonus.append(parte[1:])
        except Exception:
            return await ctx.send("❌ Formato de comando inválido. Ex: `!registrar @user encontrados=3 total=7 +design`")

        encontrados = params.get('encontrados')
        total = params.get('total')
        if encontrados is None or total is None:
            return await ctx.send("❌ Faltando argumentos. É necessário `encontrados=<n>` e `total=<n>`.")

        nao_encontrados = total - encontrados
        pontos = nao_encontrados * PONTOS_POR_EGG_NAO_ENCONTRADO
        
        desc_pontuacao = f"🥚 Easter Eggs não encontrados: {nao_encontrados} ({nao_encontrados} x {PONTOS_POR_EGG_NAO_ENCONTRADO} = {pontos} pts)\n"
        if 'design' in bonus:
            pontos += BONUS_DESIGN
            desc_pontuacao += f"🎨 Design Criativo: +{BONUS_DESIGN} pts\n"
        if 'interativo' in bonus:
            pontos += BONUS_INTERATIVO
            desc_pontuacao += f"💫 Interatividade: +{BONUS_INTERATIVO} pts\n"

        dados = self.carregar_dados()
        dados[str(membro.id)] = dados.get(str(membro.id), {})
        dados[str(membro.id)]['score'] = dados[str(membro.id)].get('score', 0) + pontos
        self.salvar_dados(dados)

        embed = discord.Embed(title=f"✅ Pontuação registrada para {membro.name}", color=discord.Color.green())
        embed.description = desc_pontuacao
        embed.add_field(name="🔢 Total Adicionado", value=f"**{pontos} pontos**")
        await ctx.send(embed=embed)
        
        log_embed = discord.Embed(title="🧮 Pontuação Registrada", description=f"{ctx.author.mention} registrou {pontos} pontos para {membro.mention}.", color=discord.Color.purple())
        await self.log_action(log_embed)
        await self.atualizar_ranking()

    @commands.command(name="ranking")
    async def ranking(self, ctx):
        await self.atualizar_ranking(force_new_message=True, channel_id=ctx.channel.id)

    @commands.command(name="halloweenhelp")
    async def halloweenhelp(self, ctx):
        embed = discord.Embed(title="🎃 Ajuda - Halloween Challenge 2025", color=0xff4500)
        embed.add_field(name="Comandos de Participante", value="`!inscrever` - Entra no evento.\n`!enviar <link> <nº de eggs>` - Envia seu site.", inline=False)
        embed.add_field(name="Canais Importantes", value=f"Envios: <#{CANAL_ENVIOS_ID}>\nRanking: <#{CANAL_RANKING_ID}>", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="finalizar")
    async def finalizar(self, ctx):
        if not self.tem_cargo_staff(ctx.author, nivel='ceo'):
            return await ctx.send("❌ Apenas o CEO pode finalizar o evento.")

        dados = self.carregar_dados()
        if not dados: return await ctx.send("Nenhuma pontuação registrada para finalizar.")

        sorted_placar = sorted(dados.items(), key=lambda item: item[1].get('score', 0), reverse=True)
        
        embed = discord.Embed(title="🎃 Halloween Challenge 2025 Finalizado! 🎃", color=0xff4500)
        desc_final = ""
        medalhas = ["🥇", "🥈", "🥉"]
        for i, (membro_id, data) in enumerate(sorted_placar[:10]):
            membro = ctx.guild.get_member(int(membro_id))
            posicao = medalhas[i] if i < 3 else f"**{i+1}º**"
            desc_final += f"{posicao} {membro.mention if membro else f'ID:{membro_id}'} - **{data.get('score', 0)} pts**\n"
        embed.description = desc_final
        await ctx.send(content="@everyone", embed=embed)

        cargo_inscrito = ctx.guild.get_role(CARGO_INSCRITO_ID)
        if cargo_inscrito:
            for membro in cargo_inscrito.members:
                await membro.remove_roles(cargo_inscrito, reason="Fim do evento Halloween Challenge.")
        await ctx.send("✅ Cargo de participante removido de todos os membros.")
        log_embed = discord.Embed(title="💀 Evento Finalizado", description=f"O evento foi finalizado por {ctx.author.mention}.", color=discord.Color.red())
        await self.log_action(log_embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user: return
        
        respostas = {
            '🎃': 'O medo está no ar…',
            '👻': 'Você ousa continuar?',
            '🦇': 'A Staff está te observando... 😈'
        }
        for trigger, response in respostas.items():
            if trigger in message.content:
                await message.channel.send(response)
                break 

    async def atualizar_ranking(self, force_new_message=False, channel_id=None):
        canal_alvo_id = channel_id or CANAL_RANKING_ID
        canal = self.bot.get_channel(canal_alvo_id)
        if not canal: return

        dados = self.carregar_dados()
        embed = discord.Embed(title="🎃 Ranking Atual – Halloween Challenge 2025", color=0xff4500)
        if not dados:
            embed.description = "O ranking ainda está vazio. Seja o primeiro a pontuar!"
        else:
            sorted_placar = sorted(dados.items(), key=lambda item: item[1].get('score', 0), reverse=True)
            desc_ranking = ""
            for i, (membro_id, data) in enumerate(sorted_placar[:10]):
                membro = canal.guild.get_member(int(membro_id))
                posicao = ["1️⃣", "2️⃣", "3️⃣"][i] if i < 3 else f"**{i+1}º**"
                desc_ranking += f"{posicao} {membro.mention if membro else f'ID:{membro_id}'} - **{data.get('score', 0)} pts**\n"
            embed.description = desc_ranking

        if force_new_message: return await canal.send(embed=embed)

        try:
            if self.ranking_message_id:
                msg = await canal.fetch_message(self.ranking_message_id)
                await msg.edit(embed=embed)
            else: raise discord.NotFound
        except (discord.NotFound, discord.HTTPException):
            async for message in canal.history(limit=10):
                if message.author == self.bot.user: await message.delete()
            msg = await canal.send(embed=embed)
            self.ranking_message_id = msg.id

async def setup(bot):
    await bot.add_cog(HalloweenCog(bot))