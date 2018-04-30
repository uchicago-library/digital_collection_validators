import argparse
import os
# import traceback
# import sys
import logging
import time
from os import _exit

errorLogs = []

def checkRoot(r): 
	"""Determines the proper number of subdirectories and files.
	
	Checks for 3 subdirs (ALTO, JPEG, TIFF) and 5 files (xml, pdf, txt) at the top-level of the input directory.
	
	:param generator r: top-level directory of input
	:rtype None 
	"""
	dirNum, fileNum = 0, 0
	rIter = os.scandir(r)
	rList = []

	try:
		while True:
			elem = next(rIter)
			if elem.is_dir():
				dirNum += 1
			elif elem.is_file():
				fileNum += 1
				rList.append(elem)

	except StopIteration:
		pass

	extDict = fileChoices(['dc.xml', 'struct.txt', 'mets.xml', 'txt', 'pdf'], rList, os.path.basename(r))

	if not all(value == 1 for value in extDict.values()):
		errorLogs.append('There is a missing file type from the root directory. Please refer to the Campus Pub \
			spec sheet for the required OCR data formats.')	
	elif dirNum != 3 or fileNum != 5:
		errorLogs.append('This directory does not have 3 subdirectories and 5 files.')

def mvolIdentifier(subdirList, subdirName):
	"""Evaluates whether 1) all mvol identifiers match and 2) their pagination is consistent
	
	Selects the identifier and ensures they all match.

	Appends last 4 digits of each mvol and ensures that there aren't any missing pages 
	in a recursive function checkPagination. 

	func checkPagination confirms the subdirectory's pagination monotonically increases or decreases.

	:param list subdirList: an os.listdir of strings
	:param str subdirName: name of subdirectory
	:rtype None
	""" 
	fullMvol = []
	pagination = []

	for s in subdirList:
		# if s.is_dir():
		# 	parser.error('There is a directory named {} in folder {}'.format(s, subdirName))
		fullMvol.append(os.path.basename(s).split('_', 1)[0])
		pagination.append(os.path.basename(s).split('_', 1)[1][:4])

	def checkPagination(pList, d):
		if len(pList) == 1:
			return True
		if abs(int(pList[-1]) - int(pList[-2])) != 1:
			errorLogs.append('The pagination does not increase or decrease by 1 in {}.'.format(d))
		checkPagination(pList[:-1], d)

	if len(set(fullMvol)) != 1:
		errorLogs.append('An mvol identifier in folder {} is inconsistent with the rest.'.format(subdirName))

	checkPagination(pagination, subdirName)

def fileChoices(fType, fList, d):
	"""Traverses a list of files and evaluates whether they all match a file extension.
	
	:param array fType: a list of string of possible extensions a file can be, depending on its directory.
	:param arr fList: a list of child files in a directory.
	:param [directory]
	"""
	extDict = {}
	for f in fList:
		# if len(os.path.basename(f).split('.', 1)) <= 2:
		# 	parser.error('something aint right')
		ext = os.path.basename(f).split('.', 1)[1:][0]
		if ext not in fType:
			errorLogs.append('A file in folder {} does not end with {}.'.format(d, fType))
		if ext in extDict:
			extDict[ext] += 1
		else:
			extDict[ext] = 1
	return extDict
	
def main():
	parser = argparse.ArgumentParser(description='Checks OCR directory')
	parser.add_argument(
		'-dir', '--directory', action='store', required=True, \
		default='/tmp/non_existent_dir', help='Input OCR data directory path')
	args = parser.parse_args()

	# logger = logging.getLogger('validator_errors')
	# logger.setLevel(logging.DEBUG)
	# def logging(arg):
	# 	while not arg[;]

	if os.path.isdir(args.directory):
		pass
	else:
		parser.error('{} is an invalid directory. Please input an existing directory.'.format(args.directory))

	try:
		directoryTree = os.walk(args.directory)
		checkRoot(args.directory)
		for root, dirs, files in directoryTree:
			for d in dirs:
				path = os.path.join(root, d)
				if d == 'ALTO':
					numAlto = fileChoices(['xml'], os.listdir(path), d)['xml']
					mvolIdentifier(os.listdir(path), d)
				elif d == 'JPEG':
					numJPEG = fileChoices(['jpg'], os.listdir(path), d)['jpg']
					mvolIdentifier(os.listdir(path), d)
				elif d == 'TIFF':
					numTif = fileChoices(['tif'], os.listdir(path), d)['tif']
					mvolIdentifier(os.listdir(path), d)
				else:
					errorLogs.append('Please remove the folder that is not ALTO, JPEG, or TIFF. \
						Note: PDF should not have a folder.')
		if (numAlto * 3) != numAlto + numJPEG + numTif:
			errorLogs.append('The number of files in the subdirectories is inconsistent.')

		localTime = time.localtime()
		currentTime = time.strftime('%I:%M%p on %b %d, %Y', localTime)
		if len(errorLogs) == 0:
			print(' -------------- RESULTS FROM VALIDATOR TOOL -------------- ')
			print('            Test run', currentTime, '          ')
			print('               OCR data passed all tests!')
		else:
			print(' -------------- RESULTS FROM VALIDATOR TOOL -------------- ')
			print('            Test', currentTime, '          ')
			print('\n'.join([error for error in errorLogs]))
		return 0
	except OSError as err:
		print("OS error: {0}".format(err))
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	_exit(main())


''' ALTERNATIVE FOR OOP VERSION '''

# import argparse

# class MyClass(object):
#   def __init__(self, foo, bar):
#     self.foo = foo
#     self.bar = bar

#   def Print(self):
#     print self.foo
#     print self.bar

# def main():
#   parser = argparse.ArgumentParser()
#   parser.add_argument('foo')
#   parser.add_argument('bar')
#   args = parser.parse_args()
#   c1 = MyClass(args.foo, args.bar)
#   args_dict = vars(args)
#   c2 = MyClass(**args_dict)
