set terminal pdfcairo enhanced font "Helvetica,18"
set log y
set log x
set format xy "10^{%T}"
set xrange [1e-3:10]
set yrange [1e-3:1]
set key left bottom
set style data lines

set output "asset_brown.pdf"
set label "(b)" at 1.5, 0.7
p 'asset_a003_b01.dat' using 1:2 with line lw 4 lc rgb 'blue' title "asset", \
  'asset_a003_b01.dat' using 3:4 with line lw 4 lc rgb 'red' title 'N(0, 1)'

unset label

set output "asset_growth_brown.pdf"
set label "(a)" at 1.5, 0.7
p 'asset_growth_a003_b01.dat' using 1:2 with line lw 4 lc rgb 'blue' title "asset growth", \
  'asset_growth_a003_b01.dat' using 3:4 with line lw 4 lc rgb 'red' title 'N(0, 1)'

unset label
set output "price_brown.pdf"
set label "(c)" at 1.5, 0.7
p 'price_a003_b01.dat' using 1:2 with line lw 4 lc rgb 'blue' title "price", \
  'price_a003_b01.dat' using 3:4 with line lw 4 lc rgb 'red' title 'N(0, 1)'

