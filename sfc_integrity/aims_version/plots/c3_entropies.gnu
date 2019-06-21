# plot.gnu
reset

set style line 1 lw 4 lt 1 pt 1 linecolor rgb "black"
set style line 2 lw 4 lt 2 pt 2 linecolor rgb "dark-grey"
set style line 3 lw 4 lt 3 pt 2 linecolor rgb "black"

set term pdf enhanced
set datafile separator ";"

set key left top

set grid

#set logscale y 10 

set output 'c3_entropies.pdf'
#set yrange [0:10]
#set xrange [0:5.5]

set style data histogram

set xlabel "Analysis"
set ylabel "Entropy Value"

#set xtics ("[3,9,18]" 0, "[15,45,90]" 1, "[30,90,180]" 2, "[150,450,900]" 3, "[300,600,1800]" 4)

#set xtics rotate by 10 offset -5,-0.7

plot "entropies_c3_only.txt" using 2 title "Merged C3" with steps ls 2, \
	 "entropies_c3_only.txt" using 1 title "Cataloged C3" with steps ls 1, \
	 "entropies_c3_only.txt" using 2 notitle with points ls 3  

