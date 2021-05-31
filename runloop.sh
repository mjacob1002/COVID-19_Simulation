#!/bin/bash

total_loops=0
for vaxType in "NoVax" "StandardVax" "AgeVax" "MovementVax" "SpreadingVax"
do
outer=0
while [ $outer -lt 21 ]
do
count=1
while [ $count -le 48 ]
do
	if [ $total_loops == 1001 ]
	then
		echo All done
		exit 0
	fi
	echo $(( 48*$outer + $count )) $vaxType
	python3 getData.py $(( 48*$outer + $count )) $vaxType &
	((count++))
	((total_loops++))
done
wait
echo "outer Loop $outer done"
((outer++))
wait
done
echo Done with $vaxType
done
echo All done
