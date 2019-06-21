# accuracy.gnu
reset

set term pdf enhanced
set datafile separator ";"

set key left top
set key outside horizontal

set grid
set xtics scale 0 
set output 'samples_size.pdf'

set auto x
set yrange [0:110]
set xtics 20 

set style fill solid border -1

set ylabel "Anomalies [%]"
set xlabel "Samples"

set xtics ("5" 1, "20" 20, "40" 40, "60" 60, "80" 80, "100" 100)
#set xtics offset 1 

#set logscale x 2

num_of_categories=3
set boxwidth 40/num_of_categories
dx=40/num_of_categories
offset=-0.1

plot 'mean.csv' using ($1+offset):($3+$4) title "Generated" linecolor rgb "#404040" with boxes, \
	'' using ($1+offset):($3+$5) title "Total detected" linecolor rgb "#808080" with boxes, \
	'' using ($1+offset):3 title "Actual anomalies" linecolor rgb "#778899" with boxes, \
	'' using ($1+offset):5 title "False-positives" linecolor rgb "grey" with boxes, \
	'' using ($1+offset):($3+$4+5):2 notitle with labels, \
	'mean.csv' using ($1+offset):3 smooth cspline title "Accuracy trend" lw 3 lc rgb "black" with lines, \
	'mean.csv' using ($1+offset):5 smooth cspline title "False-positives trend" dashtype "-" lw 3 lc rgb "black" with lines, \
