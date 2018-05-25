import os
import time
import sys
import argparse
from os import _exit

''' TO DO - 5/25 ----------------------------------------
	- each subfunction returns a tuple
	- in that subfunction, each error is added to a tuple
	- that tuple is recursively saved
	- and returned
	- to append to longer errorLogs in main
'''

def checkRoot(r, rootLog): 
	"""Determines the proper number of subdirectories and files.
	Checks for 3 subdirs (ALTO, JPEG, TIFF) and 5 files (xml, pdf, txt) at the top-level of the input directory.
	:param generator r: top-level directory of input
	:rtype None 
	"""
	rChoices = ['dc.xml', 'struct.txt', 'mets.xml', 'txt', 'pdf']
	dirNum, fileNum = 0, 0
	rIter = os.scandir(r)
	rList = []
	mvolIdentifierSet = set()

	for elem in rIter:
		if elem.is_dir():
			dirNum += 1
		elif elem.is_file():
			fileNum += 1
			rList.append(elem)
			mvolIdentifierSet.add(os.path.basename(elem).split('.', 1)[0])

	extensionDict, evalErrors = evaluateFileNames(rChoices, rList, ())[0], evaluateFileNames(rChoices, rList, ())[1]
	print(type(evalErrors)) # must change evalErrors so it's also a tuple
	rootLog += (evalErrors)

	if len(mvolIdentifierSet) != 1:
		rootLog = rootLog + ('The mvol identifiers of files in the root directory require uniformity.')
	if dirNum != 3 or fileNum != 5:
		rootLog += ('The root directory does not have 3 subdirectories and 5 files.')
	elif not all(value == 1 for value in extensionDict.values()):
		rootLog += ('There is a missing file type from the root directory. Please refer ' \
			'to the Campus Pub spec sheet for the required OCR data formats.')
	return rootLog

def evaluateFileNames(fType, d, newErrors):
	"""Traverses a list of files and evaluates whether they all match a file extension.
	:param array fType: a list of expected file extensions (str)
	:param generator d: directory of files
	:rtype: None
	"""
	if isinstance(d, (list,)):
		fList = d
		d = 'root'
	else:
		fList = os.scandir(d)
	extDict = {}
	for f in fList:
		if f.is_dir():
			newErrors += ('Please remove the nested directory "{}" in {}.'.format(os.path.basename(f), d))
		else:
			ext = os.path.basename(f).split('.', 1)[1:][0]
			if ext not in fType:
				newErrors += ('A file in folder {} does not end with {}.'.format(d, fType))
			if ext in extDict:
				extDict[ext] += 1
			else:
				extDict[ext] = 1
	print(type(newErrors))
	return (extDict, newErrors)

def identifyMvol(r, mvolLog):
	"""Evaluates whether 1) all mvol identifiers match and 2) their pagination is consistent
	func checkPagination confirms the subdirectory's pagination monotonically increases or decreases.
	:param generator r: directory of files
	:rtype: None
	""" 
	subdirList = os.scandir(r)
	fullMvol = []
	pagination = []

	for s in subdirList:
		if s.is_file():
			fullMvol.append(os.path.basename(s).split('_', 1)[0])
			pagination.append(os.path.basename(s).split('_', 1)[1][:4])

	def countPagination(pList, d, newErrors):
		if len(pList) == 1:
			return newErrors
		if abs(int(pList[-1]) - int(pList[-2])) != 1:
			newErrors += ('The pagination does not increase or decrease by 1 in {}.'.format(d))
		countPagination(pList[:-1], d, newErrors)

	mvolLog += (countPagination(pagination, r, ()))

	if len(set(fullMvol)) != 1:
		mvolLog += ('An mvol identifier in folder {} is inconsistent with the rest.'.format(r))
	return mvolLog

def buildParser(args):
	parser = argparse.ArgumentParser(description='Checks OCR directory')
	parser.add_argument(
		'-dir', '--directory', action='store', required=True, default=os.getcwd(), help='Input OCR data directory path')
	return parser.parse_args(args)

def checkDirectory(r, dList, pName, checked, newErrors):
	"""Traverses a directory, counts its files, and calls functions on files
	:param generator r: directory
	:param list dList: list of expected extension objects, acceptableDirs
	:param str pName: name of directory
	"""
	if checked:
		return newErrors
	if len(dList) == 1 and dList[0]['name'] != pName:
		newErrors = newErrors + ('Please remove or rename the folder that is not ALTO, JPEG, or TIFF.')
		checked = True
	cur = dList[-1]
	if pName == '0108':
		checkRootResult = checkRoot(r, ())
		newErrors = newErrors + (checkRootResult)
		checked = True
	elif cur['name'] == pName:
		ext = cur['extension']
		evaluatedNames = evaluateFileNames([ext], r, ())
		numF, errorList = evaluatedNames[0][ext], evaluatedNames[1]
		newErrors = newErrors + (errorList)
		cur.update({'num': numF})
		newErrors = newErrors + (identifyMvol(r, ()))
		checked = True
	checkDirectory(r, dList[:-1], pName, checked, newErrors)

def main():
	errorLog = []
	parse = buildParser(sys.argv[1:])
	if os.path.isdir(parse.directory):
		pass
	else:
		parser.error('{} is an invalid directory. Please input an existing directory.'.format(parse.directory))
	try:
		directoryTree = os.walk(parse.directory)
		acceptableDirs = [
			{'name': 'ALTO', 'extension': 'xml'},
			{'name': 'JPEG', 'extension': 'jpg'},
			{'name': 'TIFF', 'extension': 'tif'},
			{'name': '0108'}
		]

		for root, dirs, files in directoryTree:
			pathName = root[-4:].upper()
			checkDirectoryResult = checkDirectory(root, acceptableDirs, pathName, False, ())
			errorLog.append(checkDirectoryResult)

		if (acceptableDirs[0]['num'] * 3) != sum([(i['num']) for i in acceptableDirs if 'extension' in i and 'num' in i]):
			errorLog.append(('The number of files in the subdirectories is inconsistent. Please remove the ' \
			'missing or extra file.'))

		currentTime = time.strftime('%I:%M%p on %b %d, %Y', time.localtime())

		print('Total and complete error log', errorLog)
		
		if len(errorLog) == 0:
			print(' ============== RESULTS FROM VALIDATOR TOOL ============== ')
			print('            Test ran', currentTime, '          ')
			print('                OCR data passed all tests!')
		else:
			print(' ============== RESULTS FROM VALIDATOR TOOL ============== ')
			print('            Test ran', currentTime, '          ')
			print('\n'.join([error for error in errorLog if error is not None]))
		return 0
	except OSError as err:
		print("OS error: {0}".format(err))
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	_exit(main())

