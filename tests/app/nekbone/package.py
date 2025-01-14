#=================================================#
# NEKBONE PACKAGE FILE TO BE GENERATED BY HPCTEST #
#=================================================#


# from info.name, info.description, and build.kind
from spack import *
class Nekbone(MakefilePackage):
    """Nekbone is captures the basic structure and user interface of the
        extensive Nek5000 software. Nek5000 is a high order, incompressible
        Navier-Stokes solver based on the spectral element method. It has
        a wide range of applications and intricate customizations available
        to users. Nekbone, on the other hand, solves a Helmholtz equation
        in a box, using the spectral element method. It is pared down to
        include only the necessary features to compile, run, and solve the
        applications found in the test/ directory. Since almost all practical
        applications are in the three dimensional space, the solver is
        set to work with three dimensional geometries as default. Nekbone
        solves a standard Poisson equation using a conjugate gradient iteration
        with a simple preconditioner on a block or linear geometry (set
        within the test directory of the simulation). Nekbone exposes the
        principal computational kernel to reveal the essential elements of
        the algorithmic-architectural coupling that is pertinent to Nek5000. 
    """

# from info.homepage and info.url
    homepage = "https://cesar.mcs.anl.gov/content/software/thermal hydraulics"
    url      = "https://github.com/HPCToolkit/HPCTest"

# from info.version
    version('1.0', 'app/nekbone-2.3.4')

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
##    languages: [ cxx ]
        languages = 'CC = {} F90 = {}'.format(spack_cc, spack_fc)
        
## from config.variants[@base].flags
##      CXXFLAGS: "-g -O3"
        cflags = '-g -O3'
        fflags = '-g -O3'
        lflags = '-g -O3'
        
## from config.variants[@openmp].flags
##      +CXXFLAGS: $OPENMP_FLAG
##      +LDFLAGS:  $OPENMP_FLAG
        if '+openmp' in self.spec:
            cflags += ' ' + self.compiler.openmp_flag
            lflags += ' ' + self.compiler.openmp_flag
        
## from config.variants[@mpi].languages
##    languages: [ mpicxx ]
        if '+mpi' in self.spec:
            languages = 'CC={} F77={}'.format(self.spec['mpi'].mpicc, self.spec['mpi'].mpifc) # sic 'F77' b/c makefile uses it for f90 (!)
        
## from config.variants[@mpi].flags
##    flags: +CXXFLAGS: "-DUSE_MPI=1"
        if '+mpi' in self.spec:
            targets.append('USE_MPI=1')

# boilerplate closing 'build_targets'
        targets.append(languages)
        targets.append('CFLAGS="{0}"'.format(cflags))
        targets.append('FFLAGS="{0}"'.format(fflags))
        targets.append('LFLAGS="{0}"'.format(lflags))
        return targets

# from build.kind
    def build(self, spec, prefix):
        """Runs specified command, passing :py:attr:`~.MakefilePackage.build_targets`
        as targets.
        """
        import os
        from os.path import join as path_join
        from subprocess import call
        print "env {} ./makenek ex1".format(" ".join(self.build_targets))
        call("env {} ./makenek ex1".format(" ".join(self.build_targets)),
             shell=True, cwd=path_join(self.build_directory, "test", "example1"))


# from build.install
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('test/example1/nekbone', prefix.bin)
        install('test/example1/data.rea', prefix.bin)
        install('test/example1/SIZE', prefix.bin)





