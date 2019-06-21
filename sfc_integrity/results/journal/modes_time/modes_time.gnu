# modes_time.gnu
reset

set style line 1 lt 1 dashtype 1 pt 1 lc rgb "black" lw 2
set style line 2 lt 1 dashtype 2 pt 2 lc rgb "black" lw 2
set style line 3 lt 1 dashtype 3 pt 4 lc rgb "black" lw 2
set style line 4 lt 1 dashtype 4 pt 5 lc rgb "black" lw 2

set term pdf enhanced
set datafile separator ";"

set key center top
set key outside horizontal

#set grid
set xtics scale 0 
set output 'modes_time.pdf'

set yrange [0:60]
set y2range [0:10]
set y2tics
set ytics nomirror #remove mirrored tics on the right side

set ylabel "Polling Interval [min]"
set xlabel "Time to detect [min]"
set y2label "Events/hour"

plot 	"polling.dat" using 2:1 notitle axes x1y1 with lines ls 2, \
		'' using 2:1:3 title "Polling-based mode" with yerrorbars ls 2, \
		"events.dat" using 2:1 notitle axes x1y2 with lines ls 1, \
		'' using 2:1:3 title "Event-based mode" axes x1y2 with yerrorbars ls 1, \
		#"polling_50.dat" using 2:1 title "Polling-based mode (50)" axes x1y1 with linespoints ls 4, \

