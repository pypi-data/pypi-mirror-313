import os
import sys
from .utils import customArgParser, __params__

cachePath = "/cache"

# ./configure CXX=YourC++Compiler 
# ./configure --prefix=TheInstallationDirectory
# ./configure CXX=YourC++Compiler  --prefix=TheInstallationDirectory 
# ./configure --prefix=`pwd` --enable-fortran

# Macos 
# Brew gcc/7.3.0_1 (gcc, g++, gfortran)
# ./configure --prefix=`pwd` CC=gcc-7 CXX=g++-7 --enable-fortran
# ./configure --prefix=`pwd` CC=clang CXX=clang++ OPENMP_CFLAGS="-I/usr/local/Cellar/libomp/5.0.1/include -Xclang -fopenmp" OPENMP_CXXFLAGS="-I/usr/local/Cellar/libomp/5.0.1/include -Xclang -fopenmp" OPENMP_LDFLAGS="-L/usr/local/Cellar/libomp/5.0.1/lib -lomp"
# ./configure --prefix=`pwd` CC=clang CXX=clang++ OPENMP_CFLAGS="-I/usr/local/Cellar/libomp/7.0.0/include -Xclang -fopenmp" OPENMP_CXXFLAGS="-I/usr/local/Cellar/libomp/7.0.0/include -Xclang -fopenmp" OPENMP_LDFLAGS="-L/usr/local/Cellar/libomp/7.0.0/lib -lomp"
# On OSX gcc may be a wrapper for clang. In that case you can use:
# ./configure --prefix=`pwd` CC=clang CXX=clang++

def initPromise(**argv): 
    
    import subprocess
    import platform

    opt_system = platform.system()
    curr_loc = os.path.dirname(os.path.realpath(__file__))

    install_cadna = True
    args = customArgParser(sys.argv[1:] if argv == {} else argv, __params__)      # parse the command line


    compiler_CXX = 'g++'
    compiler_CC = 'g++'
    
    if '--CXX' in args:
        compiler_CXX = args['--CXX']

    if '--CC' in args:
        compiler_CC = args['--CC']
        
    if not os.path.exists(curr_loc + cachePath):
        os.makedirs(cachePath)
        
    if 'CADNA_PATH' in os.environ:    
        import logging
        logging.basicConfig()
        log = logging.getLogger()

        log.warning("It looks like your machine has CADNA installed, are you sure to proceed CADNA installation? ")
        check_point = input("Please answer 'yes' or 'no':")

        if check_point.lower() in {'yes', 'y'}:
            install_cadna = True

        else:
            install_cadna = False

    curr_loc = os.path.dirname(os.path.realpath(__file__))

    if os.path.exists(curr_loc + cachePath):
        if os.path.isfile(curr_loc + cachePath + '/CXX.txt'):
            with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
                compiler = file.read().replace('\n', '')
                print('check compilers:', compiler)

                if compiler_CXX != compiler:
                    install_cadna = True
                    

    os.chdir(curr_loc+'/cadna')

    if install_cadna:
        with open(curr_loc + cachePath + "/CC.txt", "w") as file:
            file.write(compiler_CC)
            
        with open(curr_loc + cachePath + "/CXX.txt", "w") as file:
            file.write(compiler_CXX)

        # must set environmental variables
        if not os.path.isfile('a.out') and not os.path.isfile('lib/libcadnaC.a'):
            
            if opt_system in {'Linux', 'posix', 'Darwin'}:
                if compiler_CC == 'g++' and compiler_CXX == 'g++':
                    subprocess.call('bash run_unix.sh', shell=True)

                elif compiler_CC != 'g++' and compiler_CXX != 'g++':
                    subprocess.call('bash run_unix.sh '+compiler_CC+' '+compiler_CXX, shell=True)

                elif compiler_CC != 'g++' and compiler_CXX == 'g++':
                    subprocess.call('bash run_unix_cc.sh '+compiler_CC, shell=True)

                else:
                    subprocess.call('bash run_unix_cxx.sh '+compiler_CXX, shell=True)

            elif opt_system == 'Windows': # under test
                if compiler_CC == 'g++' and compiler_CXX == 'g++':
                    subprocess.call(
                        './configure CXX=g++ --prefix=`cd` --enable-half-emulation --disable-dependency-tracking', 
                        shell=True)

                elif compiler_CC != 'g++' and compiler_CXX != 'g++':
                    subprocess.call(
                        './configure '+'CC='+compiler_CC+' '+'CXX='+compiler_CXX+' --prefix=`cd` --enable-half-emulation --disable-dependency-tracking', 
                        shell=True)

                elif compiler_CC != 'g++' and compiler_CXX == 'g++':
                    subprocess.call(
                        './configure '+'CC='+compiler_CC+' --prefix=`cd` --enable-half-emulation --disable-dependency-tracking', 
                        shell=True)

                else: 
                    subprocess.call(
                        './configure '+'CXX='+compiler_CXX+' --prefix=`cd` --enable-half-emulation --disable-dependency-tracking', 
                        shell=True)

                subprocess.call('make install', shell=True)
    