import discord
from discord.ext import commands, tasks
import feedparser
import os
from openai import AsyncOpenAI
import re 

CANAL_NOTICIAS_ID = 1360845409454526564


URL_IMAGEM_PINGUSYS = "https://i.imgur.com/CMuTsTf.png"

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class NoticiasHacker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_links = {}
        self.feeds = self.carregar_feeds()
        self.verificar_noticias.start()

    def carregar_feeds(self):
        return {
            "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
            "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
            "Cybersecurity News": "https://cybersecuritynews.com/feed/",
            "Security Affairs": "https://securityaffairs.com/wp-rss2.php",
            "Dark Reading": "https://www.darkreading.com/rss.xml",
            "Krebs on Security": "https://krebsonsecurity.com/feed/",
            "SecurityWeek": "https://feeds.feedburner.com/securityweek",
            "Threatpost": "https://threatpost.com/feed/",
            "Naked Security (Sophos)": "https://nakedsecurity.sophos.com/feed/",
            "CISA Alerts (GOV)": "https://www.cisa.gov/news-events/alerts.xml",
            "Exploit Database": "https://www.exploit-db.com/rss.xml",
            "Zero Day - ZDNet": "https://www.zdnet.com/topic/security/rss.xml",
            "SC Media": "https://www.scmagazine.com/home/feed/",
            "Cisco Talos": "https://blog.talosintelligence.com/rss/",
            "Palo Alto Unit 42": "https://unit42.paloaltonetworks.com/feed/",
            "Mandiant (FireEye)": "https://www.mandiant.com/rss.xml"
        }

    def limpar_html(self, texto):
        """Remove tags HTML básicas para economizar tokens na IA."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', texto)

    async def resumir_com_ia(self, titulo, conteudo_bruto):
        """Usa o PinguSys para resumir a notícia."""
        conteudo_limpo = self.limpar_html(conteudo_bruto)[:1500] 
        
        prompt = f"""
        Você é o PinguSys 🐧, o mascote de cibersegurança.
        Abaixo está o título e um trecho de uma notícia técnica.
        Título: {titulo}
        Conteúdo: {conteudo_limpo}

        Sua tarefa: Resuma esta notícia em EXATAMENTE 3 tópicos curtos (bullet points), em português, fáceis de entender.
        Use um tom animado, informativo e use emojis adequados em cada tópico.
        """
        try:
            completion = await aclient.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=300,
                temperature=0.6,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro na IA ao resumir notícia: {e}")
            return None

    @tasks.loop(minutes=30)
    async def verificar_noticias(self):
        canal = self.bot.get_channel(CANAL_NOTICIAS_ID)
        if not canal:
            print("❌ Canal de notícias não encontrado.")
            return

        for nome_fonte, url in self.feeds.items():
            try:
                feed = feedparser.parse(url)
                if not feed.entries:
                    continue

                noticia = feed.entries[0]
                link = noticia.link

                if self.last_links.get(nome_fonte) != link:
                    self.last_links[nome_fonte] = link
                    titulo = noticia.title
                    
                    conteudo = getattr(noticia, 'description', getattr(noticia, 'summary', ''))

                    resumo_pingusys = await self.resumir_com_ia(titulo, conteudo)

                    embed = discord.Embed(
                        title=f"📰 {titulo}",
                        url=link,
                        color=discord.Color.green()
                    )
                    
                    if resumo_pingusys:
                        embed.description = f"**Análise do PinguSys:**\n\n{resumo_pingusys}"
                    else:

                        embed.description = "🐧 Clique no título para ler a matéria completa."

                    embed.set_thumbnail(url=URL_IMAGEM_PINGUSYS)
                    embed.set_footer(text=f"Fonte: {nome_fonte}")

                    await canal.send(embed=embed)

            except Exception as e:
                print(f"Erro ao processar feed {nome_fonte}: {e}")
                continue

    @verificar_noticias.before_loop
    async def before_verificar(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(NoticiasHacker(bot))