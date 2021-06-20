from datetime import datetime as dt
from datetime import timedelta
from flatlib import angle
from chart import CurrentChart
from alpha import day_info

from pprint import pprint


def sniffer(starting_date, tracked_planet, end_sing=None, end_date=None):
	_date = starting_date
	tracking = True
	start_sign, prev_sign = None, None

	def looper(chrt):

		for sign, elements in chrt.position.items():
			for obj in elements['objects']:
				if obj.id == tracked_planet:
					return sign, obj.movement(), angle.toString(obj.signlon)

	while tracking:
		chart = CurrentChart(
					datetime=_date,
					pos=day_info['coord'],
					gmt=day_info['tz']['GMT']
				)

		current_sign, current_mov, pos = looper(chrt=chart)
		formatted_date = dt.strftime(_date, "%d/%m/%y")

		if _date == starting_date:
			start_sign = current_sign

			print(
				f'{tracked_planet} starts in {current_sign} at {formatted_date}'
				f' {pos}'
			)

		elif current_sign != prev_sign:
			print(
				f'{tracked_planet} moves to {current_sign} in {formatted_date}'
				f' {pos}'
			)

			if current_sign == end_sing or _date == end_date:
				tracking = False

			if current_sign == start_sign and current_mov == 'Direct':
				print('-=-'*10)
				print(
					f'{tracked_planet} has returned to initial position '
					f'(in {start_sign})'
				)

				resp = input(
					'press C to continue the cycles or press other any key '
					'to exit the program  '
				).strip().upper()

				print('-=-'*10)

				if resp == 'C':
					starting_date = _date
					continue

				tracking = False


		_date += timedelta(days=1)
		prev_sign = current_sign


if __name__ == '__main__':
	date = dt.strptime('09/30/93 14:20:00', '%m/%d/%y %H:%M:%S')
	planet = 'Saturn'

	sniffer(date, planet)
