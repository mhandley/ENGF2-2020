set terminal pdfcairo dashed font "Helvetica,16"
set output "access.pdf"
set xlabel "List length (thousands)"  textcolor rgbcolor "yellow"
set ylabel "Time to access 1000 items"  textcolor rgbcolor "yellow"
set border 15 linecolor rgbcolor "yellow"
set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"black" behind
set key bottom right textcolor rgbcolor "yellow"
set yrange [0:]
plot "access-start.out" using ($1/1000):2 w l lw 3 lc "#ff0000" title "Start", \
"access-mid.out" using ($1/1000):2 w l lw 3 lc "#ffa000" title "Middle", \
"access-end.out" using ($1/1000):2 w l lw 3 lc "#0000ff" title "End"
