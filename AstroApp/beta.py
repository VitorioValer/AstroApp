import geocoder
import datetime as dt
from dateutil.tz import gettz
from astral import LocationInfo
from astral.sun import sun

from Utils.utils import cprint
from constants import regents, days_regents
from chart import CurrentChart

# ------------------------------------------------------------------------------
from pprint import pprint
import inspect
# ------------------------------------------------------------------------------


class Day:
	def __init__(self):
		_pos_data = geocoder.ip('me').json['raw']

		self.city = _pos_data['city']
		self.coord = {
			'lat': float(_pos_data['loc'].split(',')[0]),
			'lng': float(_pos_data['loc'].split(',')[1])
		}

		self.tz = {
			'zone': _pos_data['timezone'],
			'file': gettz(_pos_data['timezone']),
		}

		self.now = dt.datetime.now(self.tz['file'])
		self.today = self.now.weekday()

		self.tz['GMT'] = self.tz['file'].tzname(self.now)

		self.sun = self.solar_info()
		self.day_hour, self.night_hour = self.day_duration()
		self.hours = []
		self.calculate_hours()

	def solar_info(self):
		city = LocationInfo(
			name=self.city,
			timezone=self.tz['zone'],
			latitude=self.coord['lat'],
			longitude=self.coord['lng']
		)

		sol = sun(
			observer=city.observer,
			date=dt.datetime.now(),
			tzinfo=city.timezone
		)

		return {
			'dawn': sol['dawn'],
			'rise': sol['sunrise'],
			'noon': sol['noon'],
			'set': sol['sunset'],
			'dusk': sol['dusk']
		}

	def day_duration(self):
		day_len = self.sun['set'] - self.sun['rise']
		night_len = (self.sun['rise'] + dt.timedelta(days=1)) - self.sun['set']

		return day_len / 12, night_len / 12

	def calculate_hours(self):
		time = self.sun['rise']
		idx = 1
		regent_idx = days_regents[self.today]

		while time < (self.sun['rise'] + dt.timedelta(days=1)):
			time_delta = self.day_hour if (time + dt.timedelta(seconds=1)) < \
							self.sun['set'] else self.night_hour

			self.hours.append(self.AstrologicalHour(
				time=time,
				idx=idx,
				regent=regents[regent_idx],
				is_current_hour=True if time <= self.now
				< time + time_delta else False
			))

			time += time_delta
			idx += 1 if idx < 12 else -11
			regent_idx += 1 if regent_idx < 6 else -6

	class AstrologicalHour:
		def __init__(self, time, idx, regent, is_current_hour):
			self.time = time
			self.idx = idx
			self.regent = regent
			self.is_current_hour = is_current_hour

			self.strtime = f'{time.hour:0>2}:{time.minute:0>2}:' \
				f'{time.second:0>2}.{time.microsecond // 10000:0>2}'

		def __str__(self):
			return f'{self.idx:0>2} | {self.strtime} | {self.regent}'


if __name__ == '__main__':
	today = Day()

	current_chart = CurrentChart(
		datetime=today.now,
		pos=today.coord,
		gmt=today.tz['GMT']
	)

	for h in today.hours:
		clr = 'CYAN' if h.is_current_hour else 'HEADER'

		cprint(h, clr)

	current_chart.draw_chart()
