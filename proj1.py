import argparse
import os
from os import _exit

def checkRoot(r): 
	"""Determines the proper number of subdirectories and files.
	Checks for 3 subdirs (ALTO, JPEG, TIFF) and 5 files (xml, pdf, txt) at the top-level of the input directory.
	
	:param [generator] r: <description of r>
	
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
		parser.error('There is a missing file type from the root directory. Please refer to the Campus Pub \
			spec sheet for the required OCR data formats.')	
	elif dirNum != 3 or fileNum != 5:
		parser.error('This directory does not have 3 subdirectories and 5 files.')

def mvolIdentifier(subdirList, subdirName):
	"""Evaluates whether 1) all mvol identifiers match and 2) their pagination is consistent
	
	Selects the identifier and ensures they all match.
	Appends last 4 digits of each mvol and ensures that there aren't any missing pages 
	in a recursive function checkPagination. It raises errors otherwise.
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
			parser.error('The pagination does not increase or decrease by 1 in {}'.format(d))
		checkPagination(pList[:-1], d)

	checkPagination(pagination, subdirName)

	if len(set(fullMvol)) < len(fullMvol):
		parser.error('One of the identifiers in this folder is inconsistent with the rest.')


def fileChoices(fType, fList, d):
	"""Traverses a list of files and evaluates whether they all match a file extension.
	:param array fType: a list of string of possible extensions a file can be, depending on its directory.
	:param arr fList: a list of child files in a directory.
	:param [directory]
	"""
	extDict = {}
	for f in fList:
		ext = os.path.basename(f).split('.', 1)[1:][0]
		if ext not in fType:
			parser.error('one of the files in folder {} does not end with {}'.format(d, fType))
		if ext in extDict:
			extDict[ext] += 1
		else:
			extDict[ext] = 1
	return extDict
	
parser = argparse.ArgumentParser(description='Checks OCR directory')

def main():
	parser.add_argument(
		'-dir', '--directory', action='store', required=True, \
		default='/tmp/non_existent_dir', help='input OCR data directory path')
	args = parser.parse_args()

	if exists(args.directory):
		pass
	else:
		raise ValueError('Invalid directory. Please input a real directory.')
	
	try:
		directoryTree = os.walk(args.directory) # creates 3-tuple
		checkRoot(args.directory)
		for root, dirs, files in directoryTree:
			for d in dirs:
				path = os.path.join(root, d)
				if d == 'ALTO':
					checker = fileChoices(['xml'], os.listdir(path), d)
					numAlto = checker['xml']
					mvolIdentifier(os.listdir(path), d)
				elif d == 'JPEG':
					checker = fileChoices(['jpg'], os.listdir(path), d)
					numJPEG = checker['jpg']
					mvolIdentifier(os.listdir(path), d)
				elif d == 'TIFF':
					checker = fileChoices(['tif'], os.listdir(path), d)
					numTif = checker['tif']
					mvolIdentifier(os.listdir(path), d)
				else:
					parser.error('Remove the folder that is not ALTO, JPEG, or TIFF. Did you extract the PDF from its \
						subdirectory?')

		if numAlto != numJPEG != numTif:
			parser.error('The number of files in the subdirectories is inconsistent.')
		else:
			print('hooray! you have the proper number of files with the right number of extensions')
			return 0

	except OSError as err:
		print("OS error: {0}".format(err))
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	main()