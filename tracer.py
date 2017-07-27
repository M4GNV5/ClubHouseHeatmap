import time, md5, datetime, json
from fritzconnection.fritzhosts import FritzHosts

with open("./config.json", "r") as fd:
	config = json.load(fd)

conn = FritzHosts(user=config["username"], password=config["password"])
log = open(config["logfile"], "a")
activeDevices = []

log.write("%s RESET\n" % (datetime.datetime.now().strftime(config["timeFormat"])))
log.flush()

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

	start = datetime.datetime.now()

	_activeDevices = []
	hosts = conn.get_hosts_info()
	now = datetime.datetime.now().strftime(config["timeFormat"])

	for host in hosts:
		if host["status"] == "0" or host["mac"] in config["blacklist"]:
			continue

		_activeDevices.append(host["mac"])

		if host["mac"] in activeDevices:
			activeDevices.remove(host["mac"])
			continue

		log.write("%s + %s\n" % (now, anonymizeMac(host["mac"])))
		log.flush()

	for mac in activeDevices:
		log.write("%s - %s\n" % (now, anonymizeMac(mac)))

	if len(activeDevices) > 0:
		log.flush()

	activeDevices = _activeDevices

	waitTime = config["refreshTime"] - (datetime.datetime.now() - start).total_seconds()
	if waitTime > 0:
		time.sleep(waitTime)
