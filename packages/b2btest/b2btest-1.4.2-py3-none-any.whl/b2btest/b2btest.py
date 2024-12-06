import os, sys, string
import subprocess
from consolemsg import step, fail, success, error, warn, printStdError, color, u
try: from pathlib2 import Path
except ImportError: from pathlib import Path
from .entrypoints import load_entry_points_group

def printcolor(colorcode, message):
	printStdError(color(colorcode, message))

class Differ(object):

	methods = load_entry_points_group('back2back.diff')
	extensions=None

	@classmethod
	def _fillExtensions(cls):
		if cls.extensions is not None: return
		cls.extensions = {}
		for name, typediffer in cls.methods.items():
			if not hasattr(typediffer, 'extensions'):
				continue
			cls.extensions.update((
				(extension, typediffer)
				for extension in typediffer.extensions
			))

	@classmethod
	def extraExtensions(cls, extensions):
		cls._fillExtensions()
		cls.extensions.update((
			(extension, cls.methods[pluginname])
			for extension, pluginname in extensions.items()
			))

	@classmethod
	def diff(cls, expected, result, diffbase):
		cls._fillExtensions()
		extension = os.path.splitext(result)[-1]
		diff = cls.extensions.get(extension, cls.methods['text'])
		return diff(expected, result, diffbase)


def diffbyextension(expected, result, diffbase):
	return Differ.diff(expected, result, diffbase)
	self = diffbyextension
	if not hasattr(self, 'methods'):
		self.methods = load_entry_points_group('back2back.diff')
	extensionMap = {
		".wav" : self.methods['audio'],
		".txt" : self.methods['text'],
		".clamnetwork" : self.methods['xml'],
		".xml" : self.methods['xml'],
		".ttl" : self.methods['text'],
	}

	extension = os.path.splitext(result)[-1]
	diff = extensionMap.get(extension, self.methods['text'])
	return diff(expected, result, diffbase)


try:
	FileNotFoundError
except NameError:
	FileNotFoundError=IOError


def diff_files(expected, result, diffbase) :
	if not os.access(result, os.R_OK):
		error("Result file not found: {}".format(result))
		return ["Result was not generated: '%s'"%result]
	if not os.access(expected, os.R_OK):
		error("Expectation file not found for: {}".format(result))
		return ["No expectation for the output. First run? "
			"Check the results and accept them with the --accept option."]

	return diffbyextension(expected, result, diffbase)


def archSuffix() :
	return os.popen('uname -m').read().strip()

def expectedArchName(base, extension='.wav') :
	suffix_arch = archSuffix()
	return base+'_expected_' + suffix_arch + extension

def expectedName(base, extension) :
	"""Returns the expected wav name.
	If an architecture specific output already exists, it will use it.
	"""
	expected = expectedArchName(base, extension)
	if os.access(expected,os.R_OK): return expected

	return base+'_expected'+extension

def badResultName(base, extension = '.wav') :
	return base+'_result'+extension

def diffBaseName(base) :
	return base+'_diff'

def prefix(datapath, case, output) :
	outputBasename = os.path.splitext(os.path.basename(output))[0]
	return os.path.join(datapath, case + '_' + outputBasename )

def accept(datapath, back2BackCases, archSpecific=False, cases=[]) :
	remainingCases = cases[:]
	for case, command, outputs in back2BackCases :
		if cases and case not in cases : continue
		if cases : remainingCases.remove(case)
		for output in outputs :

			extension = os.path.splitext(output)[-1]
			base = prefix(datapath, case, output)
			badResult = badResultName(base, extension)
			if not os.access(badResult, os.R_OK) : continue
			warn("Accepting {}".format(badResult))

			if archSpecific :
				os.rename(badResult, expectedArchName(base, extension))
			else :
				os.rename(badResult, expectedName(base, extension))
	if remainingCases :
		warn("No such test cases: {}".format(
			", ".join("'%s'"%case for case in remainingCases)))

def removeIfExists(filename) :
	try: os.remove(filename)
	except: pass

def passB2BTest(datapath, case, command, outputs):
	step("Test: %s Command: '%s'"%(case,command))
	for output in outputs :
		removeIfExists(output)
	try :
		commandError = subprocess.call(command, shell=True)
		if commandError :
			return ["Command failed with return code %i:\n'%s'"%(commandError,command)]
	except OSError as e :
		return ["Unable to run command: '%s'"%(command)]
	failures = []
	for output in outputs :
		extension = os.path.splitext(output)[-1]
		base = prefix(datapath, case, output)
		expected = expectedName(base, extension)
		diffbase = diffBaseName(base)
		difference = diff_files(expected, output, diffbase)
		#diffbase = diffbase+'.wav'
		diffbase = diffbase + extension

		if not difference:
			printcolor('32;1', " Passed")
			removeIfExists(diffbase)
			removeIfExists(diffbase+'.png')
			removeIfExists(badResultName(base,extension))
		else:
			printcolor('31;1', " Failed")
			os.system('cp %s %s' % (output, badResultName(base,extension)) )
			formatted = [ '\n\t  '.join(item.split('\n')) for item in difference]
			failures.append("Output '%s':\n%s"%(base, '\n'.join(['\t- %s'%item for item in formatted])))
		removeIfExists(output)
	return failures

def passB2BTests(datapath, back2BackCases, extensions) :
	Differ.extraExtensions(extensions)
		
	failedCases = []
	for case, command, outputs in back2BackCases :
		failures = passB2BTest(datapath, case, command, outputs)
		if not failures: continue
		failedCases+=[(case, failures)]

	sys.stderr.write("Summary:\n")
	printcolor('32;1', '%i passed cases'%(len(back2BackCases)-len(failedCases)))

	if not failedCases : return True

	printcolor('31;1', '%i failed cases!'%len(failedCases))
	for case, msgs in failedCases :
		sys.stderr.write(case + " :\n")
		for msg in msgs :
			sys.stderr.write( "\t%s\n"%msg)
	return False

help ="""
To run the tests call this script without parameters.
	./back2back

Failed cases will generate *_result.ext and *_diff.ext
files for each missmatching output, containing the
obtained output and the difference with the expected one.

You can run specific test cases indicating additional
parameter.

	./back2back case1 case2

If some test fail but you want to accept the new results
just call:
	./back2back --accept case1 case2
where case1 and case2 are the cases to be accepted.

To know which are the available cases:
	./back2back --list

To accept any failing cases (USE IT WITH CARE) call:
	./back2back --acceptall

To accept some results but just for a given architecture,
due to floating point missmatches, use:
	./back2back --arch --accept case1 case2
"""

def _caseList(cases) :
	return "".join(["\t"+case+"\n" for case in cases])



def runBack2BackProgram(datapath, argv, back2BackCases, chosenCases=[], help=help, extensions={}) :

	"--help" not in argv or fail(help, 0)

	architectureSpecific = "--arch" in argv
	if architectureSpecific : argv.remove("--arch")

	os.access( datapath, os.X_OK ) or fail(
		"Datapath at '%s' not available. "%datapath +
		"Check the back 2 back script on information on how to obtain it.")

	availableCases = [case for case, command, outputs in back2BackCases]
	chosenNotAvailable = set(chosenCases) - set(availableCases)
	if chosenNotAvailable:
		sys.stderr.write("Indicated cases are not availabe:\n")
		for case in chosenNotAvailable:
			sys.stderr.write("- {}\n".format(case))

	if "--list" in argv or chosenNotAvailable:
		sys.stdout.write("Available cases:\n")
		sys.stdout.write(_caseList(availableCases))
		sys.exit()

	if "--accept" in argv :
		cases = argv[argv.index("--accept")+1:]
		cases or fail(
			"Option --accept needs a set of cases to accept.\n"
			"Available cases:\n"+
			_caseList((case for case, command, outputs in back2BackCases))
			)
		unsupportedCases = set(cases).difference(set(availableCases))
		unsupportedCases and fail(
			"The following specified cases are not available:\n" +
			_caseList(unsupportedCases) +
			"Try with:\n" +
			_caseList(availableCases)
			)
		accept(datapath, back2BackCases, architectureSpecific, cases)
		sys.exit()

	if "--acceptall" in argv :
		warn("Accepting any faling case")
		accept(datapath, back2BackCases, architectureSpecific)
		sys.exit()

	print("chosenCases", chosenCases)
	if chosenCases:
		back2BackCases = [
			(case, command, outputs)
			for case, command, outputs
			in back2BackCases
			if case in chosenCases
		]
	passB2BTests(datapath, back2BackCases, extensions=extensions) or fail("Tests not passed")


def assertB2BEqual(self, result, expectedFile=None, resultFile=None):

	def safeRemove(filename):
		try: Path(filename).unlink()
		except: pass

	def makedirs(dirname):
		Path(dirname).mkdir(parents=True, exist_ok=True)

	def read(filename):
		return Path(filename).read_text(encoding='utf8')

	def write(filename, content):
		return Path(filename).write_text(content,encoding='utf8')

	def writeResultsOrAccept():
		accepting = hasattr(self, 'acceptMode') and self.acceptMode
		if not accepting:
			write(resultFile, result)
			return
		write(expectedFile, result)
		safeRemove(resultFile)
		raise Warning("Accepting new data for '{}'"
			.format(expectedFile))

	b2bdatapath = Path(self.b2bdatapath)

	result = u(result)

	if resultFile is None:
		makedirs(b2bdatapath)
		resultFile = b2bdatapath / (self.id()+"-result")
	if expectedFile is None:
		makedirs(b2bdatapath)
		expectedFile = b2bdatapath / (self.id()+"-expected")

	try:
		expectation = read(expectedFile)
	except IOError as error:
		writeResultsOrAccept()
		self.fail("No expectation found, please, check and accept '{}'"
			.format(resultFile))

	try:
		self.assertEqual(result, expectation)
	except AssertionError:
		writeResultsOrAccept()
		raise AssertionError("Differing content: '{}'".format(resultFile))

	safeRemove(resultFile)


def assertCommandB2BEqual(self, command, *outputs):
	commandError = subprocess.call(command, shell=True)
	if commandError:
		self.fail("Command failed with return code {}:\n'{}'"
			.format(commandError, command))
	return


import unittest
unittest.TestCase.assertB2BEqual = assertB2BEqual
unittest.TestCase.assertCommandB2BEqual = assertCommandB2BEqual




#vim: noet sw=4 ts=4
