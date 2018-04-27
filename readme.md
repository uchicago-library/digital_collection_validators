# Introduction

## About dcv
Digital Collection Validator (dcv) is a validator for multi-volume digitization workflows in the UChicago Library's Preservation Department. It was inspired by the non-normative document I published earlier on developing such a tool.

 dcv performs quality assessment *only* on directories of multi-volume collection objects before they are deposited into the Library Digital Repository (ownCloud). dcv will not work properly for the Library's other collections. The purpose is to minimize the manual assessment of a directory's structure and to eliminate any structural errors before it is integrated into ownCloud. dcv is hosted exclusively on the Command Propmt. 

## dcv's Functions
dcv checks for the following in a directory:

- existence of directory
- 3 subdirectories (ALTO, JPEG, TIFF)
- 5independent files in the main directory (dc.xml, mets.xml, pdf, struct.text, text)
- all files in each subdirectory have the same extension
- the number of files in each subdirectory are consistent with each other
- mvol identifiers are in the right order; none are missing
- tbd: outputs an Excel sheet with errors

If the inputted directory fails any of the above qualifications, dcv will list specific errors.

Although this version of dcv runs on a local machine's command prompt or terminal, *no programming experience is required*. To run the tool over a directory of OCR data, simply open the machine's command prompt and run the validator by inputting the path of the directory in question.

# Quickstart

1. Open Command Prompt

  If you are in the Preservation Department, it is likely you will be working on a Windows machine. In the bottom-left searchbar, type `cmd` and open the Command Prompt.
2. Download the validator in the Command Prompt
```bash
$ git clone git@github.com:uchicago-library/digital_collection_validators
```
3. Navigate to the desired folder of OCR data on your local machine
4. Copy the path at the top of the Folder Explorer window
5. In the Command Prompt, input the below block of code. Replace `<DIRECTORY_PATH>` by pasting the path from the previous step
```bash
$ proj1.py -dir <DIRECTORY_PATH>
```
    
  **Example**: For Presidential Papers Box 68, Folder 108, the prompt might look something like
```
$ proj1.py -dir C:\Users\presworker\samba\prespapers\68\0108
```
6. dcv will run through the directory and flag any errors
