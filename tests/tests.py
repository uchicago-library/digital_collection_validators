import os
import unittest
import argparse
import tempfile
import shutil
import sys
from dcv.proj1 import main, parseArgs, fileChoices, checkRoot, mvolIdentifier

# def main():
# 	def list_files(startpath):
# 		for root, dirs, files in os.walk(startpath):
# 			level = root.replace(startpath, '').count(os.sep)
# 			indent = ' ' * 4 * (level)
# 			print('{}{}/'.format(indent, os.path.basename(root)))
# 			subindent = ' ' * 4 * (level + 1)
# 			for f in files:
# 				print('{}{}'.format(subindent, f))
# 	list_files(testDir)
	  

class projTests(unittest.TestCase):

	def setUp(self):
		'''
		Create a temporary dir, add 3 subdirs, 5 files.
		Within subdirs, add 2 files (different extensions)
		'''
		sysDir = tempfile.gettempdir()
		testDir = os.path.join(sysDir, 'testdir')
		self.mainDir = tempfile.mkdtemp(suffix=None, prefix=None, dir=None)
		self.aDir = tempfile.mkdtemp(suffix=None, prefix='ALTO', dir= self.mainDir)
		self.jDir = tempfile.mkdtemp(suffix=None, prefix='JPEG', dir= self.mainDir)
		self.tDir = tempfile.mkdtemp(suffix=None, prefix='TIFF', dir= self.mainDir)


		tempfile.mkstemp(suffix='.xml', prefix='mvol-0004-1922-0108_0001', dir=self.mainDir)
		# break with out of order ALTO
		tempfile.mkstemp(suffix='.xml', prefix='mvol-0004-1922-0108_0002', dir=self.aDir)		
		tempfile.mkstemp(suffix='.jpg', prefix='mvol-0004-1922-0108_0001', dir=self.jDir)
		tempfile.mkstemp(suffix='.jpg', prefix='mvol-0004-1922-0108_0002', dir=self.jDir)
		tempfile.mkstemp(suffix='.tif', prefix='mvol-0004-1922-0108_0001', dir=self.tDir)
		tempfile.mkstemp(suffix='.tif', prefix='mvol-0004-1922-0108_0002', dir=self.tDir)

	def test_stdout(self):
		class MyOutput(object):
			def __init__(self):
				self.data = []
			def write(self, s):
				self.data.append(s)
			def __str__(self):
				return "".join(self.data)

		stdout_org = sys.stdout
		my_stdout = MyOutput()
		try:
			sys.stdout = my_stdout
			fn_print(2)
		finally:
			sys.stdout = stdout_org
		self.assertEquals( str(my_stdout), "abab\n")

	def test_fileChoices(self):
		result = fileChoices(['.xml'], self.aDir)['xml']
		self.assertEqual(result, 1)

	def checkRoot(self):
		firstFunction = checkRoot()
		firstFunction.self.mainDir()
		assert frustration.status == 'changed correctly'
		result = checkRoot(self.mainDir)
		# self.assertEqual(result, ) test for a console logged item

	def tearDown(self):
		try:
			shutil.rmtree(self.mainDir)
			shutil.rmtree(self.aDir)
			shutil.rmtree(self.jDir)
			shutil.rmtree(self.tDir)
			os.remove(os.getcwd())
		except IOError as e:
			print('IOError')
		else:
			os.remove(os.getcwd())

if __name__ == '__main__':
	unittest.main()
