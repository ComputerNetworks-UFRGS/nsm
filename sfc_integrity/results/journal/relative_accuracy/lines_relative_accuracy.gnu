# accuracy.gnu
reset

set term pdf enhanced
set datafile separator ";"

set key center top
set key outside horizontal

set grid
set xtics scale 0 
set output 'lines_relative_accuracy.pdf'

set auto x
set yrange [0:110]
set xtics 5
set xrange [0:45]

set style fill solid border -1

set ylabel "Anomalies [%]"
set xlabel "Number of Customers"

#set xtics ("5" 1, "10" 2, "20" 3, "40" 4)
#set xtics offset 1 

#set logscale x 2

num_of_categories=3
set boxwidth 5/num_of_categories
dx=5/num_of_categories
offset=-0.1

plot 'entropy.csv' using ($1+offset):3 title "SED accuracy" lw 3 lc rgb "black" with linespoints, \
	'merged.csv' using ($1+offset):3 title "MED accuracy" dashtype "." lw 3 lc rgb "black" with linespoints, \
	'mean.csv' using ($1+offset):3 title "NED accuracy" dashtype "-" lw 3 lc rgb "black" with linespoints, \
