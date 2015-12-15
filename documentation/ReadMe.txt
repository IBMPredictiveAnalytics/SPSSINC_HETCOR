#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2011
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/

This zip file contains the materials for the extension command

SPSSINC HETCOR


The command provides a procedure for polychoric and polyserial correlations (as well as Pearson correlation).

This material requires SPSS Statistics 17.0.3 or higher.


Users with IBM SPSS Statistics 19 or Higher
------------------------------------------

The SPSSINC HETCOR extension command is installed with R Essentials. If you have not already done so, then please install R Essentials. 
It is available from the SPSS community at http://www.ibm.com/developerworks/spssdevcentral. The command also requires the Python Plug-in, 
which is installed with Python Essentials, available from the SPSS community. Once you have installed R Essentials and Python Essentials, 
you have everything required to run the SPSSINC HETCOR extension command.

See the Usage section for additional details.


Users with PASW Statistics 18
-----------------------------

The SPSSINC HETCOR extension command may already be installed on your system. If it is not, then first ensure that the R Plug-in is installed. 
It is available from the SPSS community at http://www.ibm.com/developerworks/spssdevcentral. Then do the following:

Extract SPSSINC_HETCOR.spe from the zip file, and from the SPSS Statistics menus choose

Utilities>Extension Bundles>Install Extension Bundle

In the Open Extension Bundle dialog, navigate to the location where you extracted the file, select SPSSINC_HETCOR.spe and click Open.

To run the SPSSINC HETCOR extension command, you will also need the Python Plug-in, available from the SPSS community. 

See the Usage section for additional details.


SPSS Statistics 17 Users
------------------------

This material requires the Python plug-in and the R plug-in, as well as the R polycor package.
It includes a dialog box definition, a help file, the syntax definition, and the implementation files.

To install this procedure, unzip all of the files into the extensions subdirectory of your SPSS Statistics installation. Please ensure that the files are at the root 
of the extensions subdirectory, not in a folder under the extensions subdirectory. For Mac, the extensions directory is located under the Contents directory 
in the SPSS Statistics application bundle.

Next, in SPSS Statistics, use

Utilties>Install Custom Dialog

to add this item to the menus by navigating to where you unzipped the files and selecting SPSSINC_HETCOR.spd.


Usage
------  

The dialog box will appear on the Utilties menu.

Executing

SPSSINC HETCOR /HELP.

will display the complete syntax help.



Questions and comments should be directed to the Python or R Programmability forum on the SPSS community.
