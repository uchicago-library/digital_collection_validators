import argparse
import os

""" checkRoot evaluates there are 3 subdirs (ALTO, JPEG, TIFF) and 5 files (xml, pdf, txt)
	checkRoot throws an error if there are not 3 subdirs and 5 files"""
def checkRoot(r):
	for n_item in scandir(r):
		if n_item.is_dir():
			dirNum += 1
		elif n_item.is_file():
			fileNum += 1
	if dirNum != 3 or fileNum != 5:
		parser.error('there are not 3 subdirectories and 5 files in this directory')

""" fileChoices takes paramaters of extensions (@choices) and a list of child files (@flist). 
	It traverses fList to see if all files end with choices """
def fileChoices(fType, fList):
	extDict = {}
	for f in fList:
		ext = os.path.splitext(f)[1][1:]
		print(ext)
		if ext != fType:
			parser.error('one of the files does not end with {}'.format(fType))
		if str(ext) in fList:
			extDict[ext] += 1
		else:
			extDict[ext] = 1
		print(f)

""" observing """
parser = argparse.ArgumentParser(description='Checks OCR directory')

def main():
	parser.add_argument(
		'-dir', '--directory', action='store', required=True, \
		default='/tmp/non_existent_dir', help='input OCR data directory path')
	args = parser.parse_args()
	args_dict = vars(args)
	directoryTree = os.walk(args.directory)

	for root, dirs, files in directoryTree:
		# temporary: draws tree for reference
		path = root.split(os.sep)
		print((len(path) - 1) * '---', os.path.basename(root))
		for f in files:
			print(len(path) * '---', f)

		# traverses tree
		for d in dirs:
			if d == 'ALTO':
				numAlto = len(os.listdir(d))
				fileChoices('xml', os.listdir(d))
			if d == 'JPEG':
				numJPEG = len(os.listdir(d))
				fileChoices('jpeg', os.listdir(d))
			if d == 'TIFF':
				numTiff = len(os.listdir(d))
				fileChoices('tif', os.listdir(d))

		if numAlto != numJPEG != numTiff:
			parser.error('the number of files in each subdirectory do not match one another.')

	try:
		return 0
	except KeyboardInterrupt:
		return 131

if __name__ == '__main__':
	main()

