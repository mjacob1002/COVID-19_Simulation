# COVID-19_Simulation
COVID-19 RxCovea project

# Setting up

Clone this repo into a separate directory. Delete all of the files in the Aggregate/* and Outputs/* subdirectories. 

# Example

Depending on the vaccination strategy that is wanted to be run, change the variable in the runloop.sh file called vaxType to match the directory name corresponding to the vaccination strategy type being simulated. For example, if I wanted to run an AgeVax simulation, I'd set:
```shell
export vaxType="AgeVax"
```
Additionally, count represents the number used in the name when generating the "out" csv files stored in Outputs subdirectories. You can modify the number of files by changing the number in the while loop in the script. 
