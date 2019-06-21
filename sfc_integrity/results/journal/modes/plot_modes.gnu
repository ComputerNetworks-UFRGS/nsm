# plot_time.gnuplot
reset

set term pdf enhanced
set datafile separator ";"

set key left top

set grid

#set logscale y 10 

set output 'plot_modes.pdf'
set yrange [0:30]
set xrange [0:12]

set style data histogram

set xlabel "Time [h]"
#set ylabel "Time []"

set ytics ("Anomalies" 5, "Events" 10, "Events Detection" 15, "Polling Analysis" 20, "Polling Detection" 25) 
set xtics 0,1,12

plot 5 with lines notitle lw 3 lc "black", 10 with lines notitle lw 3 lc "black", 15 with lines notitle lw 3 lc "black", 20 with lines notitle lw 3 lc "black", 25 with lines notitle lw 3 lc "black", \
	'anomalies.csv' with points notitle lw 3 pt 2 ps 1.5 lc "black", \
	'events.csv' with points notitle lw 3 pt 6 ps 1.5 lc "black", \
	'events_mode.csv' with points notitle lw 3 pt 7 ps 1.5 lc "black", \
	'polling.csv' with points notitle lw 3 pt 1 ps 1.5 lc "black", \
	'polling_mode.csv' with points notitle lw 3 ps 1.5 lc "black"
