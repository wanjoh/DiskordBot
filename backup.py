import wavelink as wavelink

from strings import *
from apikeys import *
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
import os
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import urllib.request
import re
import time

starttime = time.time()
client = commands.Bot(command_prefix='!', activity=discord.Game(s_status))

loop = False


@client.event
async def on_ready():
    print(s_ready)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(s_nemaDjidanja)


@client.command()
async def zop(ctx):
    await ctx.send(s_zop)


@client.command()
async def pomoc(ctx):
    await ctx.send(s_pomoc)


@client.command(pass_context=True)
async def izadji(ctx):
    if checkUser(ctx):
        return
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send(s_nestanem)
        bot_voice = False
    else:
        await ctx.message.add_reaction(e_srednji)


@client.command()
async def resi(ctx, arg):
    if ctx.author.id in ban_list:
        return
    await ctx.send(s_dado + arg + s_suki)


def checkUrl(url) -> bool:
    validate = URLValidator()
    try:
        validate(url)
        return True
    except ValidationError as exception:
        return False


def checkUser(ctx) -> bool:
    if ctx.author.id in ban_list:
        return True
    return False


@resi.error
async def resi_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(s_kogaResiti)


"""
Komande vezane za muziku
"""

@wavelink.WavelinkMixin.listener("on_track_end")
async def on_player_stop(ctx, audio, voice):
    if loop is True:
        await voice.play(audio)

@client.command(pass_context=True)
async def pusti(ctx, *, url):
    global loop
    if checkUser(ctx):
        return
    if ctx.author.voice:
        song_there = os.path.isfile(s_songName)
        try:
            if song_there:
                os.remove(s_songName)
        except PermissionError:
            await ctx.send(s_nijeGotovo)
            return
        #print(song_there)
        channel = ctx.message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        if voice is None:
            voice = await channel.connect()

        if checkUrl(url) is False:
            url = url.replace(" ", "+")
            # print("1")
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + url)
            # print("2")
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            url = "https://youtube.com/watch?v=" + video_ids[0]

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, s_songName)
                break
        # print("lopo" + loop)
        await ctx.send("pustam " + url)

        await voice.play(discord.FFmpegPCMAudio(s_songName))
    else:
        await ctx.message.add_reaction(e_srednji)
        await ctx.send(s_nemaDjidanja)


@client.command(pass_context=True)
async def stani(ctx):
    if checkUser(ctx):
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await ctx.send(s_stani)
    else:
        await ctx.send(s_nemaDjidanja)
        await ctx.message.add_reaction(e_srednji)


@client.command(pass_context=True)
async def cekaj(ctx):
    if checkUser(ctx):
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send(s_cekam)
    else:
        await ctx.send(s_nemaDjidanja)
        await ctx.message.add_reaction(e_srednji)


@client.command(pass_context=True)
async def nastavi(ctx):
    if checkUser(ctx):
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send(s_nastavi)
    else:
        await ctx.send(s_nemaDjidanja)
        await ctx.message.add_reaction(e_srednji)


@client.command()
async def repeat(ctx, arg):
    global loop
    if arg.lower() in no_list:
        loop = False
    if arg.lower() in yes_list:
        loop = True



@repeat.error
async def repeat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(s_noArg)


@pusti.error
async def pusti_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(s_staPustiti)


client.run(token_bot)
