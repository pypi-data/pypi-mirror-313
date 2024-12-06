# -*- coding: utf-8 -*-
"""
Copyright 2019 David García Garzón

This file is part of back2back

back2back is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

back2back is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from  unittest import TestCase
import os

def assertXmlEqual(self, got, want):
	from lxml.doctestcompare import LXMLOutputChecker
	from doctest import Example

	checker = LXMLOutputChecker()
	if checker.check_output(want, got, 0):
		return
	message = checker.output_difference(Example("", want), got, 0)
	raise AssertionError(message)

TestCase.assertXmlEqual = assertXmlEqual

def differences(expected, result, diffbase=None):
	extension = os.path.splitext(result)[-1]

	with open(expected) as f:
		expectedContent = f.read()

	with open(result) as f:
		resultContent = f.read()

	try:
		assertXmlEqual(None, resultContent, expectedContent)
		return []
	except AssertionError as e:
		result = e.args
	return result

differences.extensions = [
	'.xml',
	]

def main():
	import sys
	diffs = differences(*sys.argv[1:])
	if not diffs : sys.stdout.write("Ok\n"); sys.exit(0)
	for d in diffs :
		print >> sys.stderr, d



