#!/bin/bash

count=311
export vaxType="StandardVax"
while [ $count -le 312 ]
do
	echo $count $vaxType
	python3 getData.py $count $vaxType &
	((count++))
done
echo All done
