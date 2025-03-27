import os

import asyncio
import discord
import yt_dlp

from discord import app_commands
from  discord.ext import commands
from collections import deque
from dotenv import load_dotenv


def discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f"{bot.user} is jamming")

    @bot.tree.command(name="play", description="Play or add a song to the queue")
    @app_commands.describe(song="Song name")
    

    async def play(interaction: discord.Interaction, song: str):
        await interaction.response.defer()


        try:
            voice_channel = interaction.user.voice.channel
        except AttributeError: 
            await interaction.followup.send("You must be in a voice channel!")
            return
        

        voice_client = interaction.guild.voice_client
        guild_id = interaction.guild_id


        if not voice_client:
            voice_client = await voice_channel.connect()
        elif voice_channel != voice_client.channel:
            await voice_client.move_to(voice_channel)
        

        data = await asyncio.to_thread(ytdl.extract_info, song, download=False)
        if data is None:
            await interaction.followup.send("No match found")
            return

        url = data["entries"][0]["url"]
        title = data["entries"][0]["title"]
        
        if guild_id not in guild_que:
            guild_que[guild_id] = deque()

        if voice_client.is_playing() or voice_client.is_paused() or len(guild_que[guild_id]) >= 1:
            guild_que[guild_id].append([url, title])
            await interaction.followup.send(f"{title} added to queue")
            return
        else:
            guild_que[guild_id].append([url, title])
            await play_next(voice_client, interaction, guild_id)
        


    async def play_next(voice_client, interaction, guild_id):
        if len(guild_que[guild_id]) >= 1:


            def after(error):
                if error:
                    print(f"Error:{error}")
                else:
                    asyncio.run_coroutine_threadsafe(play_next(voice_client, interaction, guild_id), bot.loop)


            url, title = guild_que[guild_id].pop()
            player = discord.FFmpegPCMAudio(url, **ffmpeg_options)
            await interaction.followup.send(f"Now playing {title}")
            voice_client.play(player, after=after)
        else:
            print("Queue is empty. Finished playing.")
            await voice_client.disconnect()



    @bot.tree.command(name="skip", description="Skip current song")
    async def skip(interaction: discord.Interaction):
        await interaction.response.defer()
        voice_client = interaction.guild.voice_client

        try:
            voice_channel = interaction.user.voice.channel
        except AttributeError:
            await interaction.followup.send("You must be in a voice channel")
            return

        if not voice_client or (not guild_que[interaction.guild_id] and not voice_client.is_playing()):
            await interaction.followup.send("Nothing is playing")
            return
        else:
            voice_client.stop()



    @bot.tree.command(name="pause", description="Pauses the current song")
    async def pause(interaction: discord.Interaction):
        await interaction.response.defer()
        voice_clinet = interaction.guild.voice_client

        if not voice_clinet:
            await interaction.followup.send("Ambienator is not it a voice channel.")
            return
        if not voice_clinet.is_playing():
            await interaction.followup.send("No song to pause.")
            return
        else:
            await interaction.followup.send("Song paused!")
            voice_clinet.pause()


    @bot.tree.command(name="resume", description="Resumes the current song")
    async def resume(interaction: discord.Interaction):
        await interaction.response.defer()
        voice_clinet = interaction.guild.voice_client

        if not voice_clinet:
            await interaction.followup.send("Ambienator is not it a voice channel.")
            return
        if not voice_clinet.is_paused():
            await interaction.followup.send("No song to resume.")
            return
        else:
            await interaction.followup.send("Song resumed!")
            voice_clinet.resume()



    @bot.tree.command(name="stop", description="Stop music") 
    async def stop(interaction: discord.Interaction): 
        await interaction.response.defer() 
        voice_client = interaction.guild.voice_client

        if not voice_client: 
            await interaction.followup.send("Ambienator is not in a voice channel.")
            return
        
        if voice_client.is_playing() or voice_client.is_paused(): 
            await interaction.followup.send("Jamm stopped!")
            voice_client.stop()
            guild_que[interaction.guild_id] = deque() 
        else:
            await interaction.followup.send("Nothing is playing.")
            return
        

    @bot.tree.command(name="leave", description="Disconnect from the voice channel")
    async def leave(interaction: discord.Interaction):
        await interaction.response.defer()
        voice_client = interaction.guild.voice_client

        if not voice_client:
            await interaction.followup.send("Ambienator is not in a voice channel.")
            return
        else:
            await interaction.followup.send("Bye!")
            await voice_client.disconnect()
        

    bot.run(TOKEN)


if __name__ == "__main__":
  
load_dotenv()
ID = os.getenv("CLIENT_ID")
SECERET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("DISCORD_TOKEN")

ytdl_options = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "noplaylist": True,
    }

ffmpeg_options = {
    "options": "-vn",
    }

ytdl = yt_dlp.YoutubeDL(ytdl_options)

  discord_bot()

  guild_que = {}
