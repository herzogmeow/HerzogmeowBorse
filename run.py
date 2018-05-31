import discord
import asyncio
import time
import _thread
from cmd import *
from res import *

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    try:
        userid = message.author.id
        message.content = message.content.lower()
        channel = message.channel
        avatarurl = client.user.default_avatar_url
        if message.content.startswith('b!'):
            command = str(message.content)[2:]
            await insertCmd(userid, command)
        msgtitle, msgdisc, msgcolor, msgname, msgtime = await reply()
        if msgtitle != "0":
            em = discord.Embed(title=msgtitle, description=msgdisc, colour=msgcolor, timestamp=msgtime)
            em.set_author(name=msgname, icon_url=avatarurl)
            await client.send_message(message.channel, embed=em)
    except Exception as e:
        print("on_message :"+str(e))

client.run('DiscordToken')