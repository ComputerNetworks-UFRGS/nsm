# plot.gnu
reset

set style line 1 lw 4 lt 1 pt 1 linecolor rgb "black"
set style line 2 lw 4 lt 1 dashtype "-" pt 1 linecolor rgb "#646464"
set style line 3 lw 4 lt 2 pt 2 linecolor rgb "black"

set term pdf enhanced
set termoption dashed
set datafile separator ";"

set key left top

set grid

#set logscale y 10 

set output 'vnffg_150-450-add_vnfs.pdf'
#set yrange [0:10]
#set xrange [0:5.5]

set style data histogram

set xlabel "Analysis"
set ylabel "Entropy Value"

#set xtics ("[3,9,18]" 0, "[15,45,90]" 1, "[30,90,180]" 2, "[150,450,900]" 3, "[300,600,1800]" 4)

#set xtics rotate by 10 offset -5,-0.7

plot "vnffg_150-450-add_vnfs.csv" using 1 title "Cataloged" with steps ls 1, \
	 "vnffg_150-450-add_vnfs.csv" using 2 title "Monitored" with steps ls 2, \
	 "vnffg_150-450-add_vnfs.csv" using 2 notitle with points ls 3 

