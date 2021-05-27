#!/bin/bash

export vaxType="SpreadingVax"
outer=0
while [ $outer -lt 25 ]
do
count=1
while [ $count -le 40 ]
do
	echo $count $vaxType
	python3 getData.py $(( 40*$outer + $count )) $vaxType &
	((count++))
done
wait
echo "outer Loop $outer done"
((outer++))
wait
done
echo All done
