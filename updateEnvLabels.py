#! python3/usr/bin/env
import sys
import requests
from requests.auth import HTTPBasicAuth
from jira import JIRA, JIRAError


# Determine if user input represents a valid selection
def isInOptions(optionList):
    userInput = input()
    while userInput.lower() not in optionList:
        try:
            userInput = input('Invalid selection. Try again...\n')
        except:
            print('Ya blew it...')
            sys.exit(1)

    return userInput


# Function to check user input for spaces
def checkForSpace(prompt):
    userInput = input(prompt)
    while (' ' in userInput) == True:
        try:
            userInput = input('\"Environment Deployed To\" labels should not contain spaces. Try again: ')
        except:
            print('Ya blew it...')
            sys.exit(1)

    return userInput


# Function to ingest labels to add/remove
def createChangeList(operation):
    userInput = input('\nHow many labels would you like to %s?: ' % operation)
    try:
        numberOfLabels = int(userInput)
    except ValueError:
        print('Ya blew it...')
        sys.exit(1)

    changeList = []
    for i in range(0, numberOfLabels):
        labelItem = checkForSpace('%s label %s: ' % (operation, i+1))
        changeList.append(labelItem)

    return changeList


def main():

    # Authenticate
    options = {'server': 'https://snapsheettech.atlassian.net/'}
    jira = JIRA(options, basic_auth=('EMAIL HERE', 'API KEY HERE'))
    api_auth = HTTPBasicAuth('EMAIL HERE', 'API KEY HERE')


    # Input and validate JQL query
    query = input('Please provide the JQL query for the issues which you would like to update:\n')
    try:
        issues = jira.search_issues(query, maxResults=None)
    except JIRAError as e:
        print('Error: ' + e.text)
        sys.exit(1)


    # Check if query matches expected output
    print('\nThis query returned %s issues. Would you like to continue?: ' % str(len(issues)))
    proceed = isInOptions(['y','n','yes','no'])
    if proceed.lower() in ['n','no']:
        print('Come back when you find the right query.')
        sys.exit(1)


    # Ask user if they'd like to add or remove a label (or both)
    print('\nDo you want to add or remove a label (or both)?')
    addRemove = isInOptions(['add', 'remove', 'both'])

    # Grab labels to add/remove
    if addRemove in ['add','both']:
        addLabels = createChangeList('Add')
    if addRemove in ['remove','both']:
        removeLabels = createChangeList('Remove')


    # Issue queries are broken up into 100 issue chunks due to limitations of the Jira API
    block_num = 0
    block_size = 100

    while True:
        # Send queries to find matching issues
        start_idx = block_num * block_size
        issues = jira.search_issues(query, startAt=start_idx, maxResults=block_size)

        if len(issues) == 0:
            break
        block_num += 1

        for issue in issues:
            # Create new label list with existing labels
            newLabelList = []
            try:
                for label in issue.fields.customfield_10158:
                    newLabelList.append(label)
            except TypeError:
                pass

            # Append addLabels
            if addRemove in ['add', 'both']:
                for label in addLabels:
                    if label not in newLabelList:
                        newLabelList.append(label)

            # Remove removeLabels
            if addRemove in ['remove','both']:
                for label in removeLabels:
                    try:
                        newLabelList.remove(label)
                    except ValueError:
                        pass # do nothing


            print('Updating %s' % (issue.key))
            response = requests.put(
                'https://snapsheettech.atlassian.net/rest/api/2/issue/%s' % (issue.key),
                auth = api_auth,
                json = {
                  'fields': {
                    'customfield_10158': newLabelList
                  }
                }
            )


    print('All done!')


if __name__ == "__main__":
    main()