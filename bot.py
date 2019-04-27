import discord
from discord.ext import commands
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
bot = commands.Bot(command_prefix="!ez")
EZAPI = "https://easyallies.com/api/site/getHome"
EZLinks = {"Twitch" : "[Twitch](https://www.twitch.tv/easyallies)", 
           "Youtube" : "[YouTube](https://www.youtube.com/channel/UCZrxXp1reP8E353rZsB3jaA)",
					 "Patreon" : "[Patreon](https://www.patreon.com/EasyAllies)"}

TZFMT = "%Y-%m-%d %H:%M %Z"
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

@bot.command()
async def schedule(ctx, tz = None):
	tmp = await ctx.send('Fetching Schedule...')
	with urllib.request.urlopen(EZAPI) as response:
		data = response.read()

	if data is None:
		await ctx.send('Failed to fetch schedule.')
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
			if timeTo.days < 3 and timeTo.days >= 0:
				upcoming += "**{}**: {} {}\n".format(event["title"], time.strftime(TZFMT) , serviceStr)

	em = discord.Embed(title='Upcoming events.', color=0xbe0121, description = upcoming)
	await tmp.edit(content="Schedule loaded.", embed=em)

@bot.command()
async def update(ctx):
	pytz_tz = pytz_dict.get_dict()
	await ctx.send('Internal data updated.')
	
bot.run(sys.argv[1])
