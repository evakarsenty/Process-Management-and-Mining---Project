# Process-Management-and-Mining---Project
Implementation of the "Addressing the Log Representativeness Problem using Species Discovery" paper

In this project, we chose to implement and recreate the first algorithm proposed by this paper, using the same conditions described in the paper. 
Additionally, we selected the Sepsis dataset (Sepsis Cases-Event Log.xes) to test our algorithm. 
Our idea, was to recreate the results of the last row (corresponding to the Sepsis Log) in the table from the paper (page 6).
Therefore, we implemented all the zeta functions that allow us to define our "species" as described in the paper (zeta_tv - trace variants, zeta_act - activities, zeta_df - direct-follows relations, zeta_t1 - uniform one minute duration, zeta_t5 - uniform 5 minutes durations, zeta_t30 - uniform half-hour duration, zeta_te2 - exponential duration). 
We also created multiple functions to calculate the expected results, such as calculate_S_est, calculate_Q1, etc. 
Finally, we calculated the lg function applied to several values of g, using the same values as in the paper (g= 0.8, 0.9, 0.95, 0.99).

# How to run our code ?

To run our code, simply download the Python file and the corresponding xes file for the data we used. 
Then, replace the `file_path_sepsis` variable in the main function of the Python file with your corresponding path to the data file. 
It's that simple!

Our code will print to you the number of cases for Sepsis Cases and the number of trace variants for Sepsis Cases, followed by the results table identical to the one obtained in the paper.

# Implementation details:

Although we followed the mathematical formulas outlined in the paper throughout our code, we observed that some of our results were not identical to those presented in the paper, although they were very similar. 
We therefore conducted extensive research into the reference papers they cited and discovered that some of the formulas in the paper were inaccurate. 
In fact, in the reference papers, we found variations of these formulas that, when applied to our data, produced results identical to those in the original paper. 
We then used the variations of the formulas found in the reference papers for the Chao2 estimator (used in the S_est calculations), as well as the Cov_obs calculations.
However, we still observe slight differences in our results that we have not been able to explain based on the reference papers, particularly when we deal with the zeta functions based on duration events.

Some details about the implementation of our code:
- For the zeta_tv and the zeta_df functions, we sort our log based on the case id and the timestamp in order to be consistent and to ensure that the events within each case are in chronological order
- For the zeta_df function, at the end and at the beggining of each case, we added a species defined as: (None, first action) or (last action, None)
- For the zeta functions based on duration of events we sort our log by the timestamp and we convert the duration of each event in minutes as specified in the paper
- In order to calculate the duration of each event, we calculate the difference in the timestamp values between the event in question and the event of the same case, that came right after
- For each of the zeta functions that are based on event durations, we compute the species value exactly as described by the corresponding mathematical formula in the paper
- For each zeta function that we implement, we added a column 'count' in order to have the number of apparition of each specie in our log
- We calculate the value of the lg function when the completness score obtained was below the threshold wished for , exactly as described by the corresponding mathematical formula in the paper
