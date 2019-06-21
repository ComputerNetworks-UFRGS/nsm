# plot_time.gnuplot
reset

set style line 1 lw 4 lt 1 pt 1 linecolor rgb "black"
#set style line 2 lw 4 lt 2 pt 2 linecolor rgb "dark-grey"
set style line 2 lw 4 lt 1 dashtype "-" pt 1 linecolor rgb "#646464"
set style line 3 lw 4 lt 1 dashtype "." pt 1 linecolor rgb "#808080"
set style line 4 lw 4 lt 1 dashtype "_" pt 1 linecolor rgb "#black"

set term pdf enhanced
set datafile separator ";"

set key left top

set grid

#set logscale y 10 

set output 'plot_time.pdf'
#set yrange [0:0.07]
set xrange [0:7]

set style data histogram

set xlabel "Instances [SFC,VNF,VDU]"
set ylabel "Time [ms]"

set xtics ("[1,3,6]" 0, "[3,9,18]" 1, "[6,18,36]" 2, "[12,36,72]" 3, "[24,72,144]" 4, "[48,144,288]" 5, "[96,288,576]" 6, "[192,576,1152]" 7)

set xtics rotate by 15 offset -5,-1.2

set xlabel offset 0,-1

# values multiplied by 1000 to convert from seconds to milliseconds

plot "entropy_mean_std.csv" using ($1*1000):($2*1000) title "OE" with yerrorbars ls 1, \
		'' using ($1*1000) notitle with lines ls 1, \
		"merged_ent_mean_std.csv" using ($1*1000):($2*1000) title "ME" with yerrorbars ls 3, \
		'' using ($1*1000) notitle with lines ls 3, \
		"quant_ent_mean_std.csv" using ($1*1000):($2*1000) title "MS" with yerrorbars ls 4, \
		'' using ($1*1000) notitle with lines ls 4, \
		"comparison_mean_std.csv" using ($1*1000):($2*1000) title "n-to-n" with yerrorbars ls 2, \
		'' using ($1*1000) notitle with lines ls 2, \

