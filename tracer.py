import time, md5, datetime, json
from fritzconnection.fritzwlan import FritzWLAN

with open("./config.json", "r") as fd:
	config = json.load(fd)

conn = FritzWLAN(user=config["username"], password=config["password"])
log = open(config["logfile"], "a")
activeDevices = []

log.write("%s RESET\n" % (datetime.datetime.now().strftime(config["timeFormat"])))

def anonymizeMac(mac):
	if config["privacy"] == "none":
		return mac
	elif config["privacy"] == "anon":
		digest = md5.new()
		digest.update(mac)
		return digest.hexdigest()
	else: #full
		return ""

while True:

	hosts = []
	for i in range(1, config["serviceCount"] + 1):
		conn.service = str(i)
		hosts.extend(conn.get_hosts_info())

	now = datetime.datetime.now().strftime(config["timeFormat"])
	_activeDevices = []

	for host in hosts:
		_activeDevices.append(host["mac"])

		if host["mac"] in activeDevices:
			index = activeDevices.index(host["mac"])
			del activeDevices[index]
			continue

		log.write("%s + %s\n" % (now, anonymizeMac(host["mac"])))

	for mac in activeDevices:
		log.write("%s - %s\n" % (now, anonymizeMac(mac)))

	activeDevices = _activeDevices
	time.sleep(config["refreshTime"])
