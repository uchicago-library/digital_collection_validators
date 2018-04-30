import os
import unittest
import tempfile
from unittest.mock import patch

# @mock.patch('proj1.listdir')
# class testPatch(self):
# 	def test_checkRoot():
# 		with patch('os.path.isfile', lambda x: True):
# 			self.assertTrue(checkRoot(self))

# creating a fixture
# pytestmark = pytest.mark.usefixtures('cleanDir')

class projTests(unittest.TestCase):
	def test_foo(self):
		self.assertTrue(True)
	
	def setUp(self):
		newPath = tempfile.mkdtemp()
		os.chdir(newPath)

	def test_starts_empty(self):
		assert os.listdir(os.getcwd()) == []

	def testCheckRoot(self):
		response = self.getcwd()
		self.assertEqual(re)

	# MVOLIDENTIFIER raises Error


	# FILECHOICES raises Error


	# checks whether directory exists


# 	def runTest(self):
# 		self.assertEqual(self, )


	def tearDown(self):
		self.dir.dispose()
		self.dir = None


# def suite():
# 	tests = ['xTestCase']
# 	return unittest.TestSuite(map(ProjTestCase))

if __name__ == '__main__':
	unittest.main()