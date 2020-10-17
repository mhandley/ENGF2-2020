set terminal pdfcairo dashed font "Helvetica,16"
set output "del.pdf"
set xlabel "List length (thousands)"  textcolor rgbcolor "yellow"
set ylabel "Time to delete 100 items"  textcolor rgbcolor "yellow"
set border 15 linecolor rgbcolor "yellow"
set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb"black" behind

plot "del.out" using ($1/1000):2 w l lw 3 lc "#ff0000" notitle
