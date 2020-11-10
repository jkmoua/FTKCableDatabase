#!/usr/bin/env python

import csv
import pprint
import json
import time
from collections import defaultdict

def getDFInfo():
    """Asking for user input to display ROB ID's for user inputted DF"""

    dfInfo = raw_input("Type in which DF's information you would like to find i.e. '1-3', '1-8', or '1-9': ")

    # outputting ROB ID's associated to user inputted DF
    print '-----------------------'
    iterVar = 0
    while iterVar < (len(dfDict[dfInfo]) - 3) :
        print 'ROB ' + dfDict[dfInfo][iterVar][0] + ' is connected to DF ' + dfInfo + ' through cable ' +  dfDict[dfInfo][iterVar][1] + ' and IM lane ' + dfDict[dfInfo][iterVar][2]
        iterVar += 1

    # outputting channel mask associated to user inputted DF
    print '-----------------------'
    print "Channel mask for DF " + dfInfo + " is " + dfDict[dfInfo][len(dfDict[dfInfo]) - 3]
    print '-----------------------'

    main()

def getRobInfo():
    """outputting DF and cable ID for user inputted ROB ID"""

    robInfo = raw_input("Enter the ROB ID whose connections you would like to know: ")

    # finding key then cable ID, and IM lane associated to user inputted DOB ID
    print '-----------------------'
    for key, value in dfDict.items():
        for sublist in value:
            if (sublist[0] != sublist[-1]) and (robInfo == sublist[0]):
                print 'ROB', robInfo, 'is connected to DF', key, 'through cable', sublist[1], 'and IM Lane', sublist[2]
    print '-----------------------'

    main()

def getCableInfo():
    """outputting info for user inputted Cable ID"""

    robCableInfo = raw_input("Enter the Cable ID whose connections you would like to know: ")

    # finding key, ROB ID, and IM lane associated to user inputted cable ID
    print '-----------------------'
    for key, value in dfDict.items():
        for sublist in value:
            if (sublist[0] != sublist[-1]) and (robCableInfo == sublist[1]):
                print 'Cable', robCableInfo, 'is connecting ROB', sublist[0], 'to IM lane', sublist[2], 'on DF', key
    print '-----------------------'

    main()

def printDict():
    """prints dfDict"""

    # using pprint for output readability
    pprint.pprint(dict(dfDict))

    main()

def sdMask():
    """prints subdetectorMask dictionary"""

    pprint.pprint(dict(subdetectorMask))

    main()

def write2json():
    """dumps dfDict dictionary to json file"""

    s = json.dumps(dfDict, sort_keys = True)
    with open('dfDict.json', 'w') as f:
        f.write(s)
        print 'Wrote DF dictionary to dfDict.json'

    main()

def writesdMasktoJSON():
    """dumps subdetectorMask dictionary to JSON file"""

    s = json.dumps(subdetectorMask, sort_keys = True)
    with open('subdetectorMask.json', 'w') as f:
        f.write(s)
        print 'Wrote subdetector channel mask dictionary to subdetectorMask.json'

    main()

def appendtoDict():
    """reads csv, and then appends desired information from csv to dfDict"""

    readCSV = csv.reader(f)

    for column in readCSV:
        # this if condition disregards inputting the separating rows in the CSV file into the dictionary
        if column[4] != '':
            # removing tower number from DF info(column[4]), 3rd number is unimportant/outdated
            dashToSplitString = 2
            groups = column[4].split('-')
            column[4] = '-'.join(groups[:dashToSplitString])
            # determining channel type from ROB ID(column[2])
            if ('0x11' or '0x12' or '0x13') in column[2]:
                channelType = 'Pixel'
            elif '0x2' in column[2]:
                channelType = 'SCT'
            elif '0x14' in column[2]:
                channelType = 'IBL'
            elif 'Rob ID' in column[2]:
                channelType = 'Subdetector'
            # this if condition disregards repeatedly adding the FTK Shelf-Slot header row for each of the 4 csv files
            if (column[4] != 'FTK Shelf-Slot') or ('FTK Shelf-Slot'  not in dfDict):
                if column[9] == 'yes':
                    installed = True
                elif column[9] == 'no':
                    installed = False
                elif column[9] == 'Installed?':
                    installed = 'Installed?'
                # adding information to dictionary
                dfDict[column[4]].append((column[2], column[3], column[5], channelType, installed))

def info():
    """giving user commands for calling functions"""

    print 'Type in "dictionary" to display DF dictionary.'
    print 'Type in "df" to get DF information.'
    print 'Type in "rob" to get ROB information.'
    print 'Type in "cable" to get cable information.'
    print 'Type in "exit" to exit.'

    main()

def main():
    """main function taking in input for which function to be called"""

    print 'Type in "info" for commands'
    k = raw_input()
    if k == 'dictionary':
        printDict()
    elif k == 'df':
        getDFInfo()
    elif k == 'rob':
        getRobInfo()
    elif k == 'cable':
        getCableInfo()
    elif k == 'exit':
        exit()
    elif k == 'info':
        info()
    elif k == 'json':
        write2json()
    elif k == 'sub':
        sdMask()
    elif k == 'sdjson':
        writesdMasktoJSON()

# using defaultdict to allow for multiple lists per key
dfDict = defaultdict(list)
subdetectorMask = defaultdict(list)

with open('PIX_SCT_AsInstalledAtP1_1.csv') as f:
    """page 1 of cabling info"""

    appendtoDict()

with open('PIX_SCT_AsInstalledAtP1_2.csv') as f:
    """page 2 of cabling info"""

    appendtoDict()

with open('PIX_SCT_AsInstalledAtP1_3.csv') as f:
    """page 3 of cabling info"""

    appendtoDict()

with open('PIX_SCT_AsInstalledAtP1_4.csv') as f:
    """page 4 of cabling info"""

    appendtoDict()

# Retrieve values from dictionary lists using 'dictionary['key' i.e. DF Shelf-Slot][list index][sublist/value index]'
# Example: print('FTK IM Lane for DF 1-3 ROB ID', dfDict['1-3'][2][0], 'is',  dfDict['1-3'][2][2])

for key, value in dfDict.items():
    """creating channel mask"""

    IMchannel = []
    IMchannelBinary = []
    for sublist in value:
        IMchannel.append(sublist[2])
    for i in range(16):
        if str(i) in IMchannel:
            IMchannelBinary.append('1')
        else:
            IMchannelBinary.append('0')
    # reversing binary number to be indexed right to left
    reverseBinary = ("".join(IMchannelBinary))[::-1]
    # converting to hex
    IMint = int(reverseBinary, 2)
    IMhex = ('%x' % IMint).zfill(4)
    # adding in channel mask name for FTK Shelf-Slot key containing type of data in dictionary
    if key == 'FTK Shelf-Slot':
        IMhex = 'Channel Mask'
    dfDict[key].append(IMhex)

for key, value in dfDict.items():
    """creating subdetector channel mask"""

    pixelChannel = []
    iblChannel = []
    sctChannel = []
    pixelChannelBinary = []
    iblChannelBinary = []
    sctChannelBinary = []
    for sublist in value:
        if sublist[3] == 'Pixel':
            pixelChannel.append(sublist[2])
        if sublist[3] == 'IBL':
            iblChannel.append(sublist[2])
        if sublist[3] == 'SCT':
            sctChannel.append(sublist[2])
    for i in range(16):
        if str(i) in pixelChannel:
            pixelChannelBinary.append('1')
        else:
            pixelChannelBinary.append('0')
    for i in range(16):
        if str(i) in iblChannel:
            iblChannelBinary.append('1')
        else:
            iblChannelBinary.append('0')
    for i in range(16):
        if str(i) in sctChannel:
            sctChannelBinary.append('1')
        else:
            sctChannelBinary.append('0')
    # reversing binary number to be indexed right to left
    pixReverseBinary = ("".join(pixelChannelBinary))[::-1]
    iblReverseBinary = ("".join(iblChannelBinary))[::-1]
    sctReverseBinary = ("".join(sctChannelBinary))[::-1]
    # converting to hex
    pixInt = int(pixReverseBinary, 2)
    pixHex = ('%x' % pixInt).zfill(4)
    iblInt = int(iblReverseBinary, 2)
    iblHex = ('%x' % iblInt).zfill(4)
    sctInt = int(sctReverseBinary, 2)
    sctHex = ('%x' % sctInt).zfill(4)
    # adding in channel mask name for FTK Shelf-Slot key containing type of data in dictionary
    if key == 'FTK Shelf-Slot':
        pixHex = 'Pixel'
        iblHex = 'IBL'
        sctHex = 'SCT'
    subdetectorMask[key].append((pixHex, iblHex, sctHex))

with open('df_system_config.txt') as g:
    """adding in FTK Tower numbers to associated DF's from txt file"""

    # this dictionary stores the board number with the respective DF
    boardDict = {}
    for line in g:
        if 'BoardNToShelfAndSlot' in line:
            board = (line[22] + line[23]).strip()
            dfShelfSlot = line[26] + '-' + ((line[29] + line[30]).strip())
            boardDict[dfShelfSlot] = board

        # This block associates the top towers with their respective board
        if 'BoardNToTopTower' in line:
            for key, value in boardDict.items():
                if value == (line[17] + line[18]).strip():
                    if line[20] == line[-1]:
                        topTower = (line[19] + line [20]).strip()
                    else:
                        topTower = (line[19] + line[20] + line[21]).strip()
                    dfDict[key].append(topTower)

        # This block associates the bottom towers with their respective board
        if 'BoardNToBotTower' in line:
            for key, value in boardDict.items():
                if value == (line[17] + line[18]).strip():
                    if line[20] == line[-1]:
                        botTower = (line[19] + line [20]).strip()
                    else:
                        botTower = (line[19] + line[20] + line[21]).strip()
                    dfDict[key].append(botTower)

for key, value in dfDict.items():
    """adding in tower names for FTK Shelf-Slot key containing type of data in dictionary"""

    if key == 'FTK Shelf-Slot':
        dfDict[key].append('Top Tower')
        dfDict[key].append('Bottom Tower')

info()
main()
