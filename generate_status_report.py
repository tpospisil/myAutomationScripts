#! python3/usr/bin/env

import csv, ssl, sys
import datetime
from testrail import *


def removeCompletedRecords(raw_data, data_type):
    dict_index = 0
    records = {}
    for i in range(len(raw_data)):
        if raw_data[i]['is_completed'] == False:
            record_info = {
                'name': '',
                'id': ''
            }
            record_info['name'] = raw_data[i]['name']
            record_info['id'] = raw_data[i]['id']
            records[dict_index] = record_info
            dict_index += 1

    if len(records) == 0:
        print('Could not generate reports. No %s records exist.' % data_type)
        sys.exit(1)
    elif len(records) == 1:
        index = 0
    else:
        for i in range(len(records)):
            print('[%s] %s' % (str(i), records[i]['name']))
        index = int(input('\nEnter the key corresponding to the %s for which you\'d like to generate a report: ' % (data_type)))

    return (records, index)


def passFailWriter(results_data, totals, writer):
    for i in range(len(results_data)):
        passed = results_data[i]['passed_count']
        failed = results_data[i]['failed_count']+results_data[i]['blocked_count']
        untested = results_data[i]['untested_count']+results_data[i]['retest_count']
        total = passed + failed + untested
        totals['passed'] += passed
        totals['failed'] += failed
        totals['untested'] += untested
        totals['total'] += total
        try:
            writer.writerow(
                {'Feature': results_data[i]['name'],
                 'Passed': passed,
                 'Failed': failed,
                 'Untested': untested,
                 'Total': total,
                 '% Passed': round((passed/total) * 100)
                 })
        except ZeroDivisionError:
            writer.writerow(
                {'Feature': results_data[i]['name'],
                 'Passed': passed,
                 'Failed': failed,
                 'Untested': untested,
                 'Total': total,
                 '% Passed': 0
                 })

    return totals


def main():

    now = datetime.datetime.now().strftime('%m%d%y')

    ssl._create_default_https_context = ssl._create_unverified_context

    client = APIClient('https://snapsheet.testrail.io/')
    client.user = 'TESTRAIL EMAIL'
    client.password = 'TESTRAIL API KEY'

    projects, project_index = removeCompletedRecords(client.send_get('get_projects'), 'project')
    milestones, milestone_index = removeCompletedRecords(client.send_get('get_milestones/%s' % (str(projects[project_index]['id']))), 'milestone')

    run_data = client.send_get(
        'get_runs/%s&milestone_id=%s' %
        (str(projects[project_index]['id']),
         str(milestones[milestone_index]['id']))
    )
    plan_data = client.send_get(
        'get_plans/%s&milestone_id=%s' %
        (str(projects[project_index]['id']),
         str(milestones[milestone_index]['id']))
    )

    totals = {'passed': 0,
              'failed': 0,
              'untested': 0,
              'total': 0
              }

    with open('%s_results_%s.csv' % (milestones[milestone_index]['name'], now), mode='w') as csv_file:
        fieldnames = ['Feature', 'Passed', 'Failed', 'Untested', 'Total', '% Passed', 'Pending Items']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        passFailWriter(run_data, totals, writer)
        passFailWriter(plan_data, totals, writer)

        try:
            writer.writerow(
                {'Feature': 'Total',
                 'Passed': totals['passed'],
                 'Failed': totals['failed'],
                 'Untested': totals['untested'],
                 'Total': totals['total'],
                 '% Passed': round((totals['passed'] / totals['total']) * 100),
                 'Pending Items': ''
                 })
        except ZeroDivisionError:
            writer.writerow(
                {'Feature': 'Total',
                 'Passed': totals['passed'],
                 'Failed': totals['failed'],
                 'Untested': totals['untested'],
                 'Total': totals['total'],
                 '% Passed': 0,
                 'Pending Items': ''
                 })

    print('\nReport generated to the \"%s\" milestone.\n' % milestones[milestone_index]['name'])

if __name__ == "__main__":
    main()