import os
import unittest
import tempfile


# @mock.patch('proj1.listdir')
# class testPatch(self):
# 	def test_checkRoot():
# 		with patch('os.path.isfile', lambda x: True):
# 			self.assertTrue(checkRoot(self))

# creating a fixture
# pytestmark = pytest.mark.usefixtures('cleanDir')

subdirFiles = ['mvol-0004-1920-0320_0001.xml', 'mvol-0004-1920-0320_0002.xml', 'mvol-0004-1920-0320_0003.xml']



class projTests(unittest.TestCase):
	def setUp(self):
		newPath = tempfile.mkdtemp()
		os.chdir(newPath)

	def test_checkRoot(self):


	# MVOLIDENTIFIER raises Error
	def test_mvolIdentifier(self):
		test_object = subdirFiles
		test_


	# FILECHOICES raises Error
	def test_fileChoices(self):


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