import vault
import re
import os
import csv
from smsmanager import textmessaging



def CreateNew():
    arrData = []
    strPhoneAddress = None
    arrData.append(None)
    arrPrompts = ["Name of device: ", "Your phone number: ", "Location you want to monitor (eg: Maryland, MD, DC, Oregon): ",
                  "Do you want to be notified about \"Stay at Home\" Orders issued? (Yes/No): "]
    for prompt in arrPrompts:
        blnNext = False

        while blnNext == False:

            print(prompt)
            strResponse = input()

            if prompt == arrPrompts[0]:
                if strResponse == None:
                    print('[!] The phone must have a name.')
                else:
                    arrData.append(strResponse)
                    blnNext = True

            elif prompt == arrPrompts[1]:
                re.sub('[^A-Za-z0-9]+', '', strResponse)
                if len(strResponse) == 10:
                    arrData.append("+1" + strResponse)
                    blnNext = True
                else:
                    print('[!] US phone numbers are ten digits in length.')

            elif prompt == arrPrompts[2]:
                strPath = os.path.split(os.path.abspath(__file__))
                with open(os.path.join(strPath[0], 'StateInfo.csv')) as csvFile:
                    csvEntries = list(csv.reader(csvFile))
                    for row in csvEntries:
                        if row[0] == strResponse.upper() or row[1] == strResponse.title():
                            arrData.append(row[1])
                            blnNext = True
                if blnNext == False:
                    print('[!] Enter a US state or district name or abbreviation.')

            elif prompt == arrPrompts[3]:
                if strResponse.lower() == 'y' or strResponse.lower() == 'yes':
                    arrData.append(True)
                    blnNext = True
                elif strResponse.lower() == 'n' or strResponse.lower() == 'no':
                    arrData.append(False)
                    blnNext = True
                else:
                    print('[!] Enter Yes or No. Entry not recognized.')

    #Totals not sent yet for the day
    arrData.append(False)
    print("Testing phone information...")
    sms = textmessaging(None, None)
    sms.testText(arrData)
    vault.Insert('SETTINGS', arrData)
    print("You're all set! " + arrData[1] + " was added to the vault and you should have recieved a text.")