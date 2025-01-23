set terminal pdfcairo font "Helvetica,18"
set output "signal_asset_growth.pdf"
unset key
set xrange [0:0.32]
set xlabel "{/Symbol a}"
set yrange [0:1.0]
set ylabel "{/Symbol b}"
p "asset_growth_fat_tailed.dat"        pt 7 ps 1 lc "red"\
, "asset_growth_not_fat_tailed.dat"    pt 2 ps 1 lc "blue"\
, "asset_growth_step.dat" pt 7 ps 1 lc "green"
