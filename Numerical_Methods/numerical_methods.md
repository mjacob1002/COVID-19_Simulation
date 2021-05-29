# Instructions

In order to impose a constraint on vaccines so that we can compare strategies, we must determine the p_0 value of the S(x) function for age, movement, and spreading radii strategies. We do this by using random simulation and then computing the average when S(x) is applied to that function at different p_0 values. 

Step 1: Go to the respective approx*.py file. For example, if you want to find the p0 value for a particular movement radius distribution, go to approx_p0_move_r.py file. Then change the mu and sigma to match the distribution that you are testing for. You may also change the .csv file names which the data is written to. Then run the file in the terminal with python3 <FILENAME>.

Step 2: After the data is saved, the run the regression.py file. The regression.py file has two arguments. The first is the name of the .csv file which the data retrieved from Step 1 is located. The second is the name of the file that you want the errors and testing of the regression model to be written to. When passing in these two arguments, run the file and an equation will output to the terminal. That is the equation for the average S(x) value as a function of p_0, which is called x. Then, isolate p_0 and get the equation for p_0 in terms of the average 
S(x), which will be the eta value used in the control strategy.