import sys, datetime, json
from dateutil.parser import parse as parseDate

if len(sys.argv) != 3:
	print "Usage: python %s <logfile> <datafile>" % sys.argv[0]
	exit()

minima = []
maxima = []
average = []
averageCount = []
activity = []
activityCount = []
dataIndex = 0
online = 0
maxOnline = 0
onlineChange = 0
lastTimestamp = None

for i in range(0, 7 * 24):
	minima.append(9000)
	maxima.append(0)
	average.append(0)
	averageCount.append(0)
	activity.append(0)
	activityCount.append(0)



def roundTime(dt, roundUp, amount = 60 * 60):
	seconds = (dt.replace(tzinfo=None) - dt.min).seconds
	rounding = (seconds + amount / 2) // amount * amount

	if roundUp:
		rounding = rounding + amount

	return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)

def fillData():
	global dataIndex, maxOnline, timestamp, lastTimestamp
	_dataIndex = timestamp.weekday() * 24 + timestamp.hour

	times = 1 + timestamp.isocalendar()[1] - lastTimestamp.isocalendar()[1]
	lastTimestamp = timestamp

	if onlineChange > 2 or onlineChange < -2:
		activity[dataIndex] += onlineChange
	activityCount[dataIndex] += 1

	while times > 0 or dataIndex != _dataIndex:
		minima[dataIndex] = min(minima[dataIndex], maxOnline)
		maxima[dataIndex] = max(maxima[dataIndex], maxOnline)
		average[dataIndex] += maxOnline
		averageCount[dataIndex] += 1

		dataIndex += 1
		if dataIndex == 7 * 24:
			dataIndex = 0

		if dataIndex == _dataIndex:
			times = times - 1



with open(sys.argv[1], "r") as log:
	line = log.readline()[:-1].split(" ")
	timestamp = parseDate(line[0])
	lastTimestamp = timestamp
	timeBorder = roundTime(timestamp, True)
	dataIndex = timestamp.weekday() * 24 + timestamp.hour

	if line[1] != "RESET":
		print "WARN: First line is not a RESET line"

	for line in log:
		line = line[:-1].split(" ")
		timestamp = parseDate(line[0])

		if line[1] == "RESET":
			online = 0
		elif line[1] == "+":
			online += 1
			onlineChange += 1
		elif line[1] == "-":
			online -= 1
			onlineChange -= 1
		else:
			print "Invalid line %s" % " ".join(line)

		if timestamp > timeBorder:
			fillData()
			timeBorder = roundTime(timestamp, True)
			maxOnline = online
			onlineChange = 0

		if online > maxOnline:
			maxOnline = online



fillData()

with open(sys.argv[2], "w") as output:
	for i in range(0, 7 * 24):
		if averageCount[i] != 0:
			average[i] /= float(averageCount[i])
		if activityCount[i] != 0:
			activity[i] /= float(activityCount[i])
		output.write("%d %d %g %g\n" % (minima[i], maxima[i], average[i], activity[i]))
