# Process-Management-and-Mining---Project
Implementation of the "Addressing the Log Representativeness Problem using Species Discovery" paper

In this project, we chose to implement and recreate the first algorithm proposed by this paper, using the same conditions described in the paper. 
Additionally, we selected the Sepsis dataset (Sepsis Cases-Event Log.xes) to test our algorithm. 
Our idea, was to recreate the results of the last row (corresponding to the Sepsis Log) in the table from the paper (page 6).
Therefore, we implemented all the zeta functions that allow us to define our "species" as described in the paper (zeta_tv - trace variants, zeta_act - activities, zeta_df - direct-follows relations, zeta_t1 - uniform one minute duration, zeta_t5 - uniform 5 minutes durations, zeta_t30 - uniform half-hour duration, zeta_te2 - exponential duration). 
We also created multiple functions to calculate the expected results, such as calculate_S_est, calculate_Q1, etc. 
Finally, we calculated the lg function applied to several values of g, using the same values as in the paper (g= 0.8, 0.9, 0.95, 0.99).

How to run our code ?




Comments:
