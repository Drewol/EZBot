import pytz
from datetime import datetime

def get_dict():
	fmt = "%Z"
	ret = {}
	for tz in pytz.all_timezones:
		#Winter
		dat = datetime(2000,1,1)
		dat = dat.replace(tzinfo=pytz.utc)
		dat = dat.astimezone(pytz.timezone(tz))
		ret[dat.strftime(fmt)] = pytz.timezone(tz)
		
		#Summer
		dat = datetime(2000,6,16)
		dat = dat.replace(tzinfo=pytz.utc)
		dat = dat.astimezone(pytz.timezone(tz))
		ret[dat.strftime(fmt)] = pytz.timezone(tz)
	return ret