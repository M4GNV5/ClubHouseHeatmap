<html>
	<body>
		<div style="text-align: center;">
			<p>
				Der Graph zeigt die Durschnittliche Anzahl an Geräten die mit dem
				Router im Vereinsheim des Bürgernetz Landkreis Pfaffenhofen
				verbunden sind, sowie für jede Stunde wie viele Geräte sich im
				Schnitt an- bzw. abmelden.
			</p>

			<?php
				if(isset($_GET["day"]))
					$day = $_GET["day"];
				else
					$day = date("w") == 0 ? 7 : date("w");

				if($day == "all")
				{
					for($i = 1; $i <= 7; $i++)
					{
						echo("<img src=\"day$i.svg\" /><hr />");
					}
				}
				else
				{
					$day = (int)$day;
					if($day < 1 || $day > 7)
						$day = 1;

					echo("<img src=\"day$day.svg\" />");
				}
			?>

			<br />

			<p class="text">
				<a href="?day=1">Montag</a>
				<a href="?day=2">Dienstag</a>
				<a href="?day=3">Mittwoch</a>
				<a href="?day=4">Donnerstag</a>
				<a href="?day=5">Freitag</a>
				<a href="?day=6">Samstag</a>
				<a href="?day=7">Sonntag</a>
				<br />
				<a href="?">Heute</a>
				<a href="?day=all">Alle</a>
				<br />
				<a href="https://github.com/M4GNV5/ClubHouseHeatmap" target="_blank">Source Code</a>
			</p>
		</div>
	</body>
</html>
