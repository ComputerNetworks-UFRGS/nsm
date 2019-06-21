# accuracy.gnu
reset

set term pdf enhanced
set datafile separator ";"

set key center top
set key outside horizontal

set grid
set xtics scale 0 
set output 'lines_sample_size.pdf'

set auto x
set yrange [0:110]
set xtics 20
set xrange [0:100]

set style fill solid border -1

set ylabel "Anomalies [%]"
set xlabel "Number of Samples"

set xtics ("5" 1, "20" 20, "40" 40, "60" 60, "80" 80, "100" 100)
#set xtics offset 1 

#set logscale x 2

num_of_categories=3
set boxwidth 40/num_of_categories
dx=40/num_of_categories
offset=-0.1

plot	'mean.csv' using ($1+offset):($3+$5) title "Total detected" lw 3 lc rgb "black" with linespoints, \
	'mean.csv' using ($1+offset):3 title "True-positives" dashtype "." lw 3 lc rgb "black" with linespoints, \
	'mean.csv' using ($1+offset):5 title "False-positives" dashtype "-" lw 3 lc rgb "black" with linespoints, \
