########## SOLUTION ##########
QUERY Burglary
EVIDENCE JohnCalls t MaryCalls t
QUERY_DIST t 0.284 f 0.716
########## STEPS ##########

VARIABLES TO ELIMINATE:
Earthquake Alarm

========== ITERATION 1 ==========

ELIMINATING VAR: Earthquake

>> SET OF FACTORS (tabular form):

FACTOR 1
VARS: MaryCalls Alarm
CPT:
t t 0.7
t f 0.01
f t 0.3
f f 0.99

FACTOR 2
VARS: Earthquake
CPT:
t 0.002
f 0.998

FACTOR 3
VARS: Burglary
CPT:
t 0.001
f 0.999

FACTOR 4
VARS: JohnCalls Alarm
CPT:
t t 0.9
t f 0.05
f t 0.1
f f 0.95

FACTOR 5
VARS: Alarm Burglary Earthquake
CPT:
t t t 0.95
t t f 0.94
t f t 0.29
t f f 0.001
f t t 0.05
f t f 0.06
f f t 0.71
f f f 0.999

>> FACTORS INVOLVING VAR Earthquake (indicated by number):

2 5

>> PRODUCT OF FACTORS 2 5 (tabular form, rounded):

VARS: Earthquake Alarm Burglary
CPT:
t t t 0.00190
t t f 0.00058
t f t 0.00010
t f f 0.00142
f t t 0.93812
f t f 0.00100
f f t 0.05988
f f f 0.99700

>> MARGINALIZATION OF FACTOR PRODUCT W.R.T. Earthquake:

VARS: Alarm Burglary
CPT:
t t 0.94002
t f 0.00158
f t 0.05998
f f 0.99842

>> REMOVE FACTORS INVOLVING VAR Earthquake FROM SET OF FACTORS
>> ADD MARGINALIZATION W.R.T. Earthquake TO SET OF FACTORS


========== ITERATION 2 ==========

ELIMINATING VAR: Alarm

>> SET OF FACTORS (tabular form):

FACTOR 1
VARS: MaryCalls Alarm
CPT:
t t 0.7
t f 0.01
f t 0.3
f f 0.99

FACTOR 2
VARS: Burglary
CPT:
t 0.001
f 0.999

FACTOR 3
VARS: JohnCalls Alarm
CPT:
t t 0.9
t f 0.05
f t 0.1
f f 0.95

FACTOR 4
VARS: Alarm Burglary
CPT:
t t 0.94002
t f 0.001578
f t 0.05998
f f 0.998422

>> FACTORS INVOLVING VAR Alarm (indicated by number):

1 3 4

>> PRODUCT OF FACTORS 1 3 4 (tabular form, rounded):

VARS: Alarm MaryCalls JohnCalls Burglary
CPT:
t t t t 0.59221
t t t f 0.00099
t t f t 0.06580
t t f f 0.00011
t f t t 0.25381
t f t f 0.00043
t f f t 0.02820
t f f f 0.00005
f t t t 0.00003
f t t f 0.00050
f t f t 0.00057
f t f f 0.00949
f f t t 0.00297
f f t f 0.04942
f f f t 0.05641
f f f f 0.93902

>> MARGINALIZATION OF FACTOR PRODUCT W.R.T. Alarm:

VARS: MaryCalls JohnCalls Burglary
CPT:
t t t 0.59224
t t f 0.00149
t f t 0.06637
t f f 0.00960
f t t 0.25677
f t f 0.04985
f f t 0.08461
f f f 0.93906

>> REMOVE FACTORS INVOLVING VAR Alarm FROM SET OF FACTORS
>> ADD MARGINALIZATION W.R.T. Alarm TO SET OF FACTORS


========== WRAP-UP ==========

>> PRODUCT OF REMAINING FACTORS:

VARS: Burglary MaryCalls JohnCalls
CPT:
t t t 0.00059
t t f 0.00007
t f t 0.00026
t f f 0.00008
f t t 0.00149
f t f 0.00959
f f t 0.04980
f f f 0.93812

>> PROBABILITY VALUES GIVEN THE EVIDENCE:

t 0.00059 f 0.00149 

>> NORMALIZED POSTERIOR PROBABILITY DISTRIBUTION:

t 0.284 f 0.716