# SPSSINC HETCOR
## Calculate correlations between nominal, ordinal, and scale variables
 This procedure calculates correlations between nominal, ordinal, and scale variables, accounting for the measurement levels of the variables. The resulting heterogeneous correlation matrix consists of Pearson product-moment correlations between scale variables, polyserial correlations between scale and categorical variables, and polychoric correlations between categorical variables.

---
Requirements
----
- IBM SPSS Statistics 18 or later, the corresponding IBM SPSS Statistics-Integration Plug-in for Python and the IBM SPSS Statistics-Integration Plug-in for R.

Note: The SPSSINC HETCOR extension is installed as part of IBM SPSS Statistics-Essentials for R.

---
Installation intructions
----
1. Open IBM SPSS Statistics
2. Navigate to Utilities -> Extension Bundles -> Download and Install Extension Bundles
3. Search for the name of the extension and click Ok. Your extension will be available.

---
Tutorial
----
### Installation Location
Analyze

&nbsp;&nbsp;Correlate 

&nbsp;&nbsp;&nbsp;&nbsp;Heterogeneous Correlations...

### UI
<img width="790" alt="image" src="https://user-images.githubusercontent.com/19230800/194336858-70e81af7-9b1d-49d3-b9ed-8db0afd8fb7e.png">
<img width="342" alt="image" src="https://user-images.githubusercontent.com/19230800/194336909-643dbf8c-ec16-4b5b-9b71-4bc9878d9472.png">

### Syntax
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

#### OPTIONS
**ESTIMATOR** specifies the estimator. TWOSTEP may execute considerably
faster and is the default.  ML can fail to converge in some cases.

**STDERR**=TRUE causes a standard error to be included in the output.

**N**=TRUE causes the count for each correlation to be displayed.
It is ignored if STDERR=FALSE.

**TYPE**=TRUE causes a separate table of the correlation types to be displayed.

**EXECUTE**=FALSE processes the command syntax but does not execute it.
This is mainly useful in combination with SAVE PROGRAMFILE.

#### PROGRAMFILE
PROGRAMFILE causes the R code that implements the hetcor function to be
written to the specified file.

The SPSSINC HETCOR command requires both the Python and R Integration Plug-ins. package.

---
License
----

- [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
                              
Contributors
----

  - IBM SPSS
