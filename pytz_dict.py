import pytz
from datetime import datetime

def get_dict():
	fmt = "%Z"
	ret = {}
	for tz in pytz.all_timezones:
		dat = datetime.utcnow()
		dat = dat.replace(tzinfo=pytz.utc)
		dat = dat.astimezone(pytz.timezone(tz))
		ret[dat.strftime(fmt)] = pytz.timezone(tz)
	return ret