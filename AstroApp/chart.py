import inspect
from pprint import pprint

from flatlib import const
from flatlib import angle
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart

from alpha import now, day_info
from Utils.utils import cprint
from datetime import datetime as dt


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

	positions[asc.sign]['objects'].append(asc)
	positions[mc.sign]['objects'].append(mc)

	for obj in _chart.objects:
		positions[obj.sign]['objects'].append(obj)

	for sign, obj in positions.items():
		print(f'\n{sign} in {obj["house"]}')
		for ob in obj['objects']:
			print(f'\t{ob.id} at {angle.toString(ob.signlon)}')


class CurrentChart(Chart):
	def __init__(self, datetime, pos, gmt):
		day = f'{datetime.year}/{datetime.month}/{datetime.day}'
		time = f'{datetime.hour}:{datetime.minute}'
		date = Datetime(day, time, gmt)

		pos = GeoPos(pos['lat'], pos['lng'])

		super().__init__(date, pos, hsys=const.HOUSES_WHOLE_SIGN)

		self.asc = self.get(const.ASC)
		self.mc = self.get(const.MC)

		self.houses = [
			self.get(const.HOUSE1), self.get(const.HOUSE2),
			self.get(const.HOUSE3), self.get(const.HOUSE4),
			self.get(const.HOUSE5), self.get(const.HOUSE6),
			self.get(const.HOUSE7), self.get(const.HOUSE8),
			self.get(const.HOUSE9), self.get(const.HOUSE10),
			self.get(const.HOUSE11), self.get(const.HOUSE12)
		]

		self.position = self.get_positions()

	def get_positions(self):
		data = {}

		for house in self.houses:
			data.update({
				house.sign: {
					'house': house.id,
					'objects': []
				}
			})

		data[self.asc.sign]['objects'].append(self.asc)
		data[self.mc.sign]['objects'].append(self.mc)

		for obj in self.objects:
			data[obj.sign]['objects'].append(obj)

		return data

	def draw_chart(self):
		for sign, obj in self.position.items():
			chart_color = 'BLUE'
			cprint('=' * 52, color=chart_color)
			cprint(f'{obj["house"]} in {sign}', color=chart_color)
			for ob in obj['objects']:
				print(f'|\t{ob.id} at {angle.toString(ob.signlon)}', end=' ')

				try:
					print(f'{ob.movement()} {angle.toString(ob.lonspeed)}')

				except AttributeError:
					print()


if __name__ == '__main__':
	date = '06/04/21 18:00:00'
	date = dt.strptime(date, '%m/%d/%y %H:%M:%S')

	my_chart = CurrentChart(
		datetime=date,
		pos=day_info['coord'],
		gmt=day_info['tz']['GMT']
	)

	my_chart.draw_chart()
