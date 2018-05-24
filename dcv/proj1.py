import os
import time
import sys
import argparse
from os import _exit

errorLog = []

def checkRoot(r): 
	"""Determines the proper number of subdirectories and files.
	Checks for 3 subdirs (ALTO, JPEG, TIFF) and 5 files (xml, pdf, txt) at the top-level of the input directory.
	:param generator r: top-level directory of input
	:rtype None 
	"""
	rChoices = ['dc.xml', 'struct.txt', 'mets.xml', 'txt', 'pdf']
	dirNum, fileNum = 0, 0
	rIter = os.scandir(r)
	rList = []
	mvols = set()

	for elem in rIter:
		if elem.is_dir():
			dirNum += 1
		elif elem.is_file():
			fileNum += 1
			rList.append(elem)
			mvols.add(os.path.basename(elem).split('.', 1)[0])

	extensionDict = evaluateFileNames(rChoices, rList)
	if len(mvols) != 1:
		errorLog.append('The mvol identifiers of files in the root directory require uniformity.')
	if dirNum != 3 or fileNum != 5:
		errorLog.append('The root directory does not have 3 subdirectories and 5 files.')
	elif not all(value == 1 for value in extensionDict.values()):
		errorLog.append('There is a missing file type from the root directory. Please refer ' \
			'to the Campus Pub spec sheet for the required OCR data formats.')

def evaluateFileNames(fType, d):
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
			errorLog.append('Please remove the nested directory "{}" in {}.'.format(os.path.basename(f), d))
		else:
			ext = os.path.basename(f).split('.', 1)[1:][0]
			if ext not in fType:
				errorLog.append('A file in folder {} does not end with {}.'.format(d, fType))
			if ext in extDict:
				extDict[ext] += 1
			else:
				extDict[ext] = 1
	return extDict

def identifyMvol(r):
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

	if len(set(fullMvol)) != 1:
		errorLog.append('An mvol identifier in folder {} is inconsistent with the rest.'.format(r))

	def countPagination(pList, d):
		if len(pList) == 1:
			return True
		if abs(int(pList[-1]) - int(pList[-2])) != 1:
			errorLog.append('The pagination does not increase or decrease by 1 in {}.'.format(d))
		countPagination(pList[:-1], d)
	countPagination(pagination, r)

def buildParser(args):
	parser = argparse.ArgumentParser(description='Checks OCR directory')
	parser.add_argument(
		'-dir', '--directory', action='store', required=True, default=os.getcwd(), help='Input OCR data directory path')
	return parser.parse_args(args)	

def main():
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

		def checkDirectory(r, dList, pName, checked):
			"""Traverses a directory, counts its files, and calls functions on files
			:param generator r: directory
			:param list dList: list of expected extension objects, acceptableDirs
			:param str pName: name of directory
			"""
			if checked:
				return
			if len(dList) == 1 and dList[0]['name'] != pName:
				errorLog.append('Please remove or rename the folder that is not ALTO, JPEG, or TIFF.')
				checked = True
			cur = dList[-1]
			if pName == '0108':
				checkRoot(r)
				checked = True
			elif cur['name'] == pName:
				ext = cur['extension']
				cur.update({'num': evaluateFileNames([ext], r)[ext]})
				identifyMvol(r)
				checked = True
			checkDirectory(r, dList[:-1], pName, checked)

		for root, dirs, files in directoryTree:
			pathName = root[-4:].upper()
			checkDirectory(root, acceptableDirs, pathName, False)				

		if (acceptableDirs[0]['num'] * 3) != sum([(i['num']) for i in acceptableDirs if 'extension' in i]):
			errorLog.append('The number of files in the subdirectories is inconsistent. Please remove the ' \
				'missing or extra file.')

		currentTime = time.strftime('%I:%M%p on %b %d, %Y', time.localtime())
		if len(errorLog) == 0:
			print(' ============== RESULTS FROM VALIDATOR TOOL ============== ')
			print('            Test ran', currentTime, '          ')
			print('                OCR data passed all tests!')
		else:
			print(' ============== RESULTS FROM VALIDATOR TOOL ============== ')
			print('            Test ran', currentTime, '          ')
			print('\n'.join([error for error in errorLog]))
		return 0
	except OSError as err:
		print("OS error: {0}".format(err))
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	_exit(main())

