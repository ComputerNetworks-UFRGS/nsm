# accuracy.gnu
reset

set term pdf enhanced
set datafile separator ";"

set key center top
set key outside horizontal

set grid
set xtics scale 0 
set output 'qualitative_accuracy.pdf'

set auto x
set yrange [0:110]
set xtics 5

set style fill solid border -1

set ylabel "Anomalies [%]"
set xlabel "Customers"

#set xtics ("5" 1, "10" 2, "20" 3, "40" 4)
set xtics offset 1 

#set logscale x 2

num_of_categories=3
set boxwidth 5.9/num_of_categories
dx=5.9/num_of_categories
offset=-0.1

plot 'entropy.csv' using ($1+offset):($3+$4) title "Generated" linecolor rgb "#808080" with boxes, \
	'' using ($1+offset):3 title "Detected" linecolor rgb "grey" with boxes, \
	'' using ($1+offset):($3+$4+5):2 notitle with labels, \
	'merged.csv' using ($1+offset+dx):($3+$4) notitle linecolor rgb "#808080" with boxes, \
	'' using ($1+offset+dx):3 notitle linecolor rgb "grey" with boxes, \
	'' using ($1+offset+dx):($3+$4+5):2 notitle with labels, \
	'entropy.csv' using ($1+offset):3 smooth csplines title "O accuracy" lw 3 lc rgb "black" with lines, \
	'merged.csv' using ($1+offset+dx):3 title "M accuracy" dashtype "_" lw 3 lc rgb "black" with lines, \
