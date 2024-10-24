import disnake
from disnake.ext import commands
import yt_dlp
import asyncio

# Definir opções para yt-dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'cookiefile': './ck/youtube_cookies.txt',  # Adiciona o uso de cookies
    'geo_bypass': True,  # Tentar contornar restrições geográficas
    # 'proxy': 'http://seu_proxy:porta',  # Adicione seu proxy aqui, se necessário
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []  # Fila de músicas
        self.current_song = None  # Música que está tocando no momento

    async def search_youtube(self, query):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)
                return info['entries'][0]
            except Exception as e:
                print(f"Erro ao buscar no YouTube: {e}")
                return None

    async def update_status(self, title):
        activity = disnake.Game(name=f"Ouvindo {title}")
        await self.bot.change_presence(activity=activity)

    async def play_song(self, inter, song_info):
        url = song_info['url']
        title = song_info['title']

        try:
            voice_client = inter.guild.voice_client

            # Obter o áudio da música
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                audio_url = info['formats'][0]['url']

            # Tocar a música
            voice_client.play(
                disnake.PCMVolumeTransformer(disnake.FFmpegPCMAudio(audio_url)),
                after=lambda _: asyncio.run_coroutine_threadsafe(self.play_next_song(inter), self.bot.loop)
            )

            self.current_song = title
            await self.update_status(title)
            await inter.followup.send(f"🎵 Tocando agora: {title}")
        except Exception as e:
            await inter.followup.send(f"Ocorreu um erro ao tentar tocar a música: {str(e)}")

    async def play_next_song(self, inter):
        if self.song_queue:
            next_song = self.song_queue.pop(0)
            await self.play_song(inter, next_song)
        else:
            self.current_song = None
            await inter.followup.send("A fila de músicas está vazia.")

    @commands.slash_command(description="Toca uma música pelo nome ou adiciona à fila")
    async def play(self, inter: disnake.ApplicationCommandInteraction, query: str):
        # Verificar se o usuário está em um canal de voz
        if inter.author.voice is None:
            embed = disnake.Embed(
                title="Erro",
                description="Você precisa estar em um canal de voz para usar este comando.",
                color=disnake.Color.red()
            )
            await inter.response.send_message(embed=embed)
            return

        await inter.response.send_message(f"Buscando: {query}...")

        # Conectar ao canal de voz do usuário
        voice_channel = inter.author.voice.channel
        if inter.guild.voice_client is None:
            await voice_channel.connect()

        song_info = await self.search_youtube(query)

        if song_info is None:
            await inter.followup.send("Não foi possível encontrar a música.")
            return

        # Adicionar música à fila
        self.song_queue.append(song_info)
        await inter.followup.send(f"🎵 Música adicionada à fila: {song_info['title']}")

        # Tocar música se não houver nenhuma tocando no momento
        if not inter.guild.voice_client.is_playing() and not self.current_song:
            await self.play_next_song(inter)

    @commands.slash_command(description="Mostra a fila de músicas")
    async def queue(self, inter: disnake.ApplicationCommandInteraction):
        if self.song_queue:
            queue_list = "\n".join([song['title'] for song in self.song_queue])
            await inter.response.send_message(f"🎶 Fila de músicas:\n{queue_list}")
        else:
            await inter.response.send_message("A fila de músicas está vazia.")

    @commands.slash_command(description="Pausa a música atual")
    async def pause(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await inter.response.send_message("⏸️ Música pausada.")
        else:
            await inter.response.send_message("Não há música tocando no momento.")

    @commands.slash_command(description="Retoma a música pausada")
    async def resume(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await inter.response.send_message("▶️ Música retomada.")
        else:
            await inter.response.send_message("Não há música pausada no momento.")

    @commands.slash_command(description="Pula para a próxima música")
    async def skip(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()  # Isto vai automaticamente chamar `play_next_song` devido ao `after`
            await inter.response.send_message("⏭️ Música pulada.")
        else:
            await inter.response.send_message("Não há música tocando no momento.")

    @commands.slash_command(description="Sai do canal de voz")
    async def leave(self, inter: disnake.ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            self.song_queue.clear()
            await inter.response.send_message("Desconectado do canal de voz e fila de músicas limpa.")
        else:
            await inter.response.send_message("Eu não estou em nenhum canal de voz no momento.")

def setup(bot):
    bot.add_cog(Music(bot))
