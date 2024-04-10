import discord
import aladhan 
from discord import app_commands
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio
from keys import * 
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
    await set_status()
    athan_checker.start()
    print("BOT ONLINE!")
    print('----------------------')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

#----------------------------------------------------------------------------------------
#start of commands

async def set_status():
    await client.change_presence(activity=discord.Game(name='Updated 4/9/24'))

@client.tree.command(name='athan')
async def athan(interaction: discord.Interaction):
    times = athan_client.get_today_times()
    prayer_text = ""
    for adhan in times:
        prayer_text += "**{}**: {}\n".format(adhan.get_en_name(), adhan.readable_timing(show_date=False))
    await interaction.response.send_message("__**Prayer Times for {}**__\n".format(datetime.datetime.now(pytz.timezone('Canada/Mountain')).strftime("%A %B %d, %Y")) + prayer_text)

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
    await ctx.send('joining manually. i will leave automatically when finished. if i dont, use command `.leave`.')
    if (ctx.author.voice): #if user is in vc, then join that vc
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        athan_to_play = ("athan" + str(random.randrange(1,5,1)) + str(".mp3"))
        source = FFmpegPCMAudio(athan_to_play)
        player = voice.play(source, after=lambda e:client.loop.create_task(leave_channel(channel, e)))
        print("MANUALLY: {} was joined. {} was played".format(channel, athan_to_play))
    else:
        await ctx.send("ur not in vc")

@client.command()
async def servers(ctx):
    await ctx.send(user_last_channel)

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
        min, max = (1, 2) if current_time < '10:00' else (2, 6)
        athan_to_play = ("athan" + str(random.randrange(min,max,1)) + str(".mp3"))
        for ch_id in user_last_channel.values():
            channel_to_join = client.get_channel(ch_id)
            voice = await channel_to_join.connect()
            source = FFmpegPCMAudio(athan_to_play)
            player = voice.play(source, after=lambda e:client.loop.create_task(leave_channel(channel_to_join, e)))
            print("{} was joined. {} was played".format(channel_to_join, athan_to_play))

async def leave_channel(channel, error):
    for voice_client in client.voice_clients:
        await voice_client.disconnect()
        user_last_channel.clear()
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