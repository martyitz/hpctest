################################################################################
#                                                                              #
#  report.py                                                                   #
#  print the results from running a test suite by extracting from a testdir    #
#                                                                              #                                                                              #
#  $HeadURL$                                                                   #
#  $Id$                                                                        #
#                                                                              #
#  --------------------------------------------------------------------------- #
#  Part of HPCToolkit (hpctoolkit.org)                                         #
#                                                                              #
#  Information about sources of support for research and development of        #
#  HPCToolkit is at 'hpctoolkit.org' and in 'README.Acknowledgments'.          #
#  --------------------------------------------------------------------------- #
#                                                                              #
#  Copyright ((c)) 2002-2017, Rice University                                  #
#  All rights reserved.                                                        #
#                                                                              #
#  Redistribution and use in source and binary forms, with or without          #
#  modification, are permitted provided that the following conditions are      #
#  met:                                                                        #
#                                                                              #
#  * Redistributions of source code must retain the above copyright            #
#    notice, this list of conditions and the following disclaimer.             #
#                                                                              #
#  * Redistributions in binary form must reproduce the above copyright         #
#    notice, this list of conditions and the following disclaimer in the       #
#    documentation and/or other materials provided with the distribution.      #
#                                                                              #
#  * Neither the name of Rice University (RICE) nor the names of its           #
#    contributors may be used to endorse or promote products derived from      #
#    this software without specific prior written permission.                  #
#                                                                              #
#  This software is provided by RICE and contributors "as is" and any          #
#  express or implied warranties, including, but not limited to, the           #
#  implied warranties of merchantability and fitness for a particular          #
#  purpose are disclaimed. In no event shall RICE or contributors be           #
#  liable for any direct, indirect, incidental, special, exemplary, or         #
#  consequential damages (including, but not limited to, procurement of        #
#  substitute goods or services; loss of use, data, or profits; or             #
#  business interruption) however caused and on any theory of liability,       #
#  whether in contract, strict liability, or tort (including negligence        #
#  or otherwise) arising in any way out of the use of this software, even      #
#  if advised of the possibility of such damage.                               #
#                                                                              #
################################################################################




class Report():

    
    def printReport(self, study, whichspec, sortKeys):

        from os import listdir
        from os.path import isfile, isdir, join, basename, relpath
        from common import homepath, options, infomsg, debugmsg, errormsg, fatalmsg, sepmsg, truncate
        from spackle import readYamlFile, writeYamlFile

        def sortKeyFunc(result):
            def get_nested(my_dict, keys):
                key = keys.pop(0)
                return my_dict[key] if len(keys) == 0 else get_nested(my_dict[key], keys)
            keylist = []
            for keypath in dimkeys:
                keylist.append(get_nested(result["input"], list(keypath)))  # copy keypath b/c get_nested destroys its second argument
            return keylist
    
        studypath = study.path
####    tableWidth = 113    # width of table row manually determined    # TODO: better
        tableWidth = 110    # width of table row manually determined    # TODO: better
        
        debugmsg("reporting on study at {} with options {}".format(studypath, options))
            
        # collect the results from all runs meeting 'whichspec'
        reportAll    = whichspec == "all"
        reportPassed = whichspec == "pass"     # if 'reportAll', don't care
        studyDirs = listdir(studypath)
        results = list()
        fails   = list()
        for runname in studyDirs:
            runPath = join(studypath, runname)
            outPath = join(runPath, "OUT", "OUT.yaml")
            if isfile(outPath):
                resultdict, error = readYamlFile(outPath)
                if error: fatalmsg("result file OUT.yaml cannot be read for test run {}".format(runPath))
                ok = resultdict["summary"]["status"] == "OK"
                if reportAll or (reportPassed == ok):
                    results.append(resultdict)
                if not ok:
                    fails.append(resultdict)
            else:
                errormsg("Test results file OUT.yaml not found for run {}, ignored".format(runPath))

        # counts for final summary line
        numTests  = len(studyDirs)
        numFails  = len(fails)
        numPasses = numTests - numFails
        
        # print a summary record for each result, sorted by config spec and then test name
        if results:

            # sort results by input dimspec sequence
            dimkey_map = {"tests":       ["test"],
                          "build":       ["config spec"],
                          "hpctoolkit":  ["hpctoolkit"],
                          "profile":     ["hpctoolkit params", "hpcrun"]
                         }
            dimkeys = []
            for key in sortKeys:
                if key in dimkey_map:
                    dimkeys.append(dimkey_map[key])
                else:
                    errormsg("unknown sort key for report ignored: '{}'".format(key))
            if len(dimkeys):
                results.sort(key=sortKeyFunc)      # key func returns list of result fields corresponding to dimkey_list

            print
            for result in results:
                                
                # format for display -- line 1
                testLabel = self.labelForTest(result)
                line1 = "| {}".format(testLabel)
                line1 += " " * (tableWidth - len(line1) - 1) + "|"
                
                # format for display -- line 2
                info = self.extractRunInfo(result)
                if info.extractRunInfoMsg:
                    line2 = ("| {}: {}").format("REPORTING FAILED", truncate(info.extractRunInfoMsg, 100))         
                    line2 += " " * (tableWidth - len(line2) - 1) + "|"
                elif info.wantProfiling and info.status == "OK":
####                line2 = ("| overhead: {:>5} | recorded: {:>5} | blocked: {:>5} | errant: {:>5} | suspicious: {:>5} | trolled: {:>5} |"
                    line2 = ("| overhead: {:>5} | samples: {:>5} | recorded: {:>5} | blocked: {:>5} | errant: {:>5} | trolled: {:>5}  |"
                            ).format(_pct(info.overhead,   100), 
                                     info.samples, 
                                     _pct(info.recorded,   info.samples), 
                                     _pct(info.blocked,    info.samples), 
                                     _pct(info.errant,     info.samples), 
####                                 _pct(info.suspicious, info.samples), 
                                     _pct(info.trolled,    info.samples)
                                    )
                else:
                    line2 = ("| {}: {}").format(info.status, truncate(info.msg, 100))         
                    line2 += " " * (tableWidth - len(line2) - 1) + "|"
    
                # print run's summary
                sepmsg(tableWidth)
                print line1
                print line2
                       
            sepmsg(tableWidth)
            print; print
            
            # final summary
            print "TESTS:  {}".format(numTests)
            print "PASSED: {}".format(numPasses)
            print "FAILED: {}".format(numFails)
            print
            if numFails:
                print "Failed tests:"
                for f in fails:
                    print "    {}".format(self.labelForTest(f))
            print; print

        else:
            infomsg("no completed runs to report")
            debugmsg("reportspec = '--which {}'".format(whichspec))


    def extractRunInfo(self, result):
        
        from argparse import Namespace
        from ast import literal_eval

        info = Namespace()
        
        info.extractRunInfoMsg = None
        
        try:
            
            info.test           = result["input"]["test"].upper().replace("/", " / ")
            info.config         = result["input"]["config spec"].upper()
            info.hpctoolkit     = result["input"]["hpctoolkit"]
            info.params         = result["input"]["hpctoolkit params"]["hpcrun"]
            info.wantProfiling  = literal_eval(result["input"]["wantProfiling"])
            info.status         = result["summary"]["status"]
            info.msg            = result["summary"]["status msg"] if info.status != "OK" else "cpu time {} seconds".format(result["run"]["normal"]["cpu time"])
            run                 = result["run"]
                                            
            if info.wantProfiling and (run != "NA"):
                hpcrun          = run["profiled"]["hpcrun summary"]
                info.overhead   = run["profiled"]["hpcrun overhead %"]
            else:
                hpcrun          = "NA"
                info.overhead   = "NA"
                
            if hpcrun != "NA":
                info.blocked    = hpcrun["blocked"]
                info.errant     = hpcrun["errant"]
                info.frames     = hpcrun["frames"]
                info.intervals  = hpcrun["intervals"]
                info.recorded   = hpcrun["recorded"]
                info.samples    = hpcrun["samples"]
                info.suspicious = hpcrun["suspicious"]
                info.trolled    = hpcrun["trolled"]
                info.yielded    = hpcrun["yielded"]
            else:
                info.blocked    = None
                info.errant     = None
                info.frames     = None
                info.intervals  = None
                info.recorded   = None
                info.samples    = None
                info.suspicious = None
                info.trolled    = None
                info.yielded    = None
            
        except Exception as e:
            info.extractRunInfoMsg = e.message      # TODO: 'KeyError' => "status"; e.message and str(e) no better
    
        return info


    def labelForTest(self, testdict):

        info  = self.extractRunInfo(testdict)
        label = "{} with {}".format(info.test, info.config)
        if info.wantProfiling:
            label += " and {}".format(info.params)  # TODO: display hpctoolkit path but make sure line's not too long
        return label


def _pct(s, d):
    
    if (s is None or s == "NA") or (d is None or d == "NA"):
        formatted = " ---- "
    else:
        percent   = (float(s) / float(d)) * 100.0
        formatted = "  0   " if s == 0 else "< 0.1%" if percent < 0.1  else "< 1  %" if percent < 1.0 else "{:>5.1f}%".format(percent)
        
    return formatted


    
    
    
    
    
    
    

