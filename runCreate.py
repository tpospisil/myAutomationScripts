#! python3/usr/bin/env

import ssl, sys
from testrail import *
from jira import JIRA


def relevantIDs(userInput, id_dict):
    plan_id = str(id_dict[userInput]['plan_id'])
    configGroup_id = str(id_dict[userInput]['configGroup_id'])
    suite_id = id_dict[userInput]['suite_id']
    return (plan_id, configGroup_id, suite_id)


def main():

    user_details = {
        'id': 'ATLASSIAN ID HERE',
        'email': 'JIRA/TESTRAIL EMAIL HERE',
        'jiraKey': 'JIRA API KEY HERE',
        'testrailKey': 'TESTRAIL API KEY HERE'
    }

    ssl._create_default_https_context = ssl._create_unverified_context

    # Provide authentication details for accessing TestRail's API
    client = APIClient('https://snapsheet.testrail.io/')
    client.user = user_details['email']
    client.password = user_details['testrailKey']


    # Dictionary to hold relevant IDs from QA Regression project
    id_dict = {1: {'plan_id': 150,
                   'suite_id': 64,
                   'project': 'S2'
                   },
               2: {'plan_id': 184,
                   'suite_id': 112,
                   'project': 'VICE'
                   },
               3: {'plan_id': 233,
                   'suite_id': 92,
                   'project': 'SnapTx'
                   },
               4: {'plan_id': 142,
                   'suite_id': 67,
                   'project': 'Shops'
                   },
               5: {'plan_id': 138,
                   'suite_id': 66,
                   'project': 'Hertz'
                   },
               6: {'plan_id': 159,
                   'suite_id': 68,
                   'project': 'S1'
                   },
               7: {'plan_id': 192,
                   'suite_id': 78,
                   'project': 'Turo'
                   },
               8: {'plan_id': 154,
                   'suite_id': 69,
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

    plan_id, configGroup_id, suite_id = relevantIDs(userInput, id_dict)

    buildName = input('\nPlease enter a name for the new build: ')

    newRun = client.send_post('add_run/10', {
        'suite_id': suite_id,
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


    print("\nHere\'s the URL for the new " + id_dict[userInput]['project'] + " build: " + newRun['url'] + "\n")

if __name__ == "__main__":
    main()