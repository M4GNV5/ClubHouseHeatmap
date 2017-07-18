## ClubHouseHeatmap

Generate a heatmap similar to the ['stats' page at bytewerk.org](http://stats.bytewerk.org/) by tracking connections to the Fritz!Box Router.

## Config

- `username`: Fritz!Box user
- `password`: the users password
- `logfile`: file to log network changes to
- `privacy`:
	- `none`: mac addresses are logged
	- `anon`: md5 of the mac addresses are logged
	- `full`: (default) no identification is logged
- `timeFormat`: a format string for strftime defining the timestamp format in the log
- `serviceCount`: amount of wlan devices the Fritz!Box has (usually 2 with 5GHz wlan, 1 without)
- `refreshTime`: timeout between each connection check
