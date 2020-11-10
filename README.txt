# README last updated 06 August 2017
# AUTHOR: Jim King Moua <jim.king.moua@cern.ch>
# DESCRIPTION: The python scipts in this directory input data from the PIX_SCT_AsInstalledAtP1 
# excel spreadsheet into a python dictionary. All scripts run on Python 2. The dictionary can 
# then be queried with the functions in the script for information about the cabling. 
# The dictionary can also be exported as a JSON file.

## makeDictionary.py script
=================================
The makeDictionary.py script inputs data from the PIX_SCT_AsInstalledAtP1_1.csv, 
PIX_SCT_AsInstalledAtP1_2.csv, PIX_SCT_AsInstalledAtP1_3.csv, PIX_SCT_AsInstalledAtP1_4.csv, 
and df_system_config.txt files. This script generates the dictionary during runtime then users 
can input commands to query the dictionary for information. The script outputs commands for 
the user at the beginning of execution. These commands will query the dictionary for different things. 
This script should mainly be used to create the dictionary and export it as a JSON file.

- PIX_SCT_AsInstalledAtP1 csv file input are declared on lines 164, 169, 174, and 179
- df_system_config.txt input declared on line 258
- dfDict.json file declared on line 77
- subdetectorMask.json file declared on line 87

'dictionary' command [function starts on line 58] - Outputs the complete DF dictionary. The keys 
of this dictionary are the Data Formatter(DF) shelf-slots. The values for these keys consists of 
several lists with the objects stored in these lists being ['ROB ID', 'Cable ID', 'FTK IM Lane', 
'Subdetector', Installed?]. The "Installed?" value in the list is of type boolean. Every key then 
has 3 string values after the lists which are the IM channel mask, top FTK tower, and bottom FTK tower.

'sub' command [function starts on line 66] - Outputs the subdetector/IM channel mask dictionary. 
The values stored in this dictionary are 4 digit hexadecimal numbers which represent which IM 
lanes on each DF are occpuied by which subdetector (Pixel, IBL, SCT). Each DF has 16 IM channels 
which allows for a 16 bit binary number with 1's representing occupied channels and 0's representing 
unoccupied channels. This 16 bit binary is then converted to a hexadecimal which is stored in the dictionaries.

'df' command [function starts on line 9] - Prompts users for a DF shelf-slot in the form of '1-3', 
'2-4', '4-10' for example. It then outputs all the ROB ID's cable ID's, and IM lanes connected to 
the user inputted DF along with the IM channel mask of the DF. If an invalid DF (typo or wrong format) 
is inputted, The script outputs "invalid DF" and the program returns to the main input function.

'rob' command [function starts on line 28] - Prompts users for a ROB ID and then returns the 
respective cable ID, DF, and IM lane it is connected to. If an invalid ROB ID (typo or wrong format) 
is inputted, The script outputs "invalid ROB" and the program returns to the main input function.

'cable' command [function starts on line 43] - Prompts users for a cable ID and then returns the 
respective ROB ID, DF, and IM lane it is connected to. If an invalid cable ID (typo or wrong format) 
is inputted, The script outputs "invalid cable" and the program returns to the main input function.

'json' command [function starts on line 73] - Writes the DF dictionary to a json file 
named dfDict.json. This is the json file used by the dfDict.py script.

'sdjson' command [function starts on line 83] - Writes the subdetector/IM channel mask 
to a json file named subdetectorMask.json. The dfDict.py script also uses this json file.

## dfDict.py script
=================================
The dfDict.py script has all the same commands as the makeDictionary.py script except 
for the 'json' and 'sdjson' commands. This script queries the DF dictionary without the 
need to generate it during runtime. It imports the data from the json files created with 
the makeDictionary.py script. Thus, it relies only on the dfDict.json and subdetectorMask.json files. 
It also adds two new commands: 'change' and 'uninstall'.

- dfDict.json file input declared on line 256
- subdetectorMask.json file input declared on line 259
- dfDict.json file output declared on line 151 for 'change' command
- cable_log.txt file output declared on line 145 for 'change' command
- dfDict.json file output declared on line 198 for 'install' command
- cable_log.txt file output declared on line 192 for 'install' command

'change' command [function starts on line 79] - Changes cabling information in the dictionary, logs changes to a 
text file called cable_log.txt, then recreates the dfDict.json files with the new cabling information. 

'install' command [function starts on line 156] - Changes the "Installed?" boolean stored in the dictionary to True 
or False based on user input. Changes are logged to the same cable_log.txt file as the 'change' command.


