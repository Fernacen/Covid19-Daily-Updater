#!/usr/bin/env python
import vault
import enum
import initsetup
from collector import collection
import phonesetup
import phonemodify
from multiprocessing import Process
import time




def Startup():
    blnFile, blnDB = vault.Exist('file')
    if not blnFile:
        #intialize
        print(verbose.firstuse.value)
        strInput = input().lower()

        if strInput == '':
            print("Setting up data files...")
            initsetup.Initialize()
        else:
            exit()
    else:
        #continue to main menu
        print(verbose.normaluse.value)

    #Dive into main menu
    MainMenu()



def MainMenu():
    strInput = None
    print(commandpalette.mainmenu.value)
    while strInput != 'exit':
        strInput = input().lower()

        if strInput == 'help':
            print(verbose.help.value)
            continue

        elif strInput == 'config':
            Configure()
            continue

        elif strInput == 'reset':
            Reset()
            continue

        elif strInput == 'start':
            Start()

        else:
            print(verbose.invalid.value)

    print(verbose.exit.value)

def Reset():
    strInput = None
    print(commandpalette.resetmenu.value)

    while strInput != 'cancel' or strInput != 'c':
        strInput = input().lower()
        # create a device
        if strInput == 'all':
            print("Starting the reset process...")
            vault.Clear('reset')
            continue

        elif strInput == 'phones':
            vault.Clear('all_phones')
            print("Done.")
            continue
            # go back to main menu

        elif strInput == 'cancel' or strInput == 'c':
            MainMenu()
            continue

        elif strInput == 'help':
            print(verbose.help.value)
            continue

        else:
            print(verbose.invalid.value)


#Set up or change device information
def Configure():
    strInput = None
    print(commandpalette.configmenu.value)

    while strInput != 'cancel' or strInput != 'c':
        strInput = input().lower()
        #create a device
        if strInput == 'new':
            phonesetup.CreateNew()
            continue

        #delete a device
        elif strInput == 'delete':
            strResult = vault.Get("udnuid", False)
            if strResult == None:
                print('There are no phones to delete')
            else:
                print('Enter the phone to delete (eg.: 3):')
                for phone in strResult:
                    print(phone.count() + '\t' + phone)
                strResult = vault.Clear("phone", phone[strInput])
                print(strResult)
            continue

        #change a device's settings
        elif strInput == 'modify':
            strEntries = vault.Get("uidudn")
            if strEntries == None:
                print('There are no phones to modify.')
            else:
                phonemodify.Modify()
                continue

        #go back to main menu
        elif strInput == 'cancel' or strInput == 'c':
            MainMenu()
            continue

        elif strInput == 'help':
            print(verbose.help.value)
            continue

        else:
            print(verbose.invalid.value)

def Start():
    arrEntries = vault.Get('all')
    lstThreads = list()
    strThread = "thread "
    intInc = 0
    while True:
        for arrEntry in arrEntries:
            intInc += 1
            strThread += str(intInc)
            c = collection(vault.Security('D', arrEntry[2]), arrEntry[3], arrEntry[4], False, arrEntry[0])
            p = Process(target=c.GetReport(), name=strThread)
            p.start()
            p.join()
            time.sleep(10)

class verbose(enum.Enum):
    normaluse = \
        'Covid-19 Daily Updater\t\tVer0.2.0\n'
    firstuse = \
        ('Thank you for using the Covid-19 Daily Updater\n'
         'Ver0.2.0\n'
         'Information about this program can be found at: https://github.com/Fernacen/Covid19-Daily-Update/\n'
         'If you encountered an error, please report it to the developer via: https://tizeka.io/report\n\n'
         'PLEASE READ THE STARTUP GUIDE BEFORE CONTINUING.\n\n'

         'Let\'s get started. Press Enter to set up the data vault...')
    help = \
        ('----HELP----\n\n'
         'Covid-19 Daily Updater\t\tVer0.2.0\n'
         'Information about this program is on GitHub at: https://github.com/Fernacen/Covid19-Daily-Update/\n'
         'If you encountered an error, please report it to the developer via: https://tizeka.io/report\n\n'
         'config:\n'
         '\tAllows you to enter phone numbers, remove phone numbers, enter host email information,\n'
         '\tschedule update times, select update format, select if you want to be notified about a\n'
         '\tstay at home order.\n\n'
         '\t\tnew:\n'
         '\t\t\tEnter a new phone number and set it up for messages.\n'
         '\t\tdelete:\n'
         '\t\t\tDelete a phone number.\n'
         '\t\tmodify:\n'
         '\t\t\tModify a phone number and it\'s settings.\n\n'
         'reset:\n'
         '\tAllows you to reset some or all of the settings in the application.\n\n'
         '\t\tall:\n'
         '\t\t\tResets all settings, and security features.\n'
         '\t\tphones:\n'
         '\t\t\tDeletes all phone numbers.\n\n'
         'start:\n'
         '\tStarts the application. You will need to stop the application to make changes.\n\n'
         'stop:\n'
         '\tStops the program so you can make changes to it.\n\n'
         'cancel:\n'
         '\tCancels the current menu and brings you back to the main menu.\n'
         'exit:\n'   
         '\tExit terminates the program. Your settings and data, if any, will remain.\n')
    config = \
        ('----CONFIGURATION----\n\n'
         'Due to security reasons, you must delete a phone if you wish to change the email or password\n'
         'associated with it.\n\n')
    reset = \
        ('----RESET----\n\n' \
         'Imformation selected to be reset cannot be restored.\n')
    start = \
        'Starting...\n'
    exit = \
        'Shutting down...\n'
    invalid = \
        'Command not recognized, please try again.\n'

class commandpalette(enum.Enum):
    mainmenu = \
        ('Available commands are:\n'
         '\thelp, config, reset, stop, start, exit\n')
    configmenu = \
        ('Available commands are:\n'
         '\tnew, delete, modify, cancel\n')
    resetmenu = \
        ('Available commands are:\n'
         '\tall, phones, cancel\n')
    confirmation = \
        ('Are you sure you want to perform this action?'
         '\tyes, no\n')

if __name__=="__main__":
    Startup()
