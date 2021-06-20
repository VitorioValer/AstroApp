import datetime as dt

regents = (
	'Sun',
	'Venus',
	'Mercury',
	'Moon',
	'Saturn',
	'Jupiter',
	'Mars'
)

days_regents = {
	6: 0,  # sunday: sun
	0: 3,  # monday: moon
	1: 6,  # tuesday: mars
	2: 2,  # wednesday: mercury
	3: 5,  # thursday: jupiter
	4: 1,  # friday: venus
	5: 4   # saturday: saturn
}

now = dt.datetime.now()
