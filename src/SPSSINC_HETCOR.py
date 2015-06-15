# module to run an R program as an Extension command

#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2014
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/

from __future__ import with_statement

__author__ = "SPSS, JKP"
__version__ = "2.0.4"

# history
# 16-may-2009 handle very long variable lists
# 2-jul-2009 handle SPSS_EXTENSIONS_PATH variable for translation catalogues
# 15-jul-2009 special handling for Chinese olangs
# 04-mar-2011 fix nonunicode mode nonwestern translation when system code page does not match
# 11-apr-2011 handle extensions location for Mac
# 14-jun-2013 make corr types translatable
# 21-nov-2014 support TO and ALL


import spss, spssaux
from spssaux import u
from extension import Template, Syntax, checkrequiredparams, processcmd
import sys, inspect, tempfile, os, csv, codecs, gettext, os.path, textwrap, locale

# debugging
    # makes debug apply only to the current thread
#try:
    #import wingdbstub
    #if wingdbstub.debugger != None:
        #import time
        #wingdbstub.debugger.StopDebug()
        #time.sleep(1)
        #wingdbstub.debugger.StartDebug()
    #import thread
    #wingdbstub.debugger.SetDebugThreads({thread.get_ident(): 1}, default_policy=0)
    ## for V19 use
    ###    ###SpssClient._heartBeat(False)
#except:
    #pass

helptext="""The SPSSINC HETCOR command requires the Python Integration Plug-in,
the R Integration Plug-in and the R polycor package.

SPSSINC HETCOR variablelist
[/OPTIONS [ESTIMATOR={TWOSTEP**}]
                     {ML       }
          [STDERR={TRUE**}]
                  {FALSE }
          [N={TRUE**}]
             {FALSE }
          [TYPE={TRUE**}]
                {FALSE }
          [MISSING={PAIRWISE**}]
                   {LISTWISE  }
          [EXECUTE={TRUE**}] ]
                   {FALSE }

[/SAVE PROGRAMFILE=filespec]

Split files and weight are not honored by this command.

SPSSINC HETCOR /HELP prints this information and does nothing else.

Example:
SPSSINC HETCOR var1 var2 var3 /OPTIONS STDERR=TRUE.

Compute the correlations of variables in variablelist using the hetcor function
from the R polycor package. The type of correlation is determined by the 
measurement levels of each pair of variables.

The estimator can be TWOSTEP or ML.  TWOSTEP may execute considerably
faster and is the default.  ML can fail to converge in some cases.

STDERR=TRUE causes a standard error to be included in the output.
N=TRUE causes the count for each correlation to be displayed.
Ignored if STDERR=FALSE.
TYPE=TRUE causes a separate table of the correlation types to be displayed.

EXECUTE=FALSE runs the command syntax without calling the hetcor function. 
This is mainly useful in combination with SAVE PROGRAMFILE.

SAVE PROGRAMFILE causes the R code that implements the hetcor function to be
written to the specified file.  Since hetcor has features not exposed in this 
extension command, the generated program can be a useful starting point 
for additional specifications.
"""

def rpolycor(data, estimator="twostep", stderr=True, missing="pairwise", n=True,
             type=True, programfile=None, execute=True):
    """Run R polycor procedure.

    data is a sequence of the variable names to correlate
    ml indicates maximum likelihood or twostep estimator
    stderr indicates whether to compute std errs or not"""

    if spssaux.GetSPSSMajorVersion() >= 18:
        domain = "SPSSINC_HETCOR"
        extloc = os.path.dirname(inspect.stack()[0][1])
        dirname = os.path.join(extloc,domain,"lang")
        if os.getenv("SPSS_EXTENSIONS_PATH"):
            paths = os.getenv("SPSS_EXTENSIONS_PATH").replace("\\","/").split(os.pathsep)
            for path in paths:
                tempdirname = os.path.join(path,domain,"lang")
                if (os.path.exists(tempdirname)):
                    dirname = tempdirname
                    break
        languages = None; codeset = None
        # Need to handle Chinese olangs manually
        try:
            lang = {"schinese":"chinese-s","tchinese":"chinese-t","bportugu":"portuguese_brazil"}[os.getenv("LANGUAGE").lower()]
            languages = [lang]
        except:
            pass
        if spss.PyInvokeSpss.IsUTF8mode():
            codeset = "UTF-8"
        else:
            codeset = locale.getlocale()[1]  # 3/4/11
        t = gettext.translation(domain,fallback=True,localedir=dirname,codeset=codeset,languages=languages)
    else:
        t = gettext.NullTranslations()

    vardict = spssaux.VariableDict(data)
    estimator = estimator == "ml" and "TRUE" or "FALSE"
    stderr = stderr and "TRUE" or "FALSE"
    missing = missing == "listwise" and "complete.obs" or "pairwise.complete.obs"
    if len(data) < 2:
        print u(t.lgettext("At least two variables must be specified"))
        raise ValueError

    # check the measurement levels and code accordingly
    dfex = []
    for i, v in enumerate(data):
        vl = vardict[data[i]].VariableLevel
        if vl == 'nominal':
            vlexpr = "factor(dta[,%s])" % (i+1)
        elif vl == 'ordinal':
            vlexpr = "ordered(dta[,%s])" % (i+1)
        else:
            vlexpr = "dta[,%s]" % (i+1)
        dfex.append(vlexpr)
    data = "c(" + ", ".join(['"' + v + '"' for v in data]) + ")"
    data = "\n".join(textwrap.wrap(data, width=100))
    dfex = "\n".join(textwrap.wrap(", ".join(dfex), width=100))
    outputfilespec = (tempfile.gettempdir() + os.sep + "hetcorout.csv").replace("\\","/")

    pgm = r"""BEGIN PROGRAM R.
domain<-"SPSSINC_HETCOR"
if (as.integer(substr(GetSPSSVersion(),1, 2)) >= 18) {
      if (Sys.info()[[1]]=="Darwin"){
         majorVersion<-strsplit(spsspkg.GetSPSSVersion(),".",fixed=TRUE)[[1]][[1]]
         if (as.integer(majorVersion) >= 19)
            basepath<-file.path("/Library/Application Support/IBM/SPSS/Statistics",majorVersion)
         else
	    basepath<-file.path("/Library/Application Support/SPSSInc/PASWStatistics",majorVersion)
      } else {basepath<-file.path(spsspkg.GetStatisticsPath())}
      res<-bindtextdomain(domain,dirname=file.path(basepath,"extensions",domain,"lang"))
      paths<-strsplit(Sys.getenv("SPSS_EXTENSIONS_PATH"),.Platform$path.sep)[[1]]
      if (!identical(paths,character(0))){
         for (i in 1:length(paths)){
            dirname<-file.path(paths[[i]],domain,"lang")
            if (file.exists(dirname)){
               res<-bindtextdomain(domain,dirname=dirname)
               break
            }
         }
      }
}
tryCatch(library(polycor), error=function(e){
         stop(paste(gettext("The following R package is required but could not be loaded:",domain=domain),"polycor"),call.=FALSE)
        }
)
if (as.integer(substr(GetSPSSVersion(),1, 2)) >= 18) {
dta <- spssdata.GetDataFromSPSS(%(data)s,missingValueToNA=TRUE)
} else {
dta <- spssdata.GetDataFromSPSS(%(data)s)
is.na(dta)<-is.na(dta)
}
df <- data.frame(%(dfex)s)
res <- tryCatch(hetcor(df, ML=%(estimator)s, std.err=%(stderr)s, use="%(missing)s"),
        error=function(e) {return(NULL)})
if (identical(res, NULL))  {write("\"COMMAND FAILED\"", file="%(outputfilespec)s") } else {
        bound <- rbind(res$corr, res$std.errors, res$n, res$type)
        write.table(bound, "%(outputfilespec)s") }

res <- tryCatch(rm(list=ls()),warning=function(e){return(NULL)})

END PROGRAM.
""" % locals()

    if programfile:
        cmdfile = programfile.replace("\\", "/")
        f = codecs.open(cmdfile, "wb", encoding="utf_8_sig")
        f.write(pgm)
        f.close()

    if execute:
        try:
            os.remove(outputfilespec)
        except:
            pass

        spss.Submit(pgm)
        genoutput(outputfilespec, data, stderr, type, n, missing,t)

        try:
            os.remove(outputfilespec)
        except:
            pass

def Run(args):
    """Execute the HETCOR command"""

    args = args[args.keys()[0]]

    oobj = Syntax([
        Template("", subc="",  ktype="existingvarlist", var="data", islist=True),
        Template("ESTIMATOR", subc="OPTIONS",  ktype="str", var="estimator", vallist=["twostep","ml"]),
        Template("STDERR", subc="OPTIONS",ktype="bool", var="stderr"),
        Template("MISSING", subc="OPTIONS",ktype="str", vallist=["pairwise","listwise"]),
        Template("N", subc="OPTIONS",ktype="bool", var="n"),
        Template("TYPE", subc="OPTIONS",ktype="bool", var="type"),
        Template("PROGRAMFILE", subc="SAVE", ktype="literal", var="programfile"),
        Template("EXECUTE", subc="OPTIONS", ktype="bool", var="execute")])

    if args.has_key("HELP"):
        #print helptext
        helper()
    else:
        processcmd(oobj, args, rpolycor, vardict=spssaux.VariableDict())

def helper():
    """open html help in default browser window
    
    The location is computed from the current module name"""
    
    import webbrowser, os.path
    
    path = os.path.splitext(__file__)[0]
    helpspec = "file://" + path + os.path.sep + \
         "markdown.html"
    
    # webbrowser.open seems not to work well
    browser = webbrowser.get()
    if not browser.open_new(helpspec):
        print("Help file not found:" + helpspec)
try:    #override
    from extension import helper
except:
    pass
from spss import CellText

def genoutput(outputfilespec, data, stderr, ctype, n, missing, t):
    """Generate pivot tables for R results as written to a csv file.

    outputfilespec is the csv file holding the R output
    data is the string listing the variable names in the form c("var1", "var2", ..., "varn")
    stderr is the stderr option used (TRUE or FALSE)
    ctype is the type option (True or False)
    n is the n option
    missing is the missing value option, which influences the N reporting.
    If stderr was not requested, its rows and the n rows will be omitted.
    t is the Translations instance for localizing the output"""

    stderr = stderr == "TRUE"
    # On the Mac, contrary to the R documentation, an R csv file by
    # default gets written with comma decimals in a comma-decimal locale
    # so replace with period to allow computations to proceed
    try:
        r = csv.reader(file(outputfilespec, "rb"), delimiter= " ")
        lines = [line for line in r]
        for i in range(len(lines)):
            lines[i] = [item.replace(",", ".") for item in lines[i]]
    except:
        print u(t.lgettext("%s command failed")%"SPSSINC HETCOR")
        raise Exception
    data = data[2:-1].split()
    varCount = len(data)
    if lines.pop(0) == ["COMMAND FAILED"]:
        print u(t.lgettext("%s command was unable to compute the correlations due to data conditions.\n"
                           "This is usually due to some variables being too far from a bivariate normal distribution.")%"SPSS HETCOR")
        raise Exception

    StartProcedure(u(t.lgettext("Heterogeneous Correlation")),"SPSSINC HETCOR")
    pt = spss.BasePivotTable(u(t.lgettext("Pearson, Polyserial, and Polychoric Correlations")),
                             "HeterogeneousCorrelations", u(t.lgettext("Correlations")), isSplit=False, caption=u(t.lgettext("Correlations computed by R %s package")%"Hetcor"))
    coldim = pt.Append(spss.Dimension.Place.column, u(t.lgettext("Variables"))+" ")
    rowdim1 = pt.Append(spss.Dimension.Place.row, u(t.lgettext("Variables")))
    rowdim2 = pt.Append(spss.Dimension.Place.row, u(t.lgettext("Statistics")))
    rowdim1cats = [CellText.String(v.strip(',"')) for v in data]   # should be VarName, but that requires an index
    pt.SetCategories(rowdim1, rowdim1cats)
    catlist = [u(t.lgettext("Correlation"))]
    if stderr:
        catlist.append(u(t.lgettext("Std. Error")))
        if n and not missing == "complete.obs":
            catlist.append(u(t.lgettext("N")))
    rowdim2cats = [CellText.String(v) for v in catlist]
    pt.SetCategories(rowdim2, rowdim2cats )
    pt.SetCategories(coldim, rowdim1cats)

    for i in range(varCount):
        for j in range(len(rowdim2cats)):
            line = [cellFloatOrElse(lin) for lin in lines[i + j * varCount][1:]]
            pt.SetCellsByRow((rowdim1cats[i], rowdim2cats[j]), line)
    if missing == "complete.obs":
        pt.TitleFootnotes(u(t.lgettext("N = %s") % lines[-varCount-1][1]))
    if ctype:
        # variable by variable correlation types
        pt = spss.BasePivotTable(u(t.lgettext("Correlation Types")),
                                 "CorrelationTypes", u(t.lgettext("Correlation Types")), isSplit=False)
        coldim = pt.Append(spss.Dimension.Place.column, u(t.lgettext("Variables"))+" ")
        rowdim1 = pt.Append(spss.Dimension.Place.row, u(t.lgettext("Variables")))
        pt.SetCategories(rowdim1, rowdim1cats)
        pt.SetCategories(coldim, rowdim1cats)

        # the last varCount lines in the file are the correlation types
        # translation expects the types to be in the translation file, but
        # "" translates wrong so is coerced to "--"
        lenlines = len(lines)
        for i in range(varCount):		
            line = [CellText.String(lin == "" and "--" or
                u(t.lgettext(lin))) for lin in lines[i + lenlines - varCount][1:]]
            pt.SetCellsByRow(rowdim1cats[i], line)
    spss.EndProcedure()

def cellFloatOrElse(value):
    """return float(value) or None if unconvertable"""
    try:
        return CellText.Number(float(value))
    except:
        return CellText.String(".")

def StartProcedure(procname, omsid):
    """Start a procedure

    procname is the name that will appear in the Viewer outline.  It may be translated
    omsid is the OMS procedure identifier and should not be translated.

    Statistics versions prior to 19 support only a single term used for both purposes.
    For those versions, the omsid will be use for the procedure name.

    While the spss.StartProcedure function accepts the one argument, this function
    requires both."""

    try:
        spss.StartProcedure(procname, omsid)
    except TypeError:  #older version
        spss.StartProcedure(omsid)