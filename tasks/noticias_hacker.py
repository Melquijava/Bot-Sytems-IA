import discord
from discord.ext import commands, tasks
import feedparser
import os
from openai import AsyncOpenAI
import re
from datetime import datetime, timezone

CANAL_NOTICIAS_ID = 1426946302679453726

URL_IMAGEM_PINGUSYS = "https://i.imgur.com/CMuTsTf.png"

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class NoticiasHacker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.links_ja_postados = set() 
        self.feeds = self.carregar_feeds()
        self.verificar_noticias.start()

    def carregar_feeds(self):
        feeds = {
            "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
            "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
            "Security Affairs": "https://securityaffairs.com/wp-rss2.php",
            "Dark Reading": "https://www.darkreading.com/rss.xml",
            "CISA Alerts (GOV)": "https://www.cisa.gov/news-events/alerts.xml",
            "Exploit Database": "https://www.exploit-db.com/rss.xml",
            
            "freeCodeCamp": "https://www.freecodecamp.org/news/rss/",
            "CSS-Tricks": "https://css-tricks.com/feed/",
            "Dev.to": "https://dev.to/feed",
            "Martin Fowler": "https://martinfowler.com/feed.atom",
            "A List Apart": "https://alistapart.com/main/feed/",
            "CodingHorror": "https://blog.codinghorror.com/rss/",
        }
        return feeds

    def limpar_html(self, texto):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', texto)

    async def resumir_com_ia(self, titulo, conteudo_bruto):
        conteudo_limpo = self.limpar_html(conteudo_bruto)[:2000]
        
        prompt = f"""
        Você é o PinguSys 🐧, o mascote tech do servidor.
        Abaixo está o título e um trecho de uma notícia.
        Título: {titulo}
        Conteúdo: {conteudo_limpo}

        Sua tarefa: Resuma esta notícia em 3 tópicos curtos (bullet points), em português.
        Use uma linguagem clara, direta e um tom animado. Adicione emojis que combinem com o tema (ex: 💻, 🚀, 💡, 🔒).
        """
        try:
            completion = await aclient.chat.completions.create(
                model="gpt-3.5-turbo", 
                messages=[{"role": "system", "content": prompt}],
                max_tokens=350,
                temperature=0.6,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro na IA ao resumir notícia: {e}")
            return None

    @tasks.loop(minutes=60)
    async def verificar_noticias(self):
        canal = self.bot.get_channel(CANAL_NOTICIAS_ID)
        if not canal:
            print("❌ Canal de notícias não encontrado.")
            return

        novas_noticias = []
        
        for nome_fonte, url in self.feeds.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    link = entry.link
                    if link not in self.links_ja_postados:
                        data_publicacao = datetime.now(timezone.utc)  
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            data_publicacao = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                        
                        novas_noticias.append({
                            'fonte': nome_fonte,
                            'titulo': entry.title,
                            'link': link,
                            'data': data_publicacao,
                            'conteudo': getattr(entry, 'description', getattr(entry, 'summary', ''))
                        })
            except Exception as e:
                print(f"Erro ao processar o feed {nome_fonte}: {e}")
                continue
        
        if not novas_noticias:
            print("Nenhuma notícia nova encontrada neste ciclo.")
            return

        noticia_escolhida = sorted(novas_noticias, key=lambda x: x['data'], reverse=True)[0]

        resumo_pingusys = await self.resumir_com_ia(noticia_escolhida['titulo'], noticia_escolhida['conteudo'])
        
        if resumo_pingusys:
            embed = discord.Embed(
                title=f"📰 {noticia_escolhida['titulo']}",
                url=noticia_escolhida['link'],
                description=f"**Análise do PinguSys:**\n\n{resumo_pingusys}",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=URL_IMAGEM_PINGUSYS)
            embed.set_footer(text=f"Fonte: {noticia_escolhida['fonte']} • Publicado em: {noticia_escolhida['data'].strftime('%d/%m/%Y às %H:%M')}")

            await canal.send(embed=embed)

            self.links_ja_postados.add(noticia_escolhida['link'])

    @verificar_noticias.before_loop
    async def before_verificar(self):
        await self.bot.wait_until_ready()
        print("🐧 Serviço de notícias do PinguSys iniciado.")

async def setup(bot):
    await bot.add_cog(NoticiasHacker(bot))