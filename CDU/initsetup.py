import os
import vault



def Initialize():

    blnSupportExists, blnDBExists = vault.Exist('folder')


    if not blnSupportExists:
        os.makedirs(vault.strSupportPath)

    vault.Key(os.path.join(vault.strSupportPath, 'key.bin'))

    if not blnDBExists:
        os.makedirs(vault.strDatabasePath)

        #Start up the vault and initialize for first use
        vault.SpinUp()
        vault.Initialize()

        NewTokens()

        #Shut down vault
        vault.ShutDown()

    print("Setup complete!\n")

def NewTokens():

    strResponse = []
    strResponse.append(None)

    # Collect data for AWS account
    print('Please enter your AWS Access Key ID:')

    strResponse.append((input()))
    print('Please enter your AWS Secret Access Key:')
    strResponse.append((input()))

    # Insert AWS info to SECRETS DB
    vault.Insert('SECRETS', strResponse)
