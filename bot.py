import discord
import asyncio
import sqlite3
import sys
import json
import urllib
import urllib.request
import math
import pytz
import pytz_dict

from datetime import datetime, timedelta
from pytz import timezone

pytz_tz = pytz_dict.get_dict()
client = discord.Client()
EZAPI = "https://easyallies.com/api/site/getHome"
EZLinks = {"Twitch" : "[Twitch](https://www.twitch.tv/easyallies)", 
           "Youtube" : "[YouTube](https://www.youtube.com/channel/UCZrxXp1reP8E353rZsB3jaA)",
					 "Patreon" : "[Patreon](https://www.patreon.com/EasyAllies)"}

TZFMT = "%Y-%m-%d %H:%M %Z"
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

async def cmd_unknown(message, *args):
	await client.send_message(message.channel, 'Unknown command.')

async def cmd_schedule(message, tz = None, *args):
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
		serviceStr = EZLinks.get(event["service"], "")
		if tz is None:
			if timeTo.days == 0:
				upcoming += "**{}**: {}h {}min. {}\n".format(event["title"], math.floor(timeTo.seconds / 3600), math.floor((timeTo.seconds / 60) % 60), serviceStr)
			elif timeTo.days < 3 and timeTo.days > 0:
				upcoming += "**{}**: {} day(s) {}h {}min. {}\n".format(event["title"], timeTo.days, math.floor(timeTo.seconds / 3600), math.floor((timeTo.seconds / 60) % 60), serviceStr)
		else:
			try:
				set_tz = pytz_tz.get(tz.upper(), None)
				if set_tz is None:
					set_tz = timezone(tz)
			except:
				await client.edit_message(tmp, "Unknown timezone.")
				return
			time = time.replace(tzinfo=pytz.utc)
			time = time.astimezone(set_tz)
			if timeTo.days < 2 and timeTo.days >= 0:
				upcoming += "**{}**: {} {}\n".format(event["title"], time.strftime(TZFMT) , serviceStr)

	em = discord.Embed(title='Upcoming events.', color=0xbe0121, description = upcoming)
	await client.edit_message(tmp, "Schedule loaded.", embed=em)

async def cmd_update(message, *args):
	pytz_tz = pytz_dict.get_dict()
	await client.send_message(message.channel, 'Internal data updated.')
	
COMMANDS = {"SCHEDULE" : cmd_schedule, "UPDATE" : cmd_update}

@client.event
async def on_message(message):
	if message.content.lower().startswith('!ez'):
		command = message.content.upper().split(' ')[0][3:]
		arguments = message.content.split(' ')[1:]
		func = COMMANDS.get(command, cmd_unknown)
		await func(message, *arguments)

client.run(sys.argv[1])
