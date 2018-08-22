#================================================#
# LULESH PACKAGE FILE TO BE GENERATED BY HPCTEST #
#================================================#


# from info.name, info.description, and build.kind
from spack import *
class Lulesh(MakefilePackage):
    """Many important simulation problems of interest to DOE involve complex multi-material
    systems that undergo large deformations. LULESH is a highly simplified application
    that represents the numerical algorithms, data motion, and programming style typical
    in scientific C or C++ based hydrodynamic applications. The Shock Hydrodynamics
    Challenge Problem was originally defined and implemented by LLNL as one of five
    challenge problems in the DARPA UHPC program and has since become a widely studied
    proxy application in DOE co-design efforts for exascale. It has been ported to a number
    of programming models and optimized for a number of advanced platforms. 
    """

# from info.homepage and info.url
    homepage = "https://codesign.llnl.gov/lulesh.php"
    url      = "https://github.com/HPCToolkit/HPCTest"

# from info.version
    version('1.0', 'app/lulesh')

# from config.variants[@openmp].{variant,description}, and config.'default variants'
    variant('openmp', description='Build with OpenMP support', default=True)

# from config.variants[@mpi].{variant,description,depends}, and config.'default variants'
    variant('mpi', description='Build with MPI support', default=True)
    depends_on('mpi', when='+mpi')

# boilerplate for config.variants[*].flags...
    @property
    def build_targets(self):
        targets = []
        
## from config.variants[@base].languages
        languages = 'CXX = {}'.format(spack_cxx)
        
## from config.variants[@base].flags
        cxxflags = '-g -O3'
        ldflags = '-g -O3'
        
## from config.variants[@openmp].flags
        if '+openmp' in self.spec:
            cxxflags += ' ' + self.compiler.openmp_flag
            ldflags  += ' ' + self.compiler.openmp_flag
        
## from config.variants[@mpi].languages
        if '+mpi' in self.spec:
            languages = 'CXX = {}'.format(self.spec['mpi'].mpicxx)
        
## from config.variants[@mpi].flags
        if '+mpi' in self.spec:
            cxxflags += ' ' + '-DUSE_MPI=1'

## from config.variants[@mpi].env
        if '+mpi' in self.spec:
            targets.append('MPI_INC = {0}'.format(self.spec['mpi'].prefix.include))
            targets.append('MPI_LIB = {0}'.format(self.spec['mpi'].prefix.lib))

# boilerplate closing 'build_targets'
        targets.append(languages)
        targets.append('CXXFLAGS = {0}'.format(cxxflags))
        targets.append('LDFLAGS = {0}'.format(ldflags))
        return targets

# from build.install
    def install(self, spec, prefix):
        import inspect
        mkdirp(prefix.bin)
        install('lulesh2.0', prefix.bin)





