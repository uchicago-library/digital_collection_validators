import pytest
import tempfile
import os

"""Work in progres"""

# creating a fixture
def cleanDir():
	newPath = tempfile.mkdtemp()
	os.chdir(newPath)

pytestmark = pytest.mark.usefixtures('cleanDir')

def test_doesSomething(doesSomething):
	response, msg = doesSomething.ehlo(0)
	assert response == 250
	assert 0


class ProjTestCase(object):
	def test_starts_empty(self):
		assert os.listdir(os.getcwd()) == []

	def setUp(self):
		self.dir = proj1(newPath)

# 	def runTest(self):
# 		self.assertEqual(self, )

# 	def tearDown(self):
# 		self.dir.dispose()
# 		self.dir = None


# def suite():
# 	tests = ['xTestCase']
# 	return unittest.TestSuite(map(ProjTestCase))



if __name__ == '__main__':
	unittest.main()