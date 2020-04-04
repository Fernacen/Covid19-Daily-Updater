import os
import sqlite3 as sql3
import enum
import initsetup
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

#Create folders and databases

#module-wide variables
strSupportPath = os.path.join(os.path.expanduser('~'), 'CDU', 'Support')
strDatabasePath = os.path.join(os.path.expanduser('~'), 'CDU', 'Database')

sqlConnection = None
sqlCMD = None



#check to see if the folder paths exist
def Exist(strAction):
    global strSupportPath
    global strDatabasePath
    # checks if the file eixsts
    if strAction == 'file':
        if not os.path.exists(os.path.join(strSupportPath, 'key.bin')):
            blnSupport = False
        else:
            blnSupport = True

        if not os.path.exists(os.path.join(strDatabasePath, 'vault.db')):
            blnDatabase = False
        else:
            blnDatabase = True

    #checks if the folder exists
    else:
        if not os.path.exists(strSupportPath):
            blnSupport = False
        else:
            blnSupport = True

        if not os.path.exists(strDatabasePath):
            blnDatabase = False
        else:
            blnDatabase = True

    return blnSupport, blnDatabase


def SpinUp():
    global sqlConnection
    global sqlCMD
    sqlConnection = sql3.connect(os.path.join(strDatabasePath, 'vault.db'))
    sqlCMD = sqlConnection.cursor()


def ShutDown():
    sqlCMD.close()

def Key(strPath):
    
    bytKey = get_random_bytes(32)

    with open(strPath, "wb") as objFile:
        objFile.write(bytKey)


#update the data into the database
def Update(strSelection, strData):
    strSelection == strSelection.lower()
    SpinUp()

    if strSelection == "phone_num":
        #create new entry and save phone email
        strData = Security('E', strData[0])
        sqlCMD.execute('''UPDATE SETTINGS SET Phone_Num=? WHERE UID=?''', (strData, strData[1]))
        sqlConnection.commit()

    if strSelection == "aws":
        #create new entry and save phone email
        strData = Security(strData[0], 'E')
        sqlCMD.execute('''UPDATE SECRETS SET Access_ID=?, Access_Key=? WHERE UID=1''', (strData[0], strData[1]))
        sqlConnection.commit()

    elif strSelection == "udn":
        #save the SAH as true if detected
        print(strData[0])
        sqlCMD.execute('''UPDATE SETTINGS SET UDN=? WHERE UID=?''', (strData[0], strData[1]))
        sqlConnection.commit()

    elif strSelection == "sah_notified":
        #save the SAH as true if detected
        sqlCMD.execute('''UPDATE SETTINGS SET SAH_Notified=? WHERE UID=?''', (strData[0], strData[1]))
        sqlConnection.commit()

    elif strSelection == "totals_collected":
        #save the SAH as true if detected
        sqlCMD.execute('''UPDATE SETTINGS SET Totals_Collected=? WHERE UID=?''', (strData[0], strData[1]))
        sqlConnection.commit()

    elif strSelection == "usr_location":
        #save the host email port address
        sqlCMD.execute('''UPDATE SETTINGS SET Usr_Location=? WHERE UID=?''', (strData[0], strData[1]))
        sqlConnection.commit()

    ShutDown()


def Insert(strDB, arrData):

    strDB = strDB.upper()
    SpinUp()

    if strDB == 'SECRETS':
        print(arrData[1] + arrData[2])
        sqlString = '''INSERT INTO %s VALUES ( ?, ?, ?);''' % strDB
        sqlCMD.execute(sqlString, (arrData[0], Security('E', arrData[1]), Security('E', arrData[2])))

    else:
        sqlString = '''INSERT INTO %s VALUES ( ?, ?, ?, ?, ?, ?);''' % strDB
        sqlCMD.execute(sqlString, (arrData[0], arrData[1], Security('E', arrData[2]), arrData[3], arrData[4],  arrData[5]))

    sqlConnection.commit()
    ShutDown()

def Initialize():
    sqlCMD.execute('''CREATE TABLE SETTINGS ([UID] INTEGER PRIMARY KEY, [UDN] text, [Phone_Num] blob, 
    [Usr_Location] text, [SAH_Notified] boolean, [Totals_Collected] boolean)''')

    sqlCMD.execute('''CREATE TABLE SECRETS ([UID] INTEGER PRIMARY KEY, [Access_ID] text, [Access_Key] test)''')
    sqlConnection.commit()

#retrieves the data from the database
def Get(strSelection, strData=None):

    strSelection == strSelection.lower()
    SpinUp()
    if strSelection == "phone_num":
        # get the phone email
        sqlCMD.execute('''SELECT Phone_Num FROM SETTINGS WHERE UID=?''', (strData))
        strResult = sqlCMD.fetchone()[0]
        strResult = Security('D', strResult)

    elif strSelection == "access_id":
        # get host email
        sqlCMD.execute('''SELECT Access_ID FROM SECRETS WHERE UID=1''')
        strResult = sqlCMD.fetchone()[0]
        strResult = Security('D', strResult)

    elif strSelection == "access_key":
        # get host email
        sqlCMD.execute('''SELECT Access_Key FROM SECRETS WHERE UID=1''')
        strResult = sqlCMD.fetchone()[0]
        strResult = Security('D', strResult)

    elif strSelection == "all":
        # get everything
        sqlCMD.execute('''SELECT * FROM SETTINGS''')
        strResult = sqlCMD.fetchall()

    elif strSelection == "uidudn":
        # get UDNs
        sqlCMD.execute('''SELECT UID, UDN FROM SETTINGS''')
        strResult = sqlCMD.fetchall()

    elif strSelection == "sah_notified":
        # get the SAH as true if detected
        sqlCMD.execute('''SELECT SAH_Notified FROM SETTINGS WHERE UID=?''', (strData))
        strResult = sqlCMD.fetchone()[0]

    elif strSelection == "usr_location":
        # get the host email port address
        sqlCMD.execute('''SELECT Usr_Location FROM SETTINGS WHERE UID=?''', (strData))
        strResult = sqlCMD.fetchone()[0]

    elif strSelection == "totals_collected":
        # get the host email port address
        sqlCMD.execute('''SELECT Totals_Collected FROM SETTINGS WHERE UID=?''', (strData))
        strResult = sqlCMD.fetchone()[0]

    ShutDown()
    return strResult


def Clear(strSelection, strData=None):

    strSelection = strSelection.lower()

    if strSelection == "phone":
        SpinUp()
        #delete phone number and its settings from database
        sqlCMD.execute('''DELETE FROM SETTINGS WHERE UID=?''', (strData))
        sqlCMD.commit()
        ShutDown()

    if strSelection == "all_phones":
        SpinUp()
        #delete all phone numbers and their settings from database
        sqlCMD.execute('''TRUNCATE TABLE SETTINGS''')
        sqlCMD.commit()
        ShutDown()

    elif strSelection == "reset":
        #destroy database and key
        strKey, strDB = Exist('file')

        if strDB == True:
            os.remove(os.path.join(strDatabasePath, 'vault.db'))
        if strKey == True:
            os.remove(os.path.join(strSupportPath, 'key.bin'))

        #create the database and key again
        setup.Initialize()


#encrypts or decrypts data
def Security(strSelection, strData):
    
    if strSelection.upper() == 'E':

        with open((os.path.join(os.path.expanduser('~'), 'CDU', 'Support', 'key.bin')), "rb") as objFile:
            bytKey = objFile.read()

        objCipher = AES.new(bytKey, AES.MODE_CFB)
        strEncrypted = objCipher.iv + objCipher.encrypt(strData.encode('utf-8'))
        return strEncrypted

    else:
        with open((os.path.join(os.path.expanduser('~'), 'CDU', 'Support', 'key.bin')), "rb") as objFile:
            bytKey = objFile.read()

        bytIV = strData[:16]

        objCipher = AES.new(bytKey, AES.MODE_CFB, iv=bytIV)
        strDecrypted = objCipher.decrypt(strData[16:]).decode('utf-8')
        return strDecrypted
