#! python3/usr/bin/env

import csv, ssl
import datetime
from testrail import *
from jira.client import JIRA
# from pprint import pprint


def passFailData(raw_data, milestone, passFail_dict, totals):
    for i in range(len(raw_data)):
        if raw_data[i]['milestone_id'] == milestone:
            passFail_dict[raw_data[i]['name']] = {'Passed': raw_data[i]['passed_count'],
                                                  'Failed': raw_data[i]['failed_count'] + raw_data[i]['retest_count'] + raw_data[i]['blocked_count'],
                                                  'Untested': raw_data[i]['untested_count'],
                                                  'Total': raw_data[i]['passed_count'] + raw_data[i]['failed_count'] + raw_data[i]['retest_count'] + raw_data[i]['blocked_count'] + raw_data[i]['untested_count']
                                                  }
            totals['passed'] += passFail_dict[raw_data[i]['name']]['Passed']
            totals['failed'] += passFail_dict[raw_data[i]['name']]['Failed']
            totals['untested'] += passFail_dict[raw_data[i]['name']]['Untested']
            totals['total'] += passFail_dict[raw_data[i]['name']]['Total']

    return passFail_dict


def passFailWriter(passFail_dict, writer):
    for key, val in passFail_dict.items():
        writer.writerow({'Feature': key,
                         'Passed': val['Passed'],
                         'Failed': val['Failed'],
                         'Untested': val['Untested'],
                         'Total': val['Total'],
                         '% Passed': round((val['Passed'] / val['Total']) * 100)
                         })


def main():

    now = datetime.datetime.now().strftime('%m%d%y')

    ssl._create_default_https_context = ssl._create_unverified_context

    # Provide authentication details for accessing TestRail's API
    client = APIClient('https://snapsheet.testrail.io/')
    client.user = 'ENTER EMAIL HERE'
    client.password = 'ENTER API KEY HERE'

    phase2_run_dict = {}
    phase2_plan_dict = {}
    totals = {'passed': 0,
              'failed': 0,
              'untested': 0,
              'total': 0
              }

    # ProjIDs: Phase 2 = 11; Dispatch = 12

    phase2_run_data = client.send_get('get_runs/11')
    phase2_plan_data = client.send_get('get_plans/11')

    phase2_plan_dict = passFailData(phase2_plan_data, 11, phase2_plan_dict, totals)
    phase2_run_dict = passFailData(phase2_run_data, 11, phase2_run_dict, totals)

    with open('VICE_status_' + now + '.csv', mode='w') as csv_file:
        fieldnames = ['Feature', 'Passed', 'Failed', 'Untested', 'Total', '% Passed', 'Pending Items']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        passFailWriter(phase2_run_dict, writer)
        passFailWriter(phase2_plan_dict, writer)

        writer.writerow({'Feature': 'Total',
                         'Passed': totals['passed'],
                         'Failed': totals['failed'],
                         'Untested': totals['untested'],
                         'Total': totals['total'],
                         '% Passed': round((totals['passed']/totals['total']) * 100),
                         'Pending Items': ''
                         })

    options = {'server': 'https://snapsheettech.atlassian.net/'}
    jira = JIRA(options, basic_auth=('ENTER EMAIL HERE', 'API TOKEN HERE'))

    # favoriteFilters = jira.favourite_filters()

    total = jira.search_issues('filter=10040', maxResults=1000, json_result=True)['total']

    with open('VICE_bugs_' + now + '.csv', mode='w') as csv_file:
        fieldnames = ['Key', 'Summary', 'Severity', 'Component/s']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        block_num = 0
        block_size = 100

        while True:
            start_idx = block_num*block_size
            issues = jira.search_issues('filter=10040', startAt=start_idx, maxResults=block_size)
            if len(issues) == 0:
                break
            block_num += 1
            for issue in issues:

                components = []
                for i in range(len(issue.fields.components)):
                    components.append(issue.fields.components[i].name)

                writer.writerow({'Key': issue.key,
                                 'Summary': issue.fields.summary,
                                 'Severity': issue.fields.customfield_10030.value,
                                 'Component/s': ", ".join(components)
                                 })

    print('\nTotal Unresolved issues: ' + str(total) + '\n')

if __name__ == "__main__":
    main()