#! python3/usr/bin/env

import ssl
import csv
from datetime import datetime
from testrail import *
# from pprint import pprint

def to_datetime(d):
    day, month, year = map(int, d.split('-'))
    return datetime(year, day, month, 0, 0, 0)

def main():

    # Define reporting date range
    print('Please input dates in MM-DD-YYYY format.')
    start = input('\nInput reporting range start date: ')
    end = input('\nInput reporting range end date: ')
    _start = to_datetime(start)
    _end = to_datetime(end)

    # Initialize variables and plan dictionaries
    Jun = Austin = Tyler = unassigned = totals = 0
    plan_dict = {}
    run_fails = {} # This will hold the number of failed runs per plan
    run_totals = {} # This will hold the run totals per assignee for each plan
    defect_totals = {} # This will hold the defects per plan

    ssl._create_default_https_context = ssl._create_unverified_context

    # Provide authentication details for accessing TestRail's API
    client = APIClient('https://snapsheet.testrail.io/')
    client.user = 'tyler.pospisil@snapsheet.me'
    client.password = 'befIH0/waijFmVE9PSmq-J/1mKJVEwzJTSmXHaufw'

    # Request will return plan data for regression runs project
    plans = client.send_get('get_plans/10')

    for i in range(len(plans)):
        plan_dict[plans[i]['id']] = plans[i]['name'] # Dictionary over which we will iterate
        run_totals[plans[i]['name']] = 0 # Dictionary to hold run totals per assignee for each plan/product
        run_fails[plans[i]['name']] = 0 # Dictionary to hold the number of failed runs per each plan/product
        defect_totals[plans[i]['name']] = 0 # Dictionary to hold the number of defects per each plan/product

    # Begin pulling data and building csv output
    with open('run_data_master_' + start + '_' + end + '.csv', mode='w') as csv_file:
        fieldnames = ['Build Name', 'Create Date', 'Tester', '# Passed', '# Failed', 'Defects']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Loop iterates through each key:value pair in the plan_dict dictionary
        for k, v in plan_dict.items():

            plan_data = client.send_get('get_plan/' + str(k))

            user_run_totals = {'Jun Yang': 0,
                               'Austin Curry': 0,
                               'Tyler Pospisil': 0,
                               'Unassigned': 0
                               }

            # Initialize lists for given plan entry
            assignedTo = []
            buildName = []
            createDate = []
            defects = []
            failed = []
            passed = []
            run_ids = []

            for i in range(len(plan_data['entries'])):
                for j in range(len(plan_data['entries'][i]['runs'])):
                    buildName.append(plan_data['entries'][i]['runs'][j]['config'])
                    createDate.append(datetime.utcfromtimestamp(int(plan_data['entries'][i]['runs'][j]['created_on'])).strftime(
                        '%m-%d-%Y'))  # Decodes UNIX timestamp and appends in human-readable format
                    failed.append(plan_data['entries'][i]['runs'][j]['failed_count'])
                    passed.append(plan_data['entries'][i]['runs'][j]['passed_count'])
                    run_ids.append(plan_data['entries'][i]['runs'][j]['id'])

            # Trim entries which do not fall within specified reporting range
            for i in range(len(createDate) - 1, -1, -1):
                if (to_datetime(createDate[i]) <= _start) or (to_datetime(createDate[i]) >= _end):
                    del buildName[i], createDate[i], failed[i], passed[i], run_ids[i]

            # Translate trimmed list's assignee IDs to names
            for i in range(len(buildName)):
                if failed[i] != 0:
                    run_fails[v] += 1
                run_data = client.send_get('get_tests/' + str(run_ids[i]))
                tests = []
                run_defects = []
                run_tester = []
                for j in range(len(run_data)):
                    tests.append(run_data[j]['id'])
                for t in range(len(tests)):
                    test_data = client.send_get('get_results/' + str(tests[t]))
                    if len(test_data) > 0:
                        test_defects = test_data[0]['defects']
                        test_runner = test_data[0]['created_by']
                        run_tester.append(test_runner)
                    else:
                        run_tester.append(0)
                        continue
                    if test_defects == None:
                        continue
                    run_defects.append(test_defects)


                defects.append(run_defects)
                assignedTo.append(run_tester[0])
                if len(defects[i]) > 0:
                    defect_totals[v] += (",".join(defects[i]).count(",") + 1)
                else:
                    defect_totals[v] += len(defects[i])

                # Translate assignee IDs to names
                if assignedTo[i] == 1:
                    assignedTo[i] = 'Jun Yang'
                    user_run_totals['Jun Yang'] += 1
                elif assignedTo[i] == 3:
                    assignedTo[i] = 'Austin Curry'
                    user_run_totals['Austin Curry'] += 1
                elif assignedTo[i] == 4:
                    assignedTo[i] = 'Tyler Pospisil'
                    user_run_totals['Tyler Pospisil'] += 1
                else:
                    assignedTo[i] = 'Unassigned'
                    user_run_totals['Unassigned'] += 1


            # Map user_run_totals for given plan/product
            run_totals[v] = user_run_totals

            writer.writerow({'Build Name': v + ' (' + str(len(buildName)) + ')',
                             'Create Date': '---',
                             '# Passed': '---',
                             '# Failed': '---',
                             'Defects': '---',
                             'Tester': '---'
                             })

            for i in range(0, len(buildName)):
                writer.writerow({'Build Name': buildName[i],
                                 'Create Date': createDate[i],
                                 '# Passed': passed[i],
                                 '# Failed': failed[i],
                                 'Defects': ', '.join(defects[i]),
                                 'Tester': assignedTo[i]
                                 })

            writer.writerow({'Build Name': 'TOTALS',
                             'Create Date': '---',
                             '# Passed': sum(passed),
                             '# Failed': sum(failed),
                             'Defects': '---',
                             'Tester': '---'
                             })

    # Write csv containing run totals by assignee by project
    with open('run_data_totals_' + start + '_' + end + '.csv', mode='w') as csv_file:
        fieldnames = ['App', 'Jun Yang', 'Austin Curry', 'Tyler Pospisil', 'Unassigned', 'Total Runs', 'Runs Passed', 'Runs Failed', 'Defects Found']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for (k, v), (k2, v2), (k3,v3) in zip(run_totals.items(), run_fails.items(), defect_totals.items()):
            Jun += int(v['Jun Yang'])
            Austin += int(v['Austin Curry'])
            Tyler += int(v['Tyler Pospisil'])
            unassigned += int(v['Unassigned'])
            totals = Jun + Austin + Tyler + unassigned
            writer.writerow({
                'App': k,
                'Jun Yang': v['Jun Yang'],
                'Austin Curry': v['Austin Curry'],
                'Tyler Pospisil': v['Tyler Pospisil'],
                'Unassigned': v['Unassigned'],
                'Total Runs': v['Jun Yang'] + v['Austin Curry'] + v['Tyler Pospisil'] + v['Unassigned'],
                'Runs Passed': v['Jun Yang'] + v['Austin Curry'] + v['Tyler Pospisil'] + v['Unassigned'] - run_fails[k2],
                'Runs Failed': run_fails[k2],
                'Defects Found': defect_totals[k3]
            })

        writer.writerow({'App': 'TOTALS',
                         'Jun Yang': Jun,
                         'Austin Curry': Austin,
                         'Tyler Pospisil': Tyler,
                         'Unassigned': unassigned,
                         'Total Runs': totals,
                         'Runs Passed': totals - sum(run_fails.values()),
                         'Runs Failed': sum(run_fails.values()),
                         'Defects Found': sum(defect_totals.values())
                         })

if __name__ == "__main__":
    main()