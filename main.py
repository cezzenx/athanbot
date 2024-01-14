import discord
import aladhan 
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from keys import * 
import time
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
    await ctx.send("__Prayer Times for {}__\n".format(time.strftime("%A %B %d, %Y")) + prayer_text)

#auto athan joiner
#---
    
user_last_channel = {}
user_last_channel[default_channel] = "" #default channel that bot can join when no one has joined a channel recently
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and (int(after.channel.id) != int(blacklisted_channel)):  # User joined a voice channel
        user_last_channel.clear()
        user_last_channel[after.channel.id] = ""
        
@tasks.loop(seconds=60)
async def athan_checker():
    times = athan_client.get_today_times()
    current_time = time.strftime("%H:%M")
    prayer_24timings=""

    for adhan in times:
        prayer_24timings += " " + adhan.readable_timing(show_date=False, _24h=True)
    if current_time in prayer_24timings:
        channel_to_join = client.get_channel(list(user_last_channel.keys())[0])
        voice = await channel_to_join.connect()
        source = FFmpegPCMAudio("athan" + str(random.randrange(1,6,1)) + str(".mp3"))
        player = voice.play(source, after=lambda e:client.loop.create_task(leave_channel(channel_to_join, e)))

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


