set terminal pdfcairo enhanced font "Helvetica,18"
set log y
set log x
set format xy "10^{%T}"
set xrange [1e-3:10]
set yrange [1e-3:1]
set key left bottom
set style data lines

set output "return_survival.pdf"
p 'price_a012_b01.dat' using 1:2 with line lw 4 lc rgb 'blue' title "price", \
  'price_a012_b01.dat' using 3:4 with line lw 4 lc rgb 'red' title 'N(0, 1)'
