import discord
import asyncio
import sqlite3
import sys
import json
import urllib
import urllib.request
import math

from datetime import datetime, timedelta

client = discord.Client()
EZAPI = "https://easyallies.com/api/site/getHome"

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith('!schedule'):
		tmp = await client.send_message(message.channel, 'Fetching Schedule...')
		with urllib.request.urlopen(EZAPI) as response:
			data = response.read()

		if data is None:
			await client.edit_message(tmp, 'Failed to fetch schedule.')
		data = data.decode("utf-8")
		decoded = json.loads(data)
		decoded = decoded["schedule"]
		upcoming = ""
		for event in decoded:
			time = datetime.strptime(event["date"], '%Y-%m-%dT%H:%M:%S.%fZ')
			timeTo = time - datetime.utcnow()
			if timeTo.days == 0:
				upcoming += "**{}**: {}h {}min. \n".format(event["title"], math.floor(timeTo.seconds / 3600), math.floor((timeTo.seconds / 60) % 60))
			elif timeTo.days < 3 and timeTo.days > 0:
				upcoming += "**{}**: {} day(s) {}h {}min. \n".format(event["title"], timeTo.days, math.floor(timeTo.seconds / 3600), math.floor((timeTo.seconds / 60) % 60))

		em = discord.Embed(title='Upcoming events.', color=0xbe0121, description = upcoming)
		await client.edit_message(tmp, "Schedule loaded.", embed=em)
client.run(sys.argv[1])
