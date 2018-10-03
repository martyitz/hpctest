################################################################################
#                                                                              #
#  workspace.py                                                                #
#  storage in a file system directory for a collection of per-test work dirs   #
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


# TEMPORARY: simplest possible thing: hold a path to the dir & just make run subdirs on request


_prefix = "study-"


class Workspace():   
    
    def __init__(self, path):
        
        from os import makedirs
        from os.path import basename, isfile, isdir, join 
        from time import strftime
        from common import BadWorkspacePath

        if isdir(path) and basename(path).startswith(_prefix):
                self.path = path
        elif not isfile(path):
            timestamp = strftime("%Y-%m-%d--%H-%M-%S")
            self.path = join(path, _prefix + timestamp)
            makedirs(self.path)
        else:
            raise BadWorkspacePath(path)


    def __str__(self):

        return "Workspace@{}".format(self.path)
        

    @classmethod
    def isWorkspace(cls, path):
        
        from os.path import basename, isdir 
        return isdir(path) and basename(path).startswith(_prefix)
    
    
    def addJobDir(self, testName, config, hpctoolkitparams):

        import os
        from os.path import join, isdir

        # TODO: should ensure uniqueness
        jobdir = join(self.path, "{}-{}-{}".format(testName, config, hpctoolkitparams)).replace(" ", ".")
        if isdir(jobdir):
            n = 2
            while( isdir(jobdir + "-" + str(n))): n += 1
            jobdir = jobdir + "-" + str(n)
        os.makedirs(jobdir)
        
        return jobdir
        
        
    def clean(self):
        
        from shutil import rmtree
        rmtree(self.path, ignore_errors=True)

    