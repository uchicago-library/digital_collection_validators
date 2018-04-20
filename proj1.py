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

	# to do: simplify this into for-loop, possibly
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


def fileChoices(fType, fList, d):
	""" Traverses a list of files and evaluates whether they all match a file extension.

	:param str fType: a list of string of possible extensions a file can be, depending on its directory.

	:param arr fileChoices: a list of child files in a directory.

	:param [directory]

	"""
	extDict = {}
	for f in fList:
		ext = os.path.basename(f).split('.', 1)[1:][0]
		if ext not in fType:
			parser.error('one of the files in {} does not end with {}'.format(d, fType))
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
	directoryTree = os.walk(args.directory) # creates 3-tuple

	checkRoot(args.directory)

	for root, dirs, files in directoryTree:
		for d in dirs:
			path = os.path.join(root, d)
			if d == 'ALTO':
				checker = fileChoices(['xml'], os.listdir(path), d)
				numAlto = checker['xml']
			elif d == 'JPEG':
				checker = fileChoices(['jpg'], os.listdir(path), d)
				numJPEG = checker['jpg']
			elif d == 'TIFF':
				checker = fileChoices(['tif'], os.listdir(path), d)
				numTif = checker['tif']
			else:
				parser.error('Remove the folder that is not ALTO, JPEG, or TIFF. Suggestion: it could be the PDF \
					file that needs removal')

	if numAlto != numJPEG != numTif:
		parser.error('The number of files in the subdirectories is inconsistent.')
	else:
		print('hooray! you have the proper number of files with the right number of extensions')

	try:
		return 0
	except OSError as err:
		print("OS error: {0}".format(err))
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	main()


		# temporary: draws tree for reference
		# path = root.split(os.sep)
		# print((len(path) - 1) * '---', os.path.basename(root))
		# for f in files:
		# 	print(len(path) * '---', f)

