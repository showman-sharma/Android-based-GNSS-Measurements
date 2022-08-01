# Android-based GNSS Measurements

-------------------------------------------------
|	Author: V S S Anirudh Sharma		|
|	Roll Number: EE18B036			|
|	Date: 7th November 2021			|
-------------------------------------------------

## HOW TO RUN THE CODE

The 3 log files are named as follows:
1. inside.txt
2. balcony.txt
3. outside.txt
These 3 files are named to depict the 3 locations from where the logs were recorded.

These 3 files MUST be in the same folder as the code file: EE18B036_HW2_code.py

Please verify if the following libraries are installed in your system:

matplotlib==3.3.2
mpmath==1.2.1
numpy==1.19.5
pandas==1.2.2
scikit-learn==0.24.2
sklearn==0.0

The mentioned versions are as used on the author's system. 
The versions might not necessarily be the same for those who choose to test the code.
But in case of any issues, please do install these libraries of the given versions from the requirements.txt

After that, just run the code file. You must be able to see text output + 15 plots

NOTE:
In case the user wishes to check the code for different log files, the following needs to be done:
Line 8 of the code file has the following:
		cases =  ['inside','balcony','outside']
in case you wish to test the code on files 'w.txt', 'x.txt', 'y.txt' , 'z.txt', then the above line must be replaced with:
		cases =  ['w','x','y','z']

and the files 'w.txt', 'x.txt', 'y.txt' , 'z.txt' must be in the same folder as the code file



## ABOUT THE CODE
The code uses GNSSLogger app log files to output values and plots as required in Homework 2 of CS6650.
The code is sectioned as relevant to the questionnaire and reasonably well commented to make it understandable.

