#!/usr/bin/env python3
# coding=utf-8

# This file is part of PROMISE.
#
# 	PROMISE is free software: you can redistribute it and/or modify it
# 	under the terms of the GNU Lesser General Public License as
# 	published by the Free Software Foundation, either version 3 of the
# 	License, or (at your option) any later version.
#
# 	PROMISE is distributed in the hope that it will be useful, but WITHOUT
# 	ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# 	or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# 	Public License for more details.
#
# 	You should have received a copy of the GNU Lesser General Public
# 	License along with PROMISE. If not, see
# 	<http://www.gnu.org/licenses/>.
#
# Promise v1 was written by Romain Picot
# Promise v2 has been written from v1 by Thibault Hilaire and Sara Hoseininasab
# Promise v3 has been written from v2 by Xinye Chen, Thibault Hilaire and Fabienne JÉZÉQUEL
# Promise v3 enables version check, pip installing, arbitrary precision, etc., features.
# 	Sorbonne Université
# 	LIP6 (Computing Science Laboratory)
# 	Paris, France. Contact: xinyechenai@gmail.com, thibault.hilaire@lip6.fr, fabienne.jezequel@lip6.fr
#
# 	contain the entry function, called to run Promise
#
# 	© Thibault Hilaire and Fabienne JÉZÉQUEL, April 2024

# define in an explicit way for debugging
__doc__ = """
\U0001f918 cadnaPromise \U0001f918

Usage:
	runPromise --help
	runPromise (hsd|hs|sd) [options]

Options:
  -h --help                     Show this screen.
  --conf CONF_FILE              get the configuration file [default: promise.yml]
  --fp FPT_FILE             get the file for floating point number format [default: fp.json]
  --output OUTPUT               set the path of the output (where the result files are put)
  --verbosity VERBOSITY         set the verbosity (betwen 0  and 4 for very low level debug) [default: 1]
  --log LOGFILE                 set the log file (no log file if this is not defined)
  --verbosityLog VERBOSITY      set the verbosity of the log file
  --debug                       put intermediate files into `debug/` (and `compileErrors/` for compilation errrors) and display the execution trace when an error comes
  --run RUN                     file to be run
  --compile COMMAND             command to compile the code
  --files FILES                 list of files to be examined by Promise (by default, all the .cc files)
  --nbDigits DIGITS             general required number of digits
  --path PATH                   set the path of the project (by default, the current path)
  --pause                       do pause between steps
  --noParsing                   do not parse the C file (__PROMISE__ are replaced and that's all)
  --alias ALIAS                 allow aliases (examples "g++=g++-14") [default:""]
  hsd                           Half/Single/Double mixed-precision
  hs                            Half/Single mixed-precision
  sd                            Single/Double mixed-precision

  
"""

import os
from os.path import join
import sys
from collections import Counter

from .promise import Promise
from .utils import parseOptions, PromiseError, getYMLOptions, Timing, pause, commaAnd
from .utils import customArgParser, __params__, getFPM, sort_precs, update_types, get_version
from .logger import PrLogger
from .prfile import PrFile




# types handle by cadnaPromise
_typeNames = {'b':'bfloat16', 
			  'h': 'Half', 
			  's': 'Single', 
			  'd': 'Double', 
			  'q': 'Quad', 
			  'o': 'Octuple'
			  }

_types = {'b': 'flx::floatx<8, 7>', 
		  'h': 'half_float::half', 
		  's': 'float', 
		  'd': 'double', 
		  'q': 'float128',
		  'o': 'flx::floatx<19, 236>',
		 }


def runPromise(argv=None):
	"""This function is registered (in setup.py) as an entry_point
	argv is used for the unit tests"""

	# reset the logger and get a new instance
	logger = PrLogger()
	
	# reset the handlers, in case of running runPromise several times (otherwise, the log files are still open)
	
	displayTrace = False
	EARLY_SROP = False
		
	try:
		# import docopt
		# get the options from command line and yml file
		# print("__params__ 1:", __params__)

		if argv is None:
			if '--help' in sys.argv[1:] or len(sys.argv[1:]) == 0:
				print(__doc__)
				return
		else:
			if '--help' in argv or len(argv) == 0:
				print(__doc__)
				return

		args = customArgParser(sys.argv[1:] if argv is None else argv, __params__)      # parse the command line
	
		if argv is not None:
			if '--version' in argv or '--v' in argv:
				EARLY_SROP = True

		else:
			if '--version' in sys.argv[1:] or '--v' in sys.argv[1:]:
				EARLY_SROP = True

		logger.reset()
		# args = docopt.docopt(__doc__, argv=sys.argv[1:] if argv is None else argv)      # parse the command line
		# print("args:", args)
		displayTrace = args['--debug']

		logger.configureLogger(args)                                                   # configure the logger
		
		if EARLY_SROP:
			logger.message("cadnaPromise version " + get_version(
				os.path.dirname(os.path.realpath(__file__))+'/__init__.py') + ' (cadna version 3.1.12)')
	 
			logger.message("Copyright (c) 2024, GNU General Public License v3.0")
			logger.message(
				f"This work was supported by the France 2030 NumPEx Exa-MA (ANR-22-EXNU-0002) project managed by the French National Research Agency (ANR)."
				)
				
			return 

		options = getYMLOptions(args)                                           # get the options from the yml file

		# print("options:", options)
		method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias = parseOptions(options)    # parse the options

		# print("__params__ 2:", __params__)
		
		fpfmt = getFPM(args)
		method = sort_precs(method, fpfmt)
		# print('fpfmt:', fpfmt)
		# print("method:", method)

		types, typeNames = update_types(_types, _typeNames, fpfmt)
		# print("types, typeNames:", types, typeNames)

		compiler = 'g++'

		if isinstance(alias, dict):
			if alias == {}:
				curr_loc = os.path.dirname(os.path.realpath(__file__))

				cachePath = "/cache"
				if os.path.exists(curr_loc + cachePath):
					if os.path.isfile(curr_loc + cachePath + '/CXX.txt'):
						with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
							compiler = file.read().replace('\n', '')
							print('check compilers:', compiler)
			
			elif alias.get('g++', False):
				compiler = alias['g++']

		else:
			compiler = alias
			alias = {}
			
		if compiler != 'g++' and compiler is not None:
			alias['g++'] = compiler
		

		logger.message("\U0001f918 cadnaPromise \U0001f918")
		logger.message("Using the compiler: {}".format(compiler))

		PrFile.setCustom(typeCustom)
		compileErrorPath = join(path, 'compileErrors') if args['--debug'] else None
		tempPath = join(path, 'debug') if args['--debug'] else None

		# run with timing
		with Timing() as timing:
			# create Promise object
			pr = Promise(path, files, run, nbDigits, compileLines, parsing=not args['--noParsing'], alias=alias)

			# display general infos
			logger.info("We are working with %d file%s and %d different types" %
			            (pr.nbFiles, ('' if pr.nbFiles < 2 else 's'), pr.nbVariables))
			logger.info(pr.expectation())

			# debug the files
			if args['--debug']:
				pr.exportParsedFiles(tempPath)

			# get the cadna reference
			highest = types['q'] if 'q' in method else types['d']
			# print("highest:", highest)
			pr.changeSameType(highest)
			logger.step("Get a reference result with cadna (%s)" % highest)
			pr.compileAndRun(tempPath, cadna=True)
			if args['--pause']:
				pause()

			# try with the highest precision
			logger.step("Check with highest format (%s)" % typeNames[method[-1]])
			pr.changeSameType(types[method[-1]])
			
			if not pr.compileAndRun(tempPath):
				pr.changeSameType(highest)
				raise PromiseError("You should lower your expectation, it doesn't work with " + typeNames[method[-1]])
			
			if args['--pause']:
				pause()
			

			# do the Delta-Debug passes ('s','d' and then 'h','s' when method is 'hsd' for example)
			for lo, hi in reversed(list(zip(method, method[1:]))):
				logger.step("Delta-Debug %s/%s" % (typeNames[lo], typeNames[hi]))
				res = pr.runDeltaDebug(types[lo], types[hi], tempPath, args['--pause'], compileErrorPath)
				# stop if the DeltaDebug is not successful
				if not res:
					break

		# export the output
		if argv is None:
			pr.exportFinalResult(outputPath)


	except PromiseError as e:
		logger.error(e, exc_info=displayTrace)

	else:
		if timing:
			# display the number of each type
			count = Counter(pr.typesDict.values())  # count the nb of each type (result is a dictionary type:nb)
			li = ["%dx %s" % (v, k) for k, v in count.items()]
			logger.message("The final result contains %s.", commaAnd(li))
			logger.debug("Final types:\n" + pr.strResult())

			# display the stats
			logger.message("It tooks %.2fs", timing.timing)
			logger.message("\U0001F449 %d compilations (%d failed) for %.2fs", *pr.compilations)
			logger.message("\U0001F449 %d executions   (%d failed) for %.2fs", *pr.executions)

			logger.reset()
			return pr.setPerType()
		

	logger.reset()



def runPromise_custom_test(argv=None):
	"""This function is registered (in setup.py) as an entry_point
	argv is used for the unit tests"""

	# reset the logger and get a new instance
	logger = PrLogger()
	logger.reset()
	# reset the handlers, in case of running runPromise several times (otherwise, the log files are still open)
	
	displayTrace = False
	EARLY_SROP = False

	try:
		# import docopt
		# get the options from command line and yml file
		# print("__params__ 1:", __params__)
		args = customArgParser(sys.argv[1:] if argv is None else argv, __params__)      # parse the command line
		if argv is not None:
			if '--version' in argv or '--v' in argv:
				EARLY_SROP = True

		else:
			if '--version' in sys.argv[1:] or '--v' in sys.argv[1:]:
				EARLY_SROP = True

		# args = docopt.docopt(__doc__, argv=sys.argv[1:] if argv is None else argv)      # parse the command line
		# print("args:", args)
		displayTrace = args['--debug']

		logger.configureLogger(args)                                                   # configure the logger
		options = getYMLOptions(args)                                           # get the options from the yml file
		
		
		# print("options:", options)
		method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias = parseOptions(options)    # parse the options

		# print("__params__ 2:", __params__)
		
		fpfmt = getFPM(args)
		method = sort_precs(method, fpfmt)
		# print('fpfmt:', fpfmt)
		# print("method:", method)

		types, typeNames = update_types(_types, _typeNames, fpfmt)
		# print("types, typeNames:", types, typeNames)

		compiler = 'g++'
		
		if alias == {}:
			curr_loc = os.path.dirname(os.path.realpath(__file__))

			cachePath = "/cache"
			if os.path.exists(curr_loc + cachePath):
				if os.path.isfile(curr_loc + cachePath + '/.CXX.txt'):
					with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
						compiler = file.read()
	
					if compiler != 'g++' and compiler is not None:
						alias = {'--alias':compiler}

		if EARLY_SROP:
			logger.message("cadnaPromise version " + args['--version'])
			return 
		
		logger.message("\U0001f918 cadnaPromise \U0001f918")
		logger.message("Using the compiler: {}".format(compiler))

		PrFile.setCustom(typeCustom)
		compileErrorPath = join(path, 'compileErrors') if args['--debug'] else None
		tempPath = join(path, 'debug') if args['--debug'] else None

		# run with timing
		with Timing() as timing:
			# create Promise object
			pr = Promise(path, files, run, nbDigits, compileLines, parsing=not args['--noParsing'], alias=alias)

			# display general infos
			logger.info("We are working with %d file%s and %d different types" %
			            (pr.nbFiles, ('' if pr.nbFiles < 2 else 's'), pr.nbVariables))
			logger.info(pr.expectation())

			# debug the files
			if args['--debug']:
				pr.exportParsedFiles(tempPath)

			# get the cadna reference
			highest = types['q'] if 'q' in method else types['d']
			# print("highest:", highest)
			pr.changeSameType(highest)
			logger.step("Get a reference result with cadna (%s)" % highest)
			pr.compileAndRun(tempPath, cadna=True)
			if args['--pause']:
				pause()

			# try with the highest precision
			logger.step("Check with highest format (%s)" % typeNames[method[-1]])
			pr.changeSameType(types[method[-1]])
			
			if not pr.compileAndRun(tempPath):
				pr.changeSameType(highest)
				raise PromiseError("You should lower your expectation, it doesn't work with " + typeNames[method[-1]])
			
			if args['--pause']:
				pause()
			

			# do the Delta-Debug passes ('s','d' and then 'h','s' when method is 'hsd' for example)
			for lo, hi in reversed(list(zip(method, method[1:]))):
				logger.step("Delta-Debug %s/%s" % (typeNames[lo], typeNames[hi]))
				res = pr.runDeltaDebug(types[lo], types[hi], tempPath, args['--pause'], compileErrorPath)
				# stop if the DeltaDebug is not successful
				if not res:
					break

		# export the output
		if argv is None:
			pr.exportFinalResult(outputPath)


	except PromiseError as e:
		logger.error(e, exc_info=displayTrace)

	else:
		if timing:
			# display the number of each type
			count = Counter(pr.typesDict.values())  # count the nb of each type (result is a dictionary type:nb)
			li = ["%dx %s" % (v, k) for k, v in count.items()]
			logger.message("The final result contains %s.", commaAnd(li))
			logger.debug("Final types:\n" + pr.strResult())

			# display the stats
			logger.message("It tooks %.2fs", timing.timing)
			logger.message("\U0001F449 %d compilations (%d failed) for %.2fs", *pr.compilations)
			logger.message("\U0001F449 %d executions   (%d failed) for %.2fs", *pr.executions)

			logger.reset()
			return pr.setPerType()
		

	logger.reset()




if __name__ == "__main__":
	runPromise()



