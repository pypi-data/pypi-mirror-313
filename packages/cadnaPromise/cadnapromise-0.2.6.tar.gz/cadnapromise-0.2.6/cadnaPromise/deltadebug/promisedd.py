# coding=utf-8

"""This file is part of PROMISE.

	PROMISE is free software: you can redistribute it and/or modify it
	under the terms of the GNU Lesser General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	PROMISE is distributed in the hope that it will be useful, but WITHOUT
	ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
	or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
	Public License for more details.

	You should have received a copy of the GNU Lesser General Public
	License along with PROMISE. If not, see
	<http://www.gnu.org/licenses/>.

Promise v1 was written by Romain Picot
Promise v2 has been written from v1 by Thibault Hilaire and Sara Hoseininasab
	Sorbonne Université
	LIP6 (Computing Science Laboratory)
	Paris, France
Contact: thibault.hilaire@lip6.fr


File: DeltaDebug.py
Date: April 2020

	A custom DeltaDebug class, that inherits from DD class (from Zeller)

	© Thibault HILAIRE, April 2020
"""


from .dd import DD
from ..errors import PromiseCompilationError
from ..utils import pause
from ..logger import PrLogger

logger = PrLogger()


class PromiseDD(DD):
	"""Promise Delta Debug"""

	def __init__(self, pr, type1, type2, status, bar, path='', doPause=False, compileErrorPath=None):
		"""Create a Delta Debug object, with promise-dedicated test method
		Parameter:
		- pr: the Promise object of the project
		- type1, type2: (string) the two types uses for the delta-debug method
		(all the types initialy equal to types2 can be changed to type1)
		- status, bar: two tqdm objects (status and progress bar)
		- path: (string) path where put the generated files (compiled, run and tested)
			if empty, a temporary folder is used
		- doPause: (boolean) True if we pause after each dd iteratio"""
		self._status = status
		self._bar = bar
		self._type1 = type1
		self._type2 = type2
		self._pr = pr
		self._path = path
		self._pause = doPause
		self._initialTypes = dict(pr.typesDict)
		self._compileErrorPath = compileErrorPath
		super().__init__()

	def test(self, C):
		"""Test if the configuration
		Returns PASS, FAIL, or UNRESOLVED."""
		logger.debug('We test C=' + str(C))
		# change the types according to C
		self._pr.changeTypes(self._initialTypes)
		self._pr.changeSomeTypes(self._type1, C)
		# compile, run and get the result
		try:
			check = self._pr.compileAndRun(self._path, compilationErrorAsDebug=True, compileErrorPath=self._compileErrorPath)
			if self._pause:
				pause(self._status)
		except PromiseCompilationError:
			logger.debug('Compilation failed \U0001F44E')
			self._status.set_description_str('Compilation failed \U0001F44E')
			self._status.refresh()

			return DD.FAIL
		# update the status
		self._status.set_description_str('We test C=' + str(C) + (" \U0001F44D" if check else " \U0001F44E"))
		self._bar.update()
		return DD.PASS if check else DD.FAIL


	def run(self):
		"""run the Delta Debug algorithm
		Retuns what ddmax returns"""
		# run the dd
		deltas = self._pr.getTypesEqualTo(self._type2)
		t = self.ddmax(deltas)
		# set progress bar to 100%
		self._bar.total = self._bar.n
		self._bar.refresh()
		# return to the types given by dd algorithm
		self._pr.changeTypes(self._initialTypes)
		self._pr.changeSomeTypes(self._type1, list(set(deltas)-set(t)))
		logger.debug("DD algorithms returns : " + str(self._pr.typesDict))
