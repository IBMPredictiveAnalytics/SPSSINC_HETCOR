﻿* test SPSSINC HETCOR.
dataset close all.
get file='c:/spss16/samples/employee data.sav'.

SPSSINC HETCOR /help.

SPSSINC HETCOR salary educ 
  /OPTIONS ESTIMATOR=TWOSTEP STDERR=TRUE EXECUTE=FALSE
  MISSING=PAIRWISE N=TRUE TYPE=TRUE
  /SAVE PROGRAMFILE="C:\temp\hetcor_test.sps".
  
SPSSINC HETCOR salary educ /OPTIONS ESTIMATOR=TWOSTEP STDERR=TRUE.

VARIABLE LEVEL minority(nominal).
SPSSINC HETCOR salary educ minority /OPTIONS ESTIMATOR=TWOSTEP STDERR=TRUE.


SPSSINC HETCOR salary salbegin/OPTIONS STDERR=TRUE.
SPSSINC HETCOR jobcat educ/OPTIONS STDERR=TRUE.
SPSSINC HETCOR salary jobcat /OPTIONS ESTIMATOR=ML STDERR=TRUE.

GET  FILE='C:\spss16\Samples\1991 U.S. General Social Survey.sav'.
DATASET NAME DataSet1 WINDOW=FRONT.
***select if nvalid(hlth1, hlth2) = 2.
SPSSINC HETCOR hlth1 hlth2 /OPTIONS STDERR=TRUE.

SPSSINC HETCOR educ jobcat minority bdate 
/OPTIONS ESTIMATOR=TWOSTEP STDERR=TRUE
MISSING=PAIRWISE N=TRUE TYPE=TRUE.
