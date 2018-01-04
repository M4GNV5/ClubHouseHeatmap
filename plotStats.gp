set terminal svg enhanced size 1500 500

#border and grid
set border 31 linewidth .7
set style line 102 lc rgb '#d6d7d9' lt 0 lw 1
set grid back ls 102

#title and legend
set title font ", 38"
set title "" offset 0,-6
set key font ", 18"
set key left top

#axis labels
set xlabel "Zeit (h)"
set ylabel "# Geräte"
set xlabel font ", 18"
set ylabel font ", 18"

#axis descriptions
stats [0:] "stats.dat" using 3:4
minY=STATS_min_x < STATS_min_y ? STATS_min_x : STATS_min_y
maxY=STATS_max_x > STATS_max_y ? STATS_max_x : STATS_max_y

set xrange [0:23]
set yrange [minY - 0.3:maxY + 0.3]
set xtics 0, 1, 24 font ", 18"
set ytics font ", 18"

dayNames="Montag Dienstag Mittwoch Donnerstag Freitag Samstag Sonntag"

#plotting
do for [day=1:7] {
	set output sprintf("plots/day%d.svg", day)
	set title word(dayNames, day)
	start=(day - 1) * 24
	end=day * 24 + 1
	plot "stats.dat" every ::start::end using 0:3 smooth csplines title "Durchschnitt", \
		"stats.dat" every ::start::end using 0:4 with lines title "Logins"
}
