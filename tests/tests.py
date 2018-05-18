import os
import unittest
import argparse
import tempfile
import shutil
from dcv.proj1 import main, parseArgs, fileChoices, checkRoot, mvolIdentifier

# def main():
# 	sysDir = tempfile.gettempdir()
# 	testDir = os.path.join(sysDir, 'testdir')
# 	testDir = tempfile.mkdtemp(suffix=None, prefix=None, dir=None)
# 	altoDir = tempfile.mkdtemp(suffix=None, prefix='ALTO', dir= testDir)
# 	jpgDir = tempfile.mkdtemp(suffix=None, prefix='JPEG', dir= testDir)
# 	tifDir = tempfile.mkdtemp(suffix=None, prefix='TIFF', dir= testDir)

# 	tempfile.mkstemp(suffix='.xml', prefix='mvol-0004-1920-0108_0001', dir=altoDir)
# 	tempfile.mkstemp(suffix='.jpg', prefix='mvol-0004-1920-0108_0001', dir=jpgDir)
# 	tempfile.mkstemp(suffix='.tif', prefix='mvol-0004-1920-0108_0001', dir=tifDir)

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

		tempfile.mkstemp(suffix='.xml', prefix='mvol-0004-1920-0108_0001', dir=self.aDir)
		tempfile.mkstemp(suffix='.xml', prefix='mvol-0004-1920-0108_0002', dir=self.aDir)		
		tempfile.mkstemp(suffix='.jpg', prefix='mvol-0004-1920-0108_0001', dir=self.jDir)
		tempfile.mkstemp(suffix='.jpg', prefix='mvol-0004-1920-0108_0002', dir=self.jDir)
		tempfile.mkstemp(suffix='.tif', prefix='mvol-0004-1920-0108_0001', dir=self.tDir)
		tempfile.mkstemp(suffix='.tif', prefix='mvol-0004-1920-0108_0002', dir=self.tDir)

	# def test_main(self):
	# 	self.assertEqual(main(), 'ok')
	# 	self.assertEqual(main(), )

	def test_fileChoices(self):
		result = fileChoices(['.xml', '.dc.xml', '.pdf', '.struct.text', '.text'], self.mainDir)
		# assert result is {'dc.xml': 1, 'mets.xml': 1, 'pdf': 1, 'struct.txt': 1, 'txt': 1}
		self.assertEqual(fileChoices(['.xml'], self.aDir), {'xml': 1})
	def checkRoot(self):
		firstFunction = checkRoot()
		firstFunction.self.mainDir()
		assert frustration.status == 'changed correctly'
		result = checkRoot(self.mainDir)
		self.assertEqual(result, )
	def tearDown(self):
		shutil.rmtree(self.mainDir)

if __name__ == '__main__':
	unittest.main()
