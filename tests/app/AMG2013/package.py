#=================================================#
# AMG2013 PACKAGE FILE TO BE GENERATED BY HPCTEST #
#=================================================#


# from info.name, info.description, and build.kind
from spack import *
class AMG2013(HPCTestMakefilePackage):
    """AMG2013 is a parallel algebraic multigrid solver for linear systems arising from
       problems on unstructured grids.  The driver provided with AMG2013 builds linear 
       systems for various 3-dimensional problems.
       AMG2013 is written in ISO-C.  It is an SPMD code which uses MPI and OpenMP 
       threading within MPI tasks. Parallelism is achieved by data decomposition. The 
       driver provided with AMG2013 achieves this decomposition by simply subdividing 
       the grid into logical P x Q x R (in 3D) chunks of equal size. 
    """

# from info.homepage and info.url
    homepage = "https://codesign.llnl.gov/amg2013.php"
    url      = "https://github.com/HPCToolkit/HPCTest"

# from info.version
    version('1.0', 'app/AMG2013')

# from config[@openmp].{variant,description}, and config[@base].'default variants'
    variant('openmp', description='Build with OpenMP support', default=True)

# from config[@mpi].{variant,description,depends}, and config[@base].'default variants'
    variant('mpi', description='Build with MPI support', default=True)
    depends_on('mpi', when='+mpi')      # and mpicxx ??

# boilerplate for config[*].flags...
    @property
    def build_targets(self):
        targets = []
        
## from config[@base].languages
##    languages: [ cxx ]
        languages = 'CC = {}'.format(spack_cc)
        
## from config[@base].flags
##      CXXFLAGS: "-g -O3"
        cxxflags = '-g -O2'
        ldflags = '-lm'
        
## from config[@openmp].flags
##      +CXXFLAGS: $OPENMP_FLAG
##      +LDFLAGS:  $OPENMP_FLAG
        if '+openmp' in self.spec:
            cxxflags += ' ' + self.compiler.openmp_flag
            ldflags  += ' ' + self.compiler.openmp_flag
        
## from config[@mpi].languages
##    languages: [ mpicxx ]
        if '+mpi' in self.spec:
            languages = 'CXX = {}'.format(self.spec['mpi'].mpicxx)
        
## from config[@mpi].flags
##    flags: +CXXFLAGS: "-DUSE_MPI=1"
        if '+mpi' in self.spec:
            cxxflags += ' ' + '-DUSE_MPI=1'

## from config[@mpi].env
##      - "-DUSE_MPI=1"
##      - "MPI_INC = $MPI_INC"
##      - "MPI_LIB = $MPI_LIB"
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
        mkdirp(prefix.bin)
        install('amg2013', prefix.bin)





