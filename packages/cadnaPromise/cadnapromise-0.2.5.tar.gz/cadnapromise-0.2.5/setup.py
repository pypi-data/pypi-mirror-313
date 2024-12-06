# coding: utf-8
 
import logging
from setuptools import setup
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

def readme():
	"""import the readme file"""
	with open('README.rst') as f:
		return f.read()


def get_version(fname):
    with open(fname) as f:
        for line in f:
            if line.startswith("__version__ = '"):
                return line.split("'")[1]
    raise RuntimeError('Error in parsing version string.')

__package__ = 'cadnaPromise'
__version__ = get_version(__package__+'/__init__.py')
ext_errors = (CCompilerError, ModuleNotFoundError, DistutilsExecError, DistutilsPlatformError, IOError, SystemExit)

logging.basicConfig()
log = logging.getLogger(__file__)

setup_args = {'name': __package__,
		'version': __version__,
		'description':'Precision auto-tuning of floating-point variables in program',
		'long_description':readme(),
		# packages = setuptools.find_packages(),
		'classifiers':["Intended Audience :: Science/Research",
					"Intended Audience :: Developers",
					"Programming Language :: C",
					"Programming Language :: Python",
					"Topic :: Software Development",
					"Topic :: Scientific/Engineering",
					'Operating System :: POSIX',
					'Operating System :: Unix',
					'Operating System :: MacOS',
					"Programming Language :: Python :: 3",
					],
		'keywords':'computer arithmetic mixed-precision, precision auto-tuning',
		'url':'https://github.com/PEQUAN/cadnaPromise',
		'author':'LIP6 PEQUAN team',
		'author_email':'thibault.hilaire@lip6.fr; fabienne.jezequel@lip6.fr; xinyechenai@gmail.com',
		'license':'GNU General Public License v3.0',
		'packages':{"cadnaPromise",
			  		"cadnaPromise.cadna", 
					"cadnaPromise.deltadebug",  
					"cadnaPromise.extra",
					"cadnaPromise.cache"
					},
		'package_data':{"cadnaPromise": ["deltadebug/*", "cadna/*", "extra/*", "cache/*"]},
		'tests_require':['pytest', 'pytest-cov'],
		'setup_requires':['colorlog', 'colorama', 'regex'],
		'install_requires':['colorlog', 'colorama', 'tqdm', 'regex', 'pyyaml'],
		'extras_require':{'with_doc': ['sphinx', 'sphinx_bootstrap_theme']},
		'include_package_data':True,
		'data_files':[('extra/', ['cadnaPromise/extra/promise.h', 'cadnaPromise/extra/cadnaizer'])],
		'zip_safe':False,
		'entry_points':{'console_scripts': 
						['promise=cadnaPromise.run:runPromise',
						 'init-promise=cadnaPromise.install:initPromise',
						 'test-promise=cadnaPromise.run:runPromise_custom_test']
				}}


try:	
	setup(**setup_args)

except ext_errors as ext_reason:
    log.warning("The installation is not successful, please contact the maintenance team.")
