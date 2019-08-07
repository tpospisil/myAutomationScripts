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
        'name': 'ENTER NAME HERE',
        'email': 'ENTER EMAIL HERE'
    }

    ssl._create_default_https_context = ssl._create_unverified_context

    # Provide authentication details for accessing TestRail's API
    client = APIClient('https://snapsheet.testrail.io/')
    client.user = user_details['email']
    client.password = 'ENTER API KEY HERE'


    # Dictionary to hold relevant IDs from QA Regression project
    id_dict = {1: {'plan_id': 150,
                   'configGroup_id': 16,
                   'suite_id': 64,
                   'project': 'S2'
                   },
               2: {'plan_id': 184,
                   'configGroup_id': 24,
                   'suite_id': 112,
                   'project': 'VICE'
                   },
               3: {'plan_id': 233,
                   'configGroup_id': 28,
                   'suite_id': 92,
                   'project': 'SnapTx'
                   },
               4: {'plan_id': 142,
                   'configGroup_id': 18,
                   'suite_id': 67,
                   'project': 'Shops'
                   },
               5: {'plan_id': 138,
                   'configGroup_id': 13,
                   'suite_id': 66,
                   'project': 'Hertz'
                   },
               6: {'plan_id': 159,
                   'configGroup_id': 19,
                   'suite_id': 68,
                   'project': 'S1'
                   },
               7: {'plan_id': 192,
                   'configGroup_id': 25,
                   'suite_id': 78,
                   'project': 'Turo'
                   },
               8: {'plan_id': 154,
                   'configGroup_id': 17,
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

    newConfig = client.send_post('add_config/' + configGroup_id, {'name': buildName})

    addNewConfig = client.send_post('add_plan_entry/' + plan_id, {
        'suite_id': suite_id,
        'include_all': True,
        'config_ids': [newConfig['id']],
        'runs': [
            {
            'included_all': True,
            'config_ids': [newConfig['id']]
            }
        ]
    })


    # Provide authentication details for Jira
    options = {'server': 'https://snapsheettech.atlassian.net/'}
    jira = JIRA(options, basic_auth=(user_details['email'], 'ENTER API TOKEN HERE'))

    createTask = input('Do you want to create a Jira task for this test run? (Yes/No): ')

    while createTask.lower() not in ['y','n','yes','no']:
        try:
            createTask = input('Try again...')
        except:
            pass

    if createTask.lower() in ['y','yes']:
        jira.create_issue(project='QA', summary='Regression Run - %s' % buildName, issuetype='Task',
                          description=addNewConfig['runs'][0]['url'], assignee={'name':user_details['name']})
    else:
        pass

    print("\nHere\'s the URL for the new " + id_dict[userInput]['project'] + " build: " + addNewConfig['runs'][0]['url'] + "\n")

if __name__ == "__main__":
    main()