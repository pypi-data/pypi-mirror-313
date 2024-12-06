cadnaPromise
==============


.. image:: https://github.com/PEQUAN/cadnaPromise/actions/workflows/python-publish.yml/badge.svg
    :target: https://github.com/PEQUAN/cadnaPromise/actions/workflows/python-publish.yml
    :alt: Build


.. image:: https://static.pepy.tech/badge/cadnaPromise
    :target: https://github.com/PEQUAN/cadnaPromise
    :alt: Download Status


.. image:: https://img.shields.io/pypi/v/cadnaPromise?color=pink
    :target: setup.py
    :alt: Publish


.. image:: https://img.shields.io/badge/License-GPLv3-yellowgreen.svg
    :target: LICENSE
    :alt: License


.. image:: https://codecov.io/github/PEQUAN/cadnaPromise/graph/badge.svg?token=FLW73I2NAJ 
     :target: https://codecov.io/github/PEQUAN/cadnaPromise
     :alt: CodeCov

.. image:: https://readthedocs.org/projects/cadnapromise/badge/?version=latest
    :target: https://cadnapromise.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

--------
Install
--------

To install ``cadnaPromise``, simply use the pip command in terminal:  

.. parsed-literal::

  pip install cadnaPromise


after that, to activate the ``cadnaPromise``, use the command in terminal:

.. parsed-literal::

  init-promise


Check the if cadnaPromise is installed:

.. parsed-literal::

  promise --version

  


-------------
Dependencies
-------------

The installation of ``cadnaPromise`` requires the the following Python libraries: ``colorlog``, ``colorama``, ``pyyaml``, ``regex``.

The compiling of ``cadnaPromise`` requires ``g++``. Please ensure the installation of above libraries for a proper running of cadnaPromise.


-------------
Usage
-------------

In terminal, simply enter the command bellow: 

.. parsed-literal::

	get help:     promise --help | promise
	run program:  promise (hsd|hs|sd) [options]


Options:

.. parsed-literal::

  --help                        Show this screen.
  --conf CONF_FILE              get the configuration file [default: promise.yml]
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
  --version			show the version of cadnaPromise


-------------------
Acknowledgements
-------------------



``cadnaPromise`` is based on `Promise2 <https://gitlab.lip6.fr/hilaire/promise2>`_  (Hilaire et al), a full rewriting of the first PROMISE version (Picot et al).

This work was supported by the France 2030 NumPEx Exa-MA (ANR-22-EXNU-0002) project managed by the French National Research Agency (ANR).
``Promise2`` has been developed with the financial support of the COMET project Model-Based Condition Monitoring and Process Control Systems, hosted by the Materials Center Leoben Forschung GmbH.
