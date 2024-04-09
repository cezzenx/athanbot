import discord
import aladhan 
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from keys import * 
from mcstatus import JavaServer
import datetime
import pytz
import random

intents = discord.Intents.all()
intents.messages = True
intents.members = True
intents.guilds = True
intents.voice_states = True

location = aladhan.City("Calgary", "Canada")
athan_client = aladhan.Client(location)

client = commands.Bot(command_prefix='.', intents=intents)
@client.event
async def on_ready():
    athan_checker.start()
    print("BOT ONLINE!")
    print('----------------------')

#----------------------------------------------------------------------------------------
#start of commands
    
#test command
@client.command()
async def test(ctx):
    await ctx.send("bot is active")

#prayer command
@client.command(aliases=["salah", 'namaz', 'pray', 'timings', 'athan'])
async def prayer(ctx):
    times = athan_client.get_today_times()
    prayer_text = ""
    for adhan in times:
        prayer_text += "**{}**: {}\n".format(adhan.get_en_name(), adhan.readable_timing(show_date=False))
    await ctx.send("__Prayer Times for {}__\n".format(datetime.datetime.now(pytz.timezone('Canada/Mountain')).strftime("%A %B %d, %Y")) + prayer_text)

#mc server status
@client.command(aliases=["mc","server","online"])
async def minecraft(ctx):
    await ctx.send("getting status of mc server...")
    try:
        latency = server.ping()
        await ctx.send("server is online, with ping of {} ms.".format(int(latency)))
    except:
        await ctx.send("server is offline, izaan turn on please")

#join command plays athan
@client.command(pass_context = True)
async def join(ctx):
    await ctx.send('athan now automatically plays at athan time. you cant manually do it anymore')
    if (ctx.author.voice): #if user is in vc, then join that vc
        channel = ctx.message.author.voice.channel
        print(channel)
        print(type(channel))
        voice = await channel.connect()
        athan_to_play = ("athan" + str(random.randrange(1,5,1)) + str(".mp3"))
        source = FFmpegPCMAudio(athan_to_play)
        player = voice.play(source, after=lambda e:client.loop.create_task(leave_channel(channel, e)))
        print("{} was joined. {} was played".format(channel, athan_to_play))
    else:
        await ctx.send("ur not in vc")

#auto athan joiner
#---
    
user_last_channel = {}
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and (int(after.channel.id) != int(blacklisted_channel)):
        server_id = str(after.channel.guild.id)
        user_last_channel[server_id] = after.channel.id
        
@tasks.loop(minutes=1)
async def athan_checker():
    times = athan_client.get_today_times()
    current_time = datetime.datetime.now(pytz.timezone('Canada/Mountain')).strftime("%H:%M")
    prayer_24timings=""
    for adhan in times:
        prayer_24timings += " " + adhan.readable_timing(show_date=False, _24h=True)
    if current_time in prayer_24timings:
        for ch_id in user_last_channel.values():
            channel_to_join = client.get_channel(ch_id)
            voice = await channel_to_join.connect()
            athan_to_play = ("athan" + str(random.randrange(1,5,1)) + str(".mp3"))
            source = FFmpegPCMAudio(athan_to_play)
            player = voice.play(source, after=lambda e:client.loop.create_task(leave_channel(channel_to_join, e)))
            print("{} was joined. {} was played".format(channel_to_join, athan_to_play))

async def leave_channel(channel, error):
    await channel.guild.voice_client.disconnect()
    if error:
        print(f'Error during playback: {error}')
    else:
        print(f'Playback completed in {channel.guild.name}')
#----

#manual leave
@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("i left vc")
    else:
        await ctx.send("i am not in vc")

client.run(TOKEN)


