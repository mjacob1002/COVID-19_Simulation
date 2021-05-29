for vaxType in "StandardVax" "AgeVax" "MovementVax" "SpreadingVax"
do
	python3 prepData.py $vaxType 1.645
done
echo All Done
