# main.py
import os
from pickle import dump as pdump
from pickle import load as pload
import discord
from discord.ext import commands
import pandas as pd

## Load Environmental Variables
#load_dotenv()
creds = pload(open('creds.pkl','rb'))
TOKEN = creds['token']
channel_list = ['general','twsnbn-thursday-afternoon','announcements']
music_list = pd.read_csv('music_meta.csv',delimiter=',')

## Check if User Message List Exists
def load_users():
    if os.path.exists('user_list.pkl'):
        user_list = list(set(pload(open('user_list.pkl','rb'))))
    else:
        user_list = []
        pdump(user_list,open('user_list.pkl','wb'))
    return user_list

## Check if Bot is Connected to Guild VC
def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

## Define Bot
bot = commands.Bot(command_prefix="!", case_insensitive=True)

## Bot Login
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

## Join VC
@bot.command(name="join",description="Join VC")
async def join(ctx):
    vc = ctx.author.voice.channel
    await vc.connect()

## Leave VC
@bot.command(name="leave",description="Leave VC")
async def leave(ctx):
    await ctx.voice_client.disconnect()
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## List Music
@bot.command(name="list_music",description="List all music available")
async def list_music(ctx):
    for xx in music_list.itertuples():
        msg = str(xx.Index+1)+" - "+xx.song
        await ctx.send(msg)
        #embed = discord.Embed(title="Song",description=xx.Index+1)
        #embed.add_field(name="Song Title",value=xx.song)
        #embed.add_field(name="Song Ref Number",value=xx.Index)
        #await ctx.send(content=None,embed=embed)

## Join VC and Play Mood Music
@bot.command(name="play",description="Play Mood Music")
async def play(ctx,*,arg):
    # Gets voice channel of message author
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    song = music_list.iloc[int(arg)-1]
    if cid in user_list:
        if ctx.message.author.voice and (not ctx.message.guild.voice_client) and (int(arg) < 50):
            embed = discord.Embed(title="Now Playing")
            embed.add_field(name="Title",value=song['song'])
            embed.add_field(name="Link",value=song['link'])
            embed.add_field(name="License",value=song['license'])
            await ctx.send(content=None,embed=embed)
            await ctx.author.voice.channel.connect()
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
            vc = server.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['location']))
        elif ctx.message.author.voice and ctx.message.guild.voice_client and (not voice_channel.is_playing()) \
             and (int(arg) < 50):
            embed = discord.Embed(title="Now Playing")
            embed.add_field(name="Title",value=song['song'])
            embed.add_field(name="Link",value=song['link'])
            embed.add_field(name="License",value=song['license'])
            await ctx.send(content=None,embed=embed)
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['location']))
        elif ctx.message.author.voice and voice_channel.is_playing() and (int(arg) < 50):
            embed = discord.Embed(title="Now Playing")
            embed.add_field(name="Title",value=song['song'])
            embed.add_field(name="Link",value=song['link'])
            embed.add_field(name="License",value=song['license'])
            await ctx.send(content=None,embed=embed)
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
            voice_channel.stop()
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['location']))
        elif int(arg) > 49:
            await ctx.send("No such song")
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
        try:
            await ctx.message.delete()
        except Exception as err:
            print(str(err)[:250])

## Pause Music
@bot.command(name="pause",description="Pause Mood Music")
async def pause(ctx):
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    if cid in user_list:
        if voice_channel:
            if voice_channel.is_playing():
                voice_channel.pause()
            else:
                await ctx.send("No music playing")
        else:
            await ctx.send("Bot is not connected to a VC")
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Resume Music
@bot.command(name="resume",description="Resume Mood Music")
async def resume(ctx):
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    if cid in user_list:
        if voice_channel:
            if voice_channel.is_paused():
                voice_channel.resume()
            else:
                await ctx.send("No music to resume")
        else:
            await ctx.send("Bot is not connected to a VC")
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Stop Music
@bot.command(name="stop",description="Stop Mood Music")
async def pause(ctx):
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    if cid in user_list:
        if voice_channel:
            if voice_channel.is_playing():
                voice_channel.stop()
                await voice_channel.disconnect()
            else:
                await ctx.send("No music playing")
        else:
            await ctx.send("Bot is not connected to a VC")
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Add User to User Message List
@bot.command(name="add_user",description="Add user to DM list")
async def add_user(ctx,*args):
    user_list = load_users()
    list_users = [str(user_mentioned.id) for user_mentioned in ctx.message.mentions]
    for xx in list_users:
#        print(xx)
        if xx not in user_list:
#            print(xx)
            user_list = user_list + [xx]
    pdump(user_list,open('user_list.pkl','wb'))
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## List Users
@bot.command(name="list_users",description="List All DM Users")
async def list_users(ctx,*args):
    user_list = load_users()
    for xx in user_list:
        await ctx.author.send(xx)
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Set Text Channel
@bot.command(name="set_channel",description="Set Channel for Bot Commands")
async def set_channel(ctx):
    user_list = load_users()
    cid = str(ctx.author.id)
    if cid in user_list:
        channel = str(ctx.channel)
        await ctx.send('Channel set')
    else:
        await ctx.send('User not authorized to perform this action')
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

#keep_alive()
bot.run(TOKEN)
