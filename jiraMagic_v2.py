#! python3/usr/bin/env

import sys
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


# Create new list of labels for 'FixVersion' or 'Environment Deployed To' for each issue
def appendDeployLabels(issueMethod, newValue):
    newLabelList = []
    try:
        for label in issueMethod:
            if isinstance(label, str) == True:
                newLabelList.append(label)
            else:
                newLabelList.append({'name': label.name})
    except TypeError:
        pass
    newLabelList.append(newValue)

    return newLabelList


def main():

    statusDict = {'integration':
                      {'transitionId': 61,
                       'status': 'DELIVERED',
                       'environmentLabel': 'integration'
                       },
                  'zurich-uat':
                      {'environmentLabel': 'zurich-uat'
                       },
                  'us-uat':
                      {'environmentLabel': 'us-uat'
                      },
                  'uat-1':
                      {'environmentLabel': 'uat-1'
                       }
                  }

    # Determine which product is to be deployed
    print('Is this a \"VICE\", \"Workflow\", or \"Dispatch\" deployment?')
    product = isInOptions(['vice', 'vc', 'dispatch', 'dis', 'workflow', 'wrk'])

    # Determine to which environment changes are to be deployed
    print('To which environment are you deploying? [integration, zurich-uat, us-uat]')
    environment = isInOptions(['integration', 'zurich-uat', 'us-uat'])


    # Assign appropriate values to variables based on selections
    if product.lower() in ['vice','vc']:
        project = 'VC'
    elif product.lower() in ['dispatch', 'dis']:
        project = 'DIS'
    elif product.lower() in ['workflow', 'wrk']:
        project = 'WRK'
    else:
        print('Whomp whomp... Something went wrong.')
        sys.exit(1)
    # project = 'SBX'

    # Authenticate
    options = {'server': 'https://snapsheettech.atlassian.net/'}
    jira = JIRA(options, basic_auth=('EMAIL HERE', 'API KEY HERE'))

    # Create new version in the appropriate project. Use existing version if matching version already exists.
    version = input('Please provide a name for the Fix Version: ')
    try:
        newVersion = jira.create_version(version,project)
    except JIRAError as e:
        if 'A version with this name already exists' in e.text:
            projectVersions = jira.project_versions(project)
            for i in range(len(projectVersions)):
                if projectVersions[i].name == version:
                    newVersion = projectVersions[i]
            pass
        # Abort if another error is thrown
        else:
            print('Something went wrong. Error: ' + e.text)
            sys.exit(1)

    # Transition issues and add new Fix Version
    print('\nWorking... This may take some time.\n')

    # Issue queries are broken up into 100 issue chunks due to limitations of the Jira API
    block_num = 0
    block_size = 100

    while True:
        # Send queries to find matching issues
        start_idx = block_num * block_size
        if environment == 'integration':
            issues = jira.search_issues(
                'project = %s AND status = %s order by created DESC' % (project, statusDict[environment.lower()]['status']),
                startAt=start_idx,
                maxResults=block_size)
        else:
            issues = jira.search_issues(
                'project = %s AND "Environment Deployed To" = integration AND "Environment Deployed To" != %s order by created DESC'
                % (project, statusDict[environment.lower()]['environmentLabel']),
                startAt=start_idx,
                maxResults=block_size)

        if len(issues) == 0:
            break
        block_num += 1

        for issue in issues:
            # Fetch version and environment labels and append new value
            fixVersions = appendDeployLabels(issue.fields.fixVersions, {'name': newVersion.name})
            environmentLabels = appendDeployLabels(issue.fields.customfield_10158, statusDict[environment.lower()]['environmentLabel'])

            # Update issues
            if environment == 'integration':
                jira.transition_issue(
                    issue.id,statusDict['integration']['transitionId'],
                    fields={'fixVersions': fixVersions,
                            'customfield_10158': environmentLabels},
                    comment='Issue updated via automation.'
                )
            else:
                issue.update(
                    fields={'fixVersions': fixVersions,
                            'customfield_10158': environmentLabels},
                    comment='Issue updated via automation.'
                )

    print('All done.\n')

if __name__ == "__main__":
    main()