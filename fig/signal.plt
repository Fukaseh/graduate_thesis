set terminal pdfcairo font "Helvetica,18"
set output "signal.pdf"
unset key
set xrange [0:0.32]
set xlabel "{/Symbol a}"
set yrange [0:1.0]
set ylabel "{/Symbol b}"
p "fat_tailed.dat"        pt 7 ps 1 lc "red"\
, "not_fat_tailed.dat"    pt 2 ps 1 lc "blue"\
, "step_distribution.dat" pt 7 ps 1 lc "green"
