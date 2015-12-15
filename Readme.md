# SPSSINC HETCOR
## Calculate correlations between nominal, ordinal, and scale va
 This procedure calculates correlations between nominal, o  rdinal, and scale variables, accounting for the measurement levels of   the variables. The resulting heterogeneous correlation matrix consis  ts of Pearson product-moment correlations between scale variables, po  lyserial correlations between scale and categorical variables, and po  lychoric correlations between categorical variables. The procedure us  es the hetcor function from the R polycor package.

---
Requirements
----
- IBM SPSS Statistics 18 or later

---
Installation intructions
----
1. Open IBM SPSS Statistics
2. Navigate to Utilities -> Extension Bundles -> Download and Install Extension Bundles
3. Search for the name of the extension and click Ok. Your extension will be available.

---
Tutorial
----
SPSSINC HETCOR *variables*^&#42;

/OPTIONS ESTIMATOR=TWOSTEP^&#42;&#42; or ML  
STDERR=TRUE^&#42;&#42; or FALSE  
N=TRUE^&#42;&#42; or FALSE  
TYPE=TRUE^&#42;&#42; or FALSE  
MISSING=PAIRWISE^&#42;&#42; or LISTWISE  
EXECUTE=TRUE^&#42;&#42; or FALSE

/SAVE PROGRAMFILE="*filespec*"

^&#42; Required  
^&#42;&#42; Default

SPSSINC HETCOR /HELP prints this information and does nothing else.


Split files and weight are not honored by this command.

Example:
```
SPSSINC HETCOR var1 var2 var3 /OPTIONS STDERR=TRUE.
```

The variable list specifies the variables to be correlated.
The type of correlation is determined by the 
measurement levels of each pair of variables.

OPTIONS
-------
**ESTIMATOR** specifies the estimator. TWOSTEP may execute considerably
faster and is the default.  ML can fail to converge in some cases.

**STDERR**=TRUE causes a standard error to be included in the output.

**N**=TRUE causes the count for each correlation to be displayed.
It is ignored if STDERR=FALSE.

**TYPE**=TRUE causes a separate table of the correlation types to be displayed.

**EXECUTE**=FALSE processes the command syntax but does not execute it.
This is mainly useful in combination with SAVE PROGRAMFILE.

PROGRAMFILE
-----------
PROGRAMFILE causes the R code that implements the hetcor function to be
written to the specified file.

The SPSSINC HETCOR command requires both the Python and R Integration Plug-ins. package.

---
License
----

- Apache 2.0
                              
Contributors
----

  - IBM SPSS
