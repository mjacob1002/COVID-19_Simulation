#!/bin/bash

export vaxType="StandardVax"
outer=13
while [ $outer -lt 100 ]
do
count=1
while [ $count -le 10 ]
do
	echo $count $vaxType
	python3 getData.py $(( 10*$outer + $count )) $vaxType &
	((count++))
done
wait
echo "outer Loop $outer done"
((outer++))
wait
done
echo All done
