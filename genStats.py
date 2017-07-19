import sys, datetime, json
from dateutil.parser import parse as parseDate

if len(sys.argv) != 2:
	print "Usage: python %s <logfile>" % sys.argv[0]
	exit()



average = []
averageCount = []
averageIndex = 0
online = 0
maxOnline = 0
timeBorder = None

for i in range(0, 7 * 24):
	average.append(None)
	averageCount.append(0)



def roundTime(dt, roundUp, amount = 60 * 60):
	seconds = (dt.replace(tzinfo=None) - dt.min).seconds
	rounding = (seconds + amount / 2) // amount * amount

	if roundUp:
		rounding = rounding + amount

	return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)

def fillData():
	global averageIndex, maxOnline, timeBorder
	_averageIndex = timestamp.weekday() * 24 + timestamp.hour

	while averageIndex != _averageIndex:
		if average[averageIndex] == None:
			average[averageIndex] = maxOnline
		else:
			average[averageIndex] += maxOnline

		averageCount[averageIndex] += 1

		averageIndex += 1
		if averageIndex == 7 * 24:
			averageIndex = 0



with open(sys.argv[1], "r") as log:
	line = log.readline()[:-1].split(" ")
	timestamp = parseDate(line[0])
	timeBorder = roundTime(timestamp, True)
	averageIndex = timestamp.weekday() * 24 + timestamp.hour

	if line[1] != "RESET":
		print "WARN: First line is not a RESET line"

	for line in log:
		line = line[:-1].split(" ")
		timestamp = parseDate(line[0])

		if line[1] == "RESET":
			online = 0
		elif line[1] == "+":
			online += 1
		elif line[1] == "-":
			online -= 1
		else:
			print "Invalid line %s" % " ".join(line)

		if timestamp > timeBorder:
			fillData()
			timeBorder = roundTime(timestamp, True)
			maxOnline = online

		if online > maxOnline:
			maxOnline = online



fillData()

for i in range(0, 7 * 24):
	if averageCount[i] != 0:
		average[i] /= averageCount[i]

print json.dumps(average)
