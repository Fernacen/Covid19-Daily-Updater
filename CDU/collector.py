from datetime import datetime, timedelta
import csv
import os
import requests
import vault
from smsmanager import textmessaging



strBaseURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/%s.csv'

class collection:




    def __init__(self, strPhoneNum, strState, blnSAH, blnShutdown, intUID):
        self.blnSAH = blnSAH
        self.blnShutdown = blnShutdown
        self.strPhoneNum = strPhoneNum
        self.strStateName = strState
        self.intUID = intUID



    def GetReport(self):
        blnDataCapture = vault.Get('totals_collected', str(self.intUID))
        blnSAHNotified = vault.Get('sah_notified', str(self.intUID))



        if blnSAHNotified  == True:
            self.__GetGov(self.strStateName)

        if datetime.utcnow().strftime("%H:%M:%S") >= "00:15:00" and not blnDataCapture:
            try:
                csvReport = requests.get(strBaseURL % (datetime.utcnow() - timedelta(days=1)).strftime("%m-%d-%Y")).text
                csvEntries = list(csv.reader(csvReport.splitlines()))

                tplIndexes = self.__FindColumns(csvEntries[0])
                tplResultsToday = self.__FindRows(csvEntries, tplIndexes[3], tplIndexes[2], tplIndexes[1], tplIndexes[0])

                csvReport = requests.get(strBaseURL % (datetime.utcnow() - timedelta(days=2)).strftime("%m-%d-%Y")).text
                csvEntries = list(csv.reader(csvReport.splitlines()))

                tplIndexes = self.__FindColumns(csvEntries[0])
                tplResultsYesterday = self.__FindRows(csvEntries, tplIndexes[3], tplIndexes[2], tplIndexes[1],
                                                  tplIndexes[0])

                self.__SendTotals(tplResultsToday, tplResultsYesterday)

                blnDataCapture = True
                arrData = [True, self.intUID]
                vault.Update('totals_collected', arrData)
            except:
                #might not exist yet
                print("Error collecting daily totals")
                blnDataCapture = False

        elif blnDataCapture and datetime.utcnow().strftime("%H:%M:%S") >= "23:55:00":
            blnDataCapture = False
            arrData = [False, str(self.intUID)]
            vault.Update('totals_collected', arrData)

        return



    def __GetGov(self, strState):
        strPath = os.path.split(os.path.abspath(__file__))
        strGovURL = None
        with open(os.path.join(strPath[0], 'StateInfo.csv')) as csvFile:
            csvEntries = list(csv.reader(csvFile))
            for row in csvEntries:
                if row[1] == strState:
                    strGovURL = row[2]
                    strStateNm = row[1]

        objWebpage = requests.get(strGovURL)
        if "stay at home order" in objWebpage.text.lower() or \
            "shelter in place order" in objWebpage.text.lower() or \
            "stay home order" in objWebpage.text.lower():

            strMessage = strStateNm + " has issued a shelter in place order. Learn more here: \n" + strGovURL
            self.blnSAH = False #Do not notify again
            sms = textmessaging(self.strPhoneNum, strMessage)
            sms.sendText()
            arrData = [False, str(self.intUID)]
            vault.Update('sah_notified', arrData)



    def __SendTotals(self, tplResultsToday, tplResultsYesterday):
        strMessage = "COVID 19 Daily Updater\n" + "Totals for " + (datetime.utcnow() - timedelta(days=1)).strftime("%m-%d-%Y") + " " + self.strStateName + "\n" \
                     "Cases: " + str(tplResultsToday[0]) + " -- " + str(self.__DoMath(tplResultsToday[0], tplResultsYesterday[0])) + "% Change\n" \
                     "Dead: " + str(tplResultsToday[1]) + " -- " + str(self.__DoMath(tplResultsToday[1], tplResultsYesterday[1])) + "% Change\n" \
                     "Recovered: " + str(tplResultsToday[2]) + " -- " + str(self.__DoMath(tplResultsToday[2], tplResultsYesterday[2])) + "% Change\n"

        sms = textmessaging(self.strPhoneNum, strMessage)
        sms.strMessageBody = strMessage
        sms.sendText()
        print("Update for " + self.strStateName + " sent.")

    def __DoMath(self, intCurrent, intLast):
        if intCurrent != 0 and intLast != 0:
            intIncrease = intCurrent - intLast
            intPercent = round((intIncrease/intLast)*100, 2)
        else:
            #don't do math! :U
            intPercent = 0
        return intPercent

    def __FindRows(self, csvEntries, intStateColumn, intConfColumn, intDeathColumn, intRecColumn):
        intTotalDeath = 0
        intTotalRec = 0
        intTotalConf = 0
        for row in csvEntries:
            if row[intStateColumn] == self.strStateName:
                intTotalConf += int(row[intConfColumn])
                intTotalDeath += int(row[intDeathColumn])
                intTotalRec += int(row[intRecColumn])
        return intTotalConf, intTotalDeath, intTotalRec

    def __FindColumns(self, csvEntries):
        intStateColumn = 0
        intConfColumn = 0
        intDeathColumn = 0
        intRecColumn = 0

        for column in csvEntries:
            if "state" in column.lower():
                intStateColumn = csvEntries.index(column)
            if "confirmed" in column.lower():
                intConfColumn = csvEntries.index(column)
            if "deaths" in column.lower():
                intDeathColumn = csvEntries.index(column)
            if "recovered" in column.lower():
                intRecColumn = csvEntries.index(column)

        return intRecColumn, intDeathColumn, intConfColumn, intStateColumn



