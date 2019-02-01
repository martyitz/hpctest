################################################################################
#                                                                              #
#  iterate.py                                                                  #
#  robustly iterates over build configs and test cases using a testdir         #
#      to store iteration state across failed partial iterations               #
#                                                                              #
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




class Iterate():
    
    @classmethod
    def doForAll(myClass, dims, args, numrepeats, study):
        
        from itertools import product
        from common import infomsg, debugmsg, options
        from run import Run
        from executor import Executor

        if not dims["tests"].paths():       # TODO: check every dimension for emptiness, not just 'tests' -- requires more structure in Spec classes
            infomsg("test spec matches no tests")
            return False
        else:
            
            if Executor.batchInUse():
            
                # run tests asynchronously via batch system
                # TODO: throttle to some max # batch jobs scheduled at a time

                debugmsg("submitting batch jobs for runs over experiment space = crossproduct( {} ) with args = {} and options = {} in study dir = {}"
                            .format(dims, args, options, study.path))

                # schedule all the tests for batch execution
                launchedBatchRuns = set()
                for test, config, hpctoolkit, profile in product(dims["tests"], dims["build"], dims["hpctoolkit"], dims["profile"]):
                    jobID = Run.launchBatchRun(test, config, hpctoolkit, profile, numrepeats, study)
                    launchedBatchRuns.add(jobID)
                    
                # poll for completed batch jobs
                while not launchedBatchRuns.empty():
                    completed = Run.pollForFinishedRuns()
                    launchedBatchRuns.symmetric_difference_update(completed)  # since doneRuns containedIn launchedRuns, same as set subtract (not in Python)
                    for jobID in completed:
                        infomsg("...batch run of test {} finished".format(Run.descriptionForBatchJob(jobID)))
            else:
                
                # no batch system, run tests synchronously via shell
                # TODO: run tests concurrently in background throttled to some max # processes at a time

                debugmsg("performing runs over experiment space = crossproduct( {} ) with args = {} and options = {} in study dir = {}"
                            .format(dims, args, options, study.path))

                # run all the tests sequentially
                for test, config, hpctoolkit, profile in product(dims["tests"], dims["build"], dims["hpctoolkit"], dims["profile"]):
                    run = Run(test, config, hpctoolkit, profile, numrepeats, study)
                    status = run.run()
            
            




