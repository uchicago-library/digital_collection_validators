# Introduction

Digital Collection Validator (dcv) is a validator for multi-volume digitization workflows in the UChicago Library's Preservation Department. It was inspired by the non-normative document I published earlier on developing such a tool.

dcv is a command-line tool that performs quality assessment on directories of multi-volume collection objects before they are deposited into the Library Digital Repository (ownCloud). The purpose is to minimize the manual assessment of a directory's structure and to eliminate any structural errors before it is integrated into ownCloud.

dcv checks for the following in a directory:
	- 3 subdirectories (ALTO, JPEG, TIFF)
	- 5 independent files in the main directory (dc.xml, mets.xml, pdf, struct.text, text)
	- all files in each subdirectory have the same extension
	- the number of files in each subdirectory are consistent with each other

Although this version of the validator runs on a local machine's command prompt or terminal, no programming experience is required. To run the tool over a directory of OCR data, simply open the machine's command prompt and run the validator by inputting the path of the directory in question.

# Quickstart

1. Open Command Prompt
	1. If you are in the Preservation Department, it is likely you will be working on a Windows machine. In the bottom-left searchbar, type `cmd` and open the Command Prompt.
2. Download the validator
``` bash
$ git clone git@github.com:uchicago-library/digital_collection_validators
```
3. Navigate to the desired folder of OCR data in Folder Explorer
4. Copy the 'path' at the top of Folder Explorer
5. In the Command Prompt, replace <DIRECTORY_PATH> by pasting the directory 'path' from the previous step 
```bash
$ proj1.py -dir <DIRECTORY_PATH>
```
