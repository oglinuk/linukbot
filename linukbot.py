'''
linukbot - linue's discord bot
'''
import os
import csv
import time
import random
import pickle
import asyncio
import discord

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as %s:%s' % (client.user.id, client.user.name))
    print('---------------------------------------------')
    # getting bot to join the general channel
    yield from client.join_voice_channel(client.get_channel(YOUR CHANNEL ID HERE))

@client.event
@asyncio.coroutine
def on_message(message):
    # joke
    if message.content.startswith('!joke'):
        yield from client.send_message(message.channel, 'There is no place like 127.0.0.1')
    # flip
    if message.content.startswith('!flip'):
        flip = random.choice(['Heads', 'Tails'])
        yield from client.send_message(message.channel, flip)
    # purge
    if message.content.startswith('!purge'):
        if message.content[6:] == '':
            purgeLimit = 100
        else:
            purgeLimit = message.content[6:]
        yield from client.send_message(message.channel, 'Clearing! %s messages...' % (purgeLimit))
        time.sleep(2)
        yield from client.purge_from(message.channel, limit=int(purgeLimit))
    # save song
    if message.content.startswith('!savesong'):
        yield from client.send_message(message.channel, '!purge 3')
        time.sleep(2)
        yield from client.send_message(message.channel, 'Saving %s to the songlist. To view songs in the list type !songlist.' % (message.content[9:]))
        if not os.path.isfile('songlist.pkl'):
            songlist = []
        else:
            with open('songlist.pkl', 'rb') as f:
                songlist = pickle.load(f)
        songlist.append(message.content[9:])
        with open('songlist.pkl', 'wb') as f:
            pickle.dump(songlist, f)
    # songlist
    if message.content.startswith('!songlist'):
        with open('songlist.pkl', 'rb') as f:
            songlist = pickle.load(f)
        yield from client.send_message(message.channel, [song for song in songlist])
    # random song that is combined with the !play command for MusicBot - NOTE the bot must be in the same channel as the music bot
    if message.content.startswith('!rngsong'):
        with open('songlist.pkl', 'rb') as f:
            songlist = pickle.load(f)
        yield from client.send_message(message.channel, '!play %s' % (random.choice(songlist)))
    # inside joke
    if message.content.startswith('!dropshoes'):
        yield from client.send_message(message.channel, 'You have now died %s' % (message.author.name))
    # thanks
    if message.content.startswith('!th'):
        yield from client.send_message(message.channel, 'You are welcome %s' % (message.author.name))
    # when you want to roast yourself for dying in league of legends
    if message.content.startswith('!lolidied'):
        yield from client.send_message(message.channel, 'Pfft another death in league I see %s' % (message.author.name))
    # live game on op.gg for league of legends
    if message.content.startswith('!livegame'):
        yield from client.send_message(message.channel, 'http://oce.op.gg/summoner/userName=%s' % (message.content[9:]).replace(' ', ''))

# automatic assignment of Follower role when a person joins the discord server
@client.event
@asyncio.coroutine
def on_voice_state_update(before, after):
    followerRole = discord.utils.get(before.server.roles, id=YOUR ROLE ID HERE) # Get role id by '\@role'
    if not before.voice == after.voice:
        try:
            if after.voice_channel.id == YOUR CHANNEL ID HERE: # Get channel id by right-clicking channel -> copy ID
                yield from client.add_roles(after, followerRole)
        except AttributeError:
            yield from client.remove_roles(after, followerRole)

# greet when a person joins the discord server
@client.event
@asyncio.coroutine
def on_member_join(member):
    yield from client.send_message(client.get_channel(YOUR HOME CHANNEL ID HERE), 'Welcome to the domain of kami OGLinuk - ' + member.name)

client.run(YOUR BOT TOKEN HERE)
