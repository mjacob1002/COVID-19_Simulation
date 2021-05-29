#!/bin/bash

for vaxType in "NoVax"
do
outer=0
while [ $outer -lt 25 ]
do
count=1
while [ $count -le 40 ]
do
	echo $(( 40*$outer + $count )) $vaxType
	python3 getData.py $(( 40*$outer + $count )) $vaxType &
	((count++))
done
wait
echo "outer Loop $outer done"
((outer++))
wait
done
echo Done with $vaxType
done
echo All done
