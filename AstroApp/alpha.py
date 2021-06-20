import datetime as dt
from dateutil.tz import gettz
import geocoder
from astral import LocationInfo
from astral.sun import sun
from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart

from Utils.utils import cprint

from pprint import pprint


def get_suntime():
	"""

	:return:
	"""
	data = geocoder.ip('me').json
	data = data['raw']

	info = {
		'city_name': data['city'],
		'coord': {
			'lat': float(data['loc'].split(',')[0]),
			'lng': float(data['loc'].split(',')[1])
			},
		'tz': {
			'zone': data['timezone'],
			'GMT': gettz(data['timezone']).tzname(dt.datetime.now())
		}
	}

	city = LocationInfo(
		name=info['city_name'],
		timezone=info['tz']['zone'],
		latitude=info['coord']['lat'],
		longitude=info['coord']['lng']
	)

	sol = sun(
		city.observer,
		date=dt.datetime.today(),
		tzinfo=city.timezone
	)

	info['sun'] = {
		'dawn': sol['dawn'],
		'rise': sol['sunrise'],
		'noon': sol['noon'],
		'set': sol['sunset'],
		'dusk': sol['dusk']
	}

	return info


day_info = get_suntime()

# tuple with planetary regents sorted by their hourly regency
regents = (
	'Sun',
	'Venus',
	'Mercury',
	'Moon',
	'Saturn',
	'Jupiter',
	'Mars'
)

# dict with the correspondence of week day and the day's regent
# (from the regent tuple)
days_regents = {
	6: 0,  # sunday: sun
	0: 3,  # monday: moon
	1: 6,  # tuesday: mars
	2: 2,  # wednesday: mercury
	3: 5,  # thursday: jupiter
	4: 1,  # friday: venus
	5: 4   # saturday: saturn
}

now = dt.datetime.now(tz=gettz(day_info['tz']['zone']))  # fetching current
# datetime
today = now.weekday()  # fetching current week day


def show_hours(sunrise, sunset):
	"""
	Calculates the length of the current day and night astrological hours
	based on the sunrise and sunset, then prints each hour with it's
	corresponding index and correct regent, highlighting the current hour and
	regent.

	:param sunrise: sunrise datetime
	:param sunset: sunset datetime
	:return: None
	"""

	_time = sunrise  # time starts at sunrise
	_idx = 1  # first our of the day
	_regent_idx = days_regents[today]  # gets the day's regent

	day_time = sunset - sunrise  # day's length
	night_time = (sunrise + dt.timedelta(days=1)) - sunset  # night's length

	day_hour = day_time / 12
	night_hour = night_time / 12

	# loops from current sunrise until next day's sunrise
	while _time < (sunrise + dt.timedelta(days=1)):

		# sets current hour duration
		time_delta = day_hour if (_time + dt.timedelta(seconds=1)) < sunset \
			else night_hour

		# formats time information as a string
		time_str = f'{_time.hour:0>2}:{_time.minute:0>2}:{_time.second:0>2}.' \
			f'{_time.microsecond // 10000:0>2}'

		day_regent = regents[_regent_idx]  # hour regent
		# checks if current time is within astrological hour, and chooses color
		color = 'CYAN' if _time <= now < _time + time_delta else 'HEADER'

		cprint(f'{_idx:0>2} | {time_str} | {day_regent}', clr=color)

		# moves to the next hour
		_time += time_delta
		_idx += 1 if _idx < 12 else -11  # resets the hour index after 12 hours
		_regent_idx += 1 if _regent_idx < 6 else -6  # resets the regents count


def chart(datetime, coord, gmt):
	day = f'{datetime.year}/{datetime.month}/{datetime.day}'
	time = f'{datetime.hour}:{datetime.minute}'

	date = Datetime(day, time, gmt)
	pos = GeoPos(coord['lat'], coord['lng'])

	_chart = Chart(date, pos, hsys=const.HOUSES_WHOLE_SIGN)
	positions = {}

	asc = _chart.get(const.ASC)
	mc = _chart.get(const.MC)

	houses = [
		_chart.get(const.HOUSE1), _chart.get(const.HOUSE2),
		_chart.get(const.HOUSE3), _chart.get(const.HOUSE4),
		_chart.get(const.HOUSE5), _chart.get(const.HOUSE6),
		_chart.get(const.HOUSE7), _chart.get(const.HOUSE8),
		_chart.get(const.HOUSE9), _chart.get(const.HOUSE10),
		_chart.get(const.HOUSE11), _chart.get(const.HOUSE12)
	]

	for house in houses:
		positions.update({
			house.sign: {
				'house': house.id,
				'objects': []
			}
		})

		print(f'{house.id} in {house.sign}')

	positions[asc.sign]['objects'].append(asc.id)
	positions[mc.sign]['objects'].append(mc.id)

	print(
		f'{asc.id} in {asc.sign} at {angle.toString(asc.signlon)}\n'
		f'{mc.id} in {mc.sign} at {angle.toString(mc.signlon)}'
	)

	for obj in _chart.objects:
		positions[obj.sign]['objects'].append(obj.id)

		print(
			f'{obj.id} in {obj.sign} at '
			f'{angle.toString(obj.signlon)} | '
			f'{angle.toString(obj.lonspeed)}'
		)

	for sign, obj in positions.items():
		print(f'\n{sign} in {obj["house"]}')
		for ob in obj['objects']:
			print(f'\t{ob}')


if __name__ == '__main__':
	show_hours(
		sunrise=day_info['sun']['rise'],
		sunset=day_info['sun']['set']
	)
