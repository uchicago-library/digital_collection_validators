import argparse
import os

""" checkRoot evaluates there are 3 subdirs (ALTO, JPEG, TIFF) and 5 files (xml, pdf, txt)
	checkRoot throws an error if there are not 3 subdirs and 5 files"""
def checkRoot(r): 
	dirNum = 0
	fileNum = 0
	for n_item in os.scandir(r):
		if n_item.is_dir():
			dirNum += 1
		elif n_item.is_file():
			fileNum += 1
	if dirNum != 3 or fileNum != 5:
		parser.error('there are not 3 subdirectories and 5 files in this directory')

""" fileChoices takes paramaters of extensions (@choices) and a list of child files (@flist). 
	It traverses fList to see if all files end with choices """
def fileChoices(fType, fList, d):
	extDict = {}
	for f in fList:
		ext = os.path.splitext(f)[1][1:]
		if ext != fType:
			parser.error('one of the files in {} does not end with {}'.format(d, fType))
		if ext in extDict:
			extDict[ext] += 1
		else:
			extDict[ext] = 1
	return extDict
	

""" observing """
parser = argparse.ArgumentParser(description='Checks OCR directory')

def main():
	parser.add_argument(
		'-dir', '--directory', action='store', required=True, \
		default='/tmp/non_existent_dir', help='input OCR data directory path')
	args = parser.parse_args()
	args_dict = vars(args)
	directoryTree = os.walk(args.directory)

	checkRoot(args.directory)
	for root, dirs, files in directoryTree:
		for d in dirs:
			path = os.path.join(root, d)
			if d == 'ALTO':
				checker = fileChoices('xml', os.listdir(path), d)
				numAlto = checker['xml']
			elif d == 'JPEG':
				checker = fileChoices('jpg', os.listdir(path), d)
				numJPEG = checker['jpg']
			elif d == 'TIFF':
				checker = fileChoices('tif', os.listdir(path), d)
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
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	main()


		# temporary: draws tree for reference
		# path = root.split(os.sep)
		# print((len(path) - 1) * '---', os.path.basename(root))
		# for f in files:
		# 	print(len(path) * '---', f)

