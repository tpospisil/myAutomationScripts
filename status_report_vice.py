#! python3/usr/bin/env

import ssl
import csv
import itertools
import datetime
from testrail import *
from pprint import pprint


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
    client.user = 'USERNAME HERE'
    client.password = 'APIKEYHERE'

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

    phase2_plan_dict = passFailData(phase2_plan_data, 10, phase2_plan_dict, totals)
    phase2_run_dict = passFailData(phase2_run_data, 10, phase2_run_dict, totals)

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

if __name__ == "__main__":
    main()