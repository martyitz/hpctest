################################################################################
#                                                                              #
#  dimension.py                                                                #
#  abstract superclass of all Experiment parameter types                       #
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
#  Copyright ((c)) 2002-2019, Rice University                                  #
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




class Dimension(object):
    
    @classmethod
    def name(cls):
        from common import subclassResponsibility
        subclassResponsibility("Dimension", "name")
    
    @classmethod
    def default(cls):
        from common import subclassResponsibility
        subclassResponsibility("Dimension", "default")

    @classmethod
    def format(self, value, forName=False):
        from common import subclassResponsibility
        subclassResponsibility("Dimension", "format")
    
    def __init__(self, spec=""):
        from common import mustNotCall
        mustNotCall("Dimension", "__init_", "it is abstract")

    def isEmpty(self):
        from common import subclassResponsibility
        subclassResponsibility("Dimension", "isEmpty")

    def values(self):
        from common import subclassResponsibility
        subclassResponsibility("Dimension", "values")

    def __iter__(self):
        from common import subclassResponsibility
        subclassResponsibility("Dimension", "__iter__")




