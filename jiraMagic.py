#! python3/usr/bin/env

import sys
from jira.client import JIRA

def main():

    statusDict = {'integration':
                      {'transitionId': 131,
                       'status': 'MERGED'
                       },
                  'uat':
                      {'transitionId': 151,
                       'status': 'APPROVED'
                       }
                  }

    # Determine which product is to be deployed
    product = input('Is this a \"VICE\", \"Workflow\", or \"Dispatch\" deployment?\n')

    while product.lower() not in ['vice','dispatch','dis','vc', 'workflow', 'wrk']:
        try:
            product = input('Invalid selection. Try again...\n')
        except:
            print('Ya blew it...')
            sys.exit(1)

    # Determine to which environment changes are to be deployed
    environment = input('Is this an \"integration\" or \"UAT\" deployment?\n')

    while environment.lower() not in ['integration', 'uat']:
        try:
            environment = input('Invalid selection. Try again...\n')
        except:
            print('Ya blew it...')
            sys.exit(1)

    # if product.lower() in ['vice','vc']:
    #     # project = 'VC'
    # elif product.lower() in ['dispatch', 'dis']:
    #     # project = 'DIS'
    # elif product.lower() in ['workflow', 'wrk']:
    #     project = 'WRK'
    project = 'SBX'

    if environment.lower() == 'integration':
        statusInfo = statusDict['integration']
    else:
        statusInfo = statusDict['uat']


    # Authenticate
    options = {'server': 'https://snapsheettech.atlassian.net/'}
    jira = JIRA(options, basic_auth=('USER EMAIL HERE', 'API KEY HERE'))

    # Create new version in the appropriate project
    version = input('Please provide a name for the Fix Version: ')
    newVersion = jira.create_version(version,project)

    # Transition issues and add new Fix Version
    print('\nWorking... This may take some time.\n')

    # Issue queries are broken up into 100 issue chunks due to limitations of the Jira API
    block_num = 0
    block_size = 100

    while True:
        start_idx = block_num * block_size
        issues = jira.search_issues('project = %s AND status = %s order by created DESC' % (project, statusInfo['status']),
                                    startAt=start_idx,
                                    maxResults=block_size)
        if len(issues) == 0:
            break
        block_num += 1

        for issue in issues:
            fixVersions = []
            for version in issue.fields.fixVersions:
                fixVersions.append({'name': version.name})
            fixVersions.append({'name': newVersion.name})
            jira.transition_issue(issue.id,
                                  statusInfo['transitionId'],
                                  fields={'fixVersions': fixVersions},
                                  comment='Issue transitioned via automation.')

    print('All done.\n')

if __name__ == "__main__":
    main()