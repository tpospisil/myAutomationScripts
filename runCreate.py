#! python3/usr/bin/env

import ssl, sys
import argparse
from testrail import *
from jira import JIRA


def getSuiteId(userInput, id_dict):
    suite_id = id_dict[userInput]['suite_id']
    return (suite_id)


def main():

    parser = argparse.ArgumentParser(description='Creates TestRail Test Runs and Jira tasks for test execution')
    parser.add_argument('--filter', dest='filter', action='store_false',
                        help='will also add test cases which have been automated')
    args = parser.parse_args()

    user_details = {
        'id': 'ATLASSIAN ID HERE',
        'email': 'EMAIL HERE',
        'jiraKey': 'ATLASSIAN KEY HERE',
        'testrailKey': 'TESTRAIL KEY HERE'
    }

    ssl._create_default_https_context = ssl._create_unverified_context

    # Provide authentication details for accessing TestRail's API
    client = APIClient('https://snapsheet.testrail.io/')
    client.user = user_details['email']
    client.password = user_details['testrailKey']


    # Dictionary to hold relevant IDs from QA Regression project
    id_dict = {1: {'suite_id': 64,
                   'project': 'S2'
                   },
               2: {'suite_id': 112,
                   'project': 'VICE'
                   },
               3: {'suite_id': 92,
                   'project': 'SnapTx'
                   },
               4: {'suite_id': 67,
                   'project': 'Shops'
                   },
               5: {'suite_id': 66,
                   'project': 'Hertz'
                   },
               6: {'suite_id': 68,
                   'project': 'S1'
                   },
               7: {'suite_id': 78,
                   'project': 'Turo'
                   },
               8: {'suite_id': 69,
                   'project': 'Policy App'
                   }
               }

    print(
          '\n[1] Standard 2\n'
          '[2] VICE\n'
          '[3] SnapTx\n'
          '[4] Shops\n'
          '[5] Hertz\n'
          '[6] Standard 1\n'
          '[7] Turo\n'
          '[8] Policy',
          )

    userInput = int(input('\nEnter the key (1 - 8) corresponding to the product for which you\'d like to create a new run: '))

    while userInput not in range(len(id_dict) + 1) or userInput == 0:
        try:
            userInput = int(input())
        except:
            print('That\'s not a number...')
            sys.exit(1)

    caseIdArray = []
    testCases = client.send_get("get_cases/10&suite_id=%s" % (str(getSuiteId(userInput, id_dict))))
    for index in range(len(testCases)):
        if testCases[index]['custom_test_case_automated'] is not True:
            caseIdArray.append(testCases[index]['id'])

    buildName = input('\nPlease enter a name for the new build: ')

    if args.filter is not False:
        newRun = client.send_post('add_run/10', {
            'suite_id': getSuiteId(userInput, id_dict),
            'name': buildName,
            'include_all': False,
            'case_ids': caseIdArray
        })
    else:
        newRun = client.send_post('add_run/10', {
            'suite_id': getSuiteId(userInput, id_dict),
            'name': buildName,
            'include_all': True
        })

    # Provide authentication details for Jira
    options = {'server': 'https://snapsheettech.atlassian.net/'}
    jira = JIRA(options, basic_auth=(user_details['email'], user_details['jiraKey']))

    createTask = input('\nDo you want to create a Jira task for this test run? (Yes/No): ')

    while createTask.lower() not in ['y','n','yes','no']:
        try:
            createTask = input('Try again...')
        except:
            pass

    if createTask.lower() in ['y', 'yes']:
        task = jira.create_issue(project='QA', summary='%s - Regression Run' % buildName, issuetype={'name': 'Task'},
                                 description=newRun['url'], assignee={'id': user_details['id']})

        addToSprint = input('\nDo you want to add the task to the current sprint? (Yes/No): ')

        while addToSprint.lower() not in ['y', 'n', 'yes', 'no']:
            try:
                addToSprint = input('Try again...')
            except:
                pass

        if addToSprint.lower() in ['y', 'yes']:
            sprints = jira.sprints(30, maxResults=None)
            jira.add_issues_to_sprint(sprints[len(sprints)-1].id, [task.key])
    else:
        pass

    print("\nHere\'s the URL for the new %s build: %s \n" % (id_dict[userInput]['project'], newRun['url']))

if __name__ == "__main__":
    main()