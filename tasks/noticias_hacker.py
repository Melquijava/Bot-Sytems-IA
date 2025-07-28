import discord
from discord.ext import commands, tasks
import feedparser
import json
import os

CANAL_NOTICIAS_ID = 1399043309120520212

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

    @tasks.loop(minutes=30)
    async def verificar_noticias(self):
        canal = self.bot.get_channel(CANAL_NOTICIAS_ID)
        if not canal:
            print("❌ Canal de notícias não encontrado.")
            return

        for nome, url in self.feeds.items():
            feed = feedparser.parse(url)
            if not feed.entries:
                continue

            noticia = feed.entries[0]
            link = noticia.link

            if self.last_links.get(nome) != link:
                self.last_links[nome] = link
                titulo = noticia.title
                await canal.send(f"📰 **[{nome}]**\n**{titulo}**\n🔗 {link}")

    @verificar_noticias.before_loop
    async def before_verificar(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(NoticiasHacker(bot))
