import vault
import os
import csv



def Modify():
    arrData = []
    arrData.append(None)

    print('Available modifications:\n'
          '\t1 - \"Stay at Home\" Order Notifications\n'
          '\t2 - Device name\n'
          '\t3 - Current location being monitored\n'
          'You must delete a phone number if you wish to change it. Use \'cancel\' to go back to the configuration menu.')

    strModResponse = input().lower()

    if strModResponse == None:
        print('Command not recognized.')
    elif strModResponse == 'cancel' or strModResponse == 'c':
        return

    #modify stay at home info
    elif strModResponse == '1':
        strEntries = vault.Get("all")

        intEntryCount = 0
        print("Select a phone to modify:")
        print
        for entry in strEntries:
            intEntryCount += 1
            print("\t" + str(intEntryCount) + " - " + (entry[1])[:20] +
                  " - Stay at Home Notification: " + str(entry[4]).replace("1", "YES").replace("0", "NO"))
        strPhoneResponse = input().lower()
        if strPhoneResponse == 'cancel' or strPhoneResponse == 'c':
            return
        elif strPhoneResponse.isnumeric() == True:
            if int(strPhoneResponse) < 1 or int(strPhoneResponse) > intEntryCount:
                print("That phone does not exist.")
            else:
                __Change(strModResponse, strEntries[int(strPhoneResponse)-1])
        else:
            print("Entry not recognized.")

    # modify stay at home info
    elif strModResponse == '2':
        strEntries = vault.Get("all")

        intEntryCount = 0
        print("Select a phone to modify:")
        print
        for entry in strEntries:
            intEntryCount += 1
            print("\t" + str(intEntryCount) + " - " + (entry[1])[:20])
        strPhoneResponse = input().lower()
        if strPhoneResponse == 'cancel' or strPhoneResponse == 'c':
            return
        elif strPhoneResponse.isnumeric() == True:
            if int(strPhoneResponse) < 1 or int(strPhoneResponse) > intEntryCount:
                print("That phone does not exist.")
            else:
                __Change(strModResponse, strEntries[int(strPhoneResponse) - 1])
        else:
            print("Entry not recognized.")

    #modify device name
    elif strModResponse == '3':
        strEntries = vault.Get("all")

        intEntryCount = 0
        print("Select a phone to modify:")
        print
        for entry in strEntries:
            intEntryCount += 1
            print("\t" + str(intEntryCount) + " - " + (entry[1])[:20] + " - Watching Location: " + str(entry[3]))

        strPhoneResponse = input().lower()
        if strPhoneResponse == 'cancel' or strPhoneResponse == 'c':
            return
        elif strPhoneResponse.isnumeric() == True:
            if int(strPhoneResponse) < 1 or int(strPhoneResponse) > intEntryCount:
                print("That phone does not exist.")
            else:
                __Change(strModResponse, strEntries[int(strPhoneResponse) - 1])
        else:
            print("Entry not recognized.")

def __Change(strModType, arrEntry):
    #update stay at home
    if strModType == "1":
        strNewValue = str(arrEntry[4]).replace("1", "NO").replace("0", "YES")
        arrData = (not arrEntry[4], arrEntry[0])
        vault.Update('sah_notified', arrData)
        print(arrEntry[1] + "\'s \"Stay at Home\" Order Notification has been set to " + strNewValue)

    #update phone name
    elif strModType == "2":
        print("Enter a new name for " + arrEntry[1] + ":")
        strNewValue = input()
        arrData = (strNewValue, arrEntry[0])
        vault.Update('udn', arrData)
        print(arrEntry[1] + " has been renamed to " + strNewValue)

    # update phone name
    elif strModType == "3":
        blnPass = False
        print("New location you want to monitor for " + arrEntry[1] + " (eg: Maryland, MD, DC, Oregon): ")
        strNewValue = input()
        strPath = os.path.split(os.path.abspath(__file__))
        with open(os.path.join(strPath[0], 'StateInfo.csv')) as csvFile:
            csvEntries = list(csv.reader(csvFile))
            while(blnPass == False):
                for row in csvEntries:
                    if row[0] == strNewValue.upper() or row[1] == strNewValue.title():
                        arrData = (row[1], arrEntry[0])
                        vault.Update('Usr_Location', arrData)
                        print(arrEntry[1] + "\'s monitoring location has been updated to " + arrData[0])
                        blnPass = True
                if blnPass == False:
                    print('US state or district name or abbreviation not recognized.')