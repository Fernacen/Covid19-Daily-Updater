import boto3
import vault

class textmessaging:
    def __init__(self, strPhoneNumber, strMessageBody):
        self.strPhoneNumber = strPhoneNumber
        self.strMessageBody = strMessageBody

        self.aws = boto3.Session(
            aws_access_key_id=vault.Get('access_id'),
            aws_secret_access_key=vault.Get('access_key'),
            region_name='us-east-1'
        )
        self.message = self.aws.client('sns')

    def sendText(self):

        strRresponse = self.message.publish(
            PhoneNumber=self.strPhoneNumber,
            Message=self.strMessageBody,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': 'COVID19'
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            })

        return strRresponse

    def testText(self, arrData):

        strMessage = "If you have recieved this text, you have set up the COVID-19 Daily Updater correctly."
        strRresponse = self.message.publish(
            PhoneNumber=arrData[2],
            Message=strMessage,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': 'COVID19'
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Transactional'
                }
            })

        return strRresponse


