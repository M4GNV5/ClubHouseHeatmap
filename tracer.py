import time, md5, datetime, json
from fritzconnection.fritzwlan import FritzWLAN

config = False
with open("./config.json", "r") as fd:
	config = json.load(fd)

conn = FritzWLAN(user=config["username"], password=config["password"])
log = open(config["logfile"], "a")
activeDevices = []

log.write("RESET\n")

while True:

	hosts = []

	for i in range(1, config["serviceCount"] + 1):
		conn.service = str(i)
		hosts.append(conn.get_hosts_info())

	for index, host in enumerate(hosts):
		host = host[0]

		if host["mac"] in activeDevices:
			continue

		activeDevices.append(host["mac"])

		text = ""
		if config["privacy"] == "none":
			text = host["mac"]
		elif config["privacy"] == "anon":
		 	digest = md5.new()
			digest.update(host["mac"])
			text = digest.hexdigest()
		else: #full
			text = ""

		log.write("%s + %s\n" % (datetime.datetime.now().strftime(config["timeFormat"]), text))


	time.sleep(config["refreshTime"])
