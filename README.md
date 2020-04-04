# Covid19 Daily Updater

Covid19 Daily Updater (CDU) is a program designed to send you texts daily with Covid19 totals over the past two days. Additionally it alerts you of recent 'Stay at Home' orders from your local state/province. This program is designed to only work with the 50 states in the USA at this time.

Messaging and data rates may apply. See your phone contract for details.

## Installation

pip install -r path/to/requrements.txt

python3 path/to/controller.py

## Usage

This program is still in development and unstable. Refer to the requirements, definitions, and setup documents.

YOU MUST HAVE AN AWS ACCOUNT.
STEPS:
1) Go to https://aws.amazon.com/
2) Sign up for an account (it's free)
3) In the top right corner in the AWS Managment Console, nex to your name, ensure one of the three is selected:
 - us-west-2
 - us-east-1
 - us-west-1
4) In the AWS services box, search for "IAM" or "Identity and Access Management"
5) On the IAM page, select from the dropdowns "Create individual IAM users" and then "Manage Users"
6) In the view, select "Add user" ensure the following:
 - User name: (Anything you like)
 - Access type: PROGRAMMATIC ACCESS
7) Hit next and select "Attach existing policies directly"
8) In the search bar, search for "SNS" and tick the checkbox next to "AmazonSNSFullAccess"
9) Hit twice until you reach the Review page. Hit create user.
10) COPY your Access Key ID and Secret Access Key. You will need these to set up the Covid19 Daily Updater.

Current offerings:
 - Insert new phones
 - Delete phones
 - Modify phones
 - Start the process
 - Reset the entire program
 - Reset the phone database

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
