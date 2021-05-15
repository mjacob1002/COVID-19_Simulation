# a script that gets the regression coefficients and intercepts in order to find the p0 value for the S(x) function such that it equals the eta value

# change this to whatever the file output of approx_p0.py is named
data_name="Approx_p0_vs_S(x)"

python3 approx_p0.py
python3 regression.py
