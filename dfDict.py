#!/usr/bin/env python

import pprint
import json
import time

def getDFInfo():
    """Asking for user input to display ROB ID's for user inputted DF"""

    dfInfo = raw_input("Type in which DF's information you would like to find i.e. '1-3', '1-8', or '1-9': ")

    print '-----------------------'
    for key, value in dfDict.items():
        if dfInfo == key:
            # outputting ROB ID's associated to user inputted DF
            iterVar = 0
            while iterVar < (len(dfDict[dfInfo]) - 3) :
                print 'ROB ' + dfDict[dfInfo][iterVar][0] + ' is connected to DF ' + dfInfo + ' through cable ' +  dfDict[dfInfo][iterVar][1] + ' and IM lane ' + dfDict[dfInfo][iterVar][2]
                iterVar += 1

            # outputting channel mask associated to user inputted DF
            print '-----------------------'
            print "Channel mask for DF " + dfInfo + " is " + dfDict[dfInfo][len(dfDict[dfInfo]) - 3]
            print '-----------------------'
            main()
        else:
            invalidDF = True

    if invalidDF == True:
        print "Invalid DF. Format input as following '1-3', '4-10', or '3-7'"
        print '-----------------------'

    main()

def getRobInfo():
    """outputting DF and cable ID for user inputted ROB ID"""

    robInfo = raw_input("Enter the ROB ID whose connections you would like to know: ")

    # finding key then cable ID, and IM lane associated to user inputted DOB ID
    print '-----------------------'
    for key, value in dfDict.items():
        for sublist in value:
            if (len(sublist) == 5) and (robInfo == sublist[0]):
                print 'ROB', robInfo, 'is connected to DF', key, 'through cable', sublist[1], 'and IM Lane', sublist[2]
                print '-----------------------'
                main()
            else:
                invalidRob = True

    if invalidRob == True:
        print 'Invalid ROB ID'
        print '-----------------------'

    main()

def getCableInfo():
    """outputting info for user inputted Cable ID"""

    robCableInfo = raw_input("Enter the Cable ID whose connections you would like to know: ")

    # finding key, ROB ID, and IM lane associated to user inputted cable ID
    print '-----------------------'
    for key, value in dfDict.items():
        for sublist in value:
            if (len(sublist) == 5)  and (robCableInfo == sublist[1]):
                print 'Cable', robCableInfo, 'is connecting ROB', sublist[0], 'to IM lane', sublist[2], 'on DF', key
                print '-----------------------'
                main()
            else:
                invalidCable = True

    if invalidCable == True:
        print 'Invalid cable ID'
        print '-----------------------'

    main()

def changeCable():
    """changes cable stored in dictionary then rewrites dictionary to JSON with new cable"""

    robInfo = raw_input("Enter in the ROB ID, or DF(i.e. '1-3', '2-5') whose cable you will be changing: ")

    print '-----------------------'
    for key, value in dfDict.items():
        for sublist in value:
            if (len(sublist) == 5) and (robInfo == sublist[0]):
                print 'ROB ' + robInfo + ' is connected to DF ' + key + ' through cable ' + sublist[1] + ' and IM Lane ' + sublist[2]
            elif robInfo == key:
                IMlane = raw_input('Enter IM lane for DF ' + key + ' whose cable you will be changing: ')
                for key1, value in dfDict.items():
                    for sublist1 in value:
                        if (key1 == robInfo) and (IMlane == sublist1[2]):
                            robInfo = sublist1[0]
    print '-----------------------'

    # inputting new cable ID
    changeLog = ''
    newCable = raw_input("Now, enter in the new cable ID: ")
    for keyIndex, (key, value) in enumerate(dfDict.items()):
        for valueIndex, sublist in enumerate(value):
            if (len(sublist) == 5) and (newCable == sublist[1]):
                newRob = sublist[0]
            if (len(sublist) == 5) and (robInfo == sublist[0]):
                changedKeyIndex = keyIndex
                changedValueIndex = valueIndex
                lst = list(sublist)
                if 'newRob' in locals():
                    lst[0] = newRob
                lst[1] = newCable
                newSublist = lst
                dfDict[key][valueIndex] = newSublist
                changeLog = ' | ROB ' + newSublist[0] + ' is now connected to DF ' + key + ' through cable ' + newSublist[1] + ' and IM Lane ' + newSublist[2] + '. '

    # this block of code checks if the new cable ID was connecting another DF and ROB, if it was, it deletes the dictionary entry for the old connection
    unassignedLog = ''
    for keyIndex, (key, value) in enumerate(dfDict.items()):
        for valueIndex, sublist in enumerate(value):
            # this block of code checks if the new cable ID was connecting another DF in the same shelf and makes sure to disregard the newly assigned DF
            if (sublist[0] != sublist[-1]) and (newCable == sublist[1]) and (keyIndex == changedKeyIndex) and (valueIndex != changedValueIndex):
                unassignedLog = 'DF ' + key + ', IM lane ' + sublist[2] + ' now has no cable/ROB assignment.'
                lst = list(sublist)
                lst[0] = ' '
                lst[1] = ' '
                newSublist = lst
                dfDict[key][valueIndex] = newSublist
                print unassignedLog
                print '-----------------------'
            # this block of code checks if the new cable ID was connecting another DF in all other shelves
            elif (sublist[0] != sublist[-1]) and (newCable == sublist[1]) and (keyIndex != changedKeyIndex):
                unassignedLog = 'DF ' + key + ', IM lane ' + sublist[2] + ' now has no cable/ROB assignment.'
                lst = list(sublist)
                lst[0] = ' '
                lst[1] = ' '
                newSublist = lst
                dfDict[key][valueIndex] = newSublist
                print unassignedLog
                print '-----------------------'

    # inputting username and comment for change log file
    username = raw_input("Please enter username: ")
    comment = raw_input("Please enter comment: ")

    # appending comment to change log file along with time and date
    logFile = open("cable_log.txt", "a+")
    logFile.write(time.strftime("%H:%M:%S") + " "  + time.strftime("%d/%m/%Y") + changeLog + unassignedLog + " | User: " + username + " | Comment: " + comment + "\n")
    logFile.close()

    # dumping changed dictionary back into JSON file
    s = json.dumps(dfDict, sort_keys = True)
    with open('dfDict.json', 'w') as g:
        g.write(s)

    main()

def uninstallCable():
    """changes "installed?" boolean in dictionary to True or False"""

    print '-----------------------'
    cableChange = raw_input("Enter in cable ID being installed or uninstalled: ")
    for key, value in dfDict.items():
        for sublist in value:
            if (sublist[0] != sublist[-1]) and (cableChange == sublist[1]):
                if sublist[4] == True:
                    print '-----------------------'
                    print 'Cable', cableChange, 'is currently connecting ROB', sublist[0], 'to IM lane', sublist[2], 'on DF', key
                    print '-----------------------'
                    yesorno = raw_input('Are you uninstalling cable ' + cableChange + '? [y] for yes, [n] for no. ')
                    if yesorno == 'y':
                        sublist[4] = False
                        print 'Cable ' + cableChange + ' is now uninstalled.'
                        main()
                    else:
                        main()
                if sublist[4] == False:
                    print '-----------------------'
                    print 'Cable ' + cableChange + ' is currently assigned to ROB ' + sublist[0] + ', IM lane ' + sublist[2] + ', DF ' + key + ', but not installed.'
                    print '-----------------------'
                    yesorno = raw_input('Are you installing cable ' + cableChange + '? [y] for yes, [n] for no. ')
                    if yesorno == 'y':
                        sublist[4] = True
                        print 'Cable ' + cableChange + ' is now installed.'
                        main()
                    else:
                        main()

    # inputting username and comment for change log file
    username = raw_input("Please enter username: ")
    comment = raw_input("Please enter comment: ")

    # appending comment to change log file along with time and date
    logFile = open("cable_log.txt", "a+")
    logFile.write(time.strftime("%H:%M:%S") + " "  + time.strftime("%d/%m/%Y") + " | " + "User: " + username + " | Comment: " + comment + "\n")
    logFile.close()

    # dumping changed dictionary back into JSON file
    s = json.dumps(dfDict, sort_keys = True)
    with open('dfDict.json', 'w') as g:
        g.write(s)

    main()

def printDict():
    """prints dfDict"""

    # using pprint module for output readability
    pprint.pprint(dict(dfDict))

    main()

def sdMask():
    """prints subdetectorMask dictionary"""

    pprint.pprint(dict(subdetectorMask))

    main()

def info():
    """giving user commands for calling functions"""

    print 'Type in "dictionary" to display DF dictionary.'
    print 'Type in "df" to get DF information.'
    print 'Type in "rob" to get ROB information.'
    print 'Type in "cable" to get cable information.'
    print 'Type in "sub" to display subdetector channel mask dictionary'
    print 'Type in "change" to change cabling information'
    print 'Type in "install" to change install information'
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
    elif k == 'sub':
        sdMask()
    elif k == 'change':
        changeCable()
    elif k == 'install':
        uninstallCable()

with open('dfDict.json') as f:
    dfDict = json.load(f)

with open('subdetectorMask.json') as f:
    subdetectorMask = json.load(f)

info()
main()
