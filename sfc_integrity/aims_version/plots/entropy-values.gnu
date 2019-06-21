# plot.gnu
reset

set style line 1 lw 2 lt 1 pt 1 linecolor rgb "black"
set style line 2 lw 2 lt 2 pt 3 linecolor rgb "black"
set style line 3 lw 2 lt 3 pt 3 linecolor rgb "#eff3ff" # very light blue
set style line 4 lw 2 lt 4 pt 4 linecolor rgb "#bdd7e7" # light blue
set style line 5 lw 2 lt 5 pt 5 linecolor rgb "#6baed6" # blue
set style line 6 lw 2 lt 6 pt 6 linecolor rgb "#3182bd" # dark blue
set style line 7 lw 2 lt 7 pt 7 linecolor rgb "#08519c" # very dark blue


set term pdf enhanced
set datafile separator ";"

set key right top

set grid

#set logscale y 10 

set output 'entropies.pdf'
#set yrange [0:10]
#set xrange [0:5.5]

set style data histogram

set xlabel "Analysis"
set ylabel "Entropy Value"

#set xtics ("[3,9,18]" 0, "[15,45,90]" 1, "[30,90,180]" 2, "[150,450,900]" 3, "[300,600,1800]" 4)

#set xtics rotate by 10 offset -5,-0.7

plot "entropies_c1.txt" using 2 title "Merged C1" with steps ls 4, \
	 "entropies_c1.txt" using 1 title "Cataloged C1" with steps ls 1, \
	 "entropies_c1.txt" using 2 notitle with points ls 2, \
	 "entropies_c2.txt" using 2 title "Merged C2" with steps ls 5, \
	 "entropies_c2.txt" using 1 title "Cataloged C2" with steps ls 1, \
	 "entropies_c2.txt" using 2 notitle with points ls 2, \
	 "entropies_c3.txt" using 2 title "Merged C3" with steps ls 6, \
	 "entropies_c3.txt" using 1 title "Cataloged C3" with steps ls 1, \
	 "entropies_c3.txt" using 2 notitle with points ls 2, \
	 "entropies_c4.txt" using 2 title "Merged C4" with steps ls 7, \
	 "entropies_c4.txt" using 1 title "Cataloged C4" with steps ls 1, \
	 "entropies_c4.txt" using 2 notitle with points ls 2  

