set terminal pdfcairo dashed font "Helvetica,16"
set output "append.pdf"
set xlabel "List length (millions)"  textcolor rgbcolor "yellow"
set ylabel "Elapsed time"  textcolor rgbcolor "yellow"
set border 15 linecolor rgbcolor "yellow"
set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"black" behind

plot "append.out" using ($2/1000000):1 w l lw 3 lc "#ff0000" notitle
