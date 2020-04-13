#! python3/usr/bin/env

import re, csv, requests
import datetime
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import code

def main():

    page_url = input('Please provide the URL for the Confluence requirements page: ')
    page_id = re.search('(\d+)', page_url).group(0)

    api_auth = HTTPBasicAuth('EMAIL', 'ATLASSIAN KEY')
    response = requests.get(
        'https://snapsheettech.atlassian.net/wiki/rest/api/content/%s?expand=body.storage' % page_id,
        auth=api_auth
        )

    page_html = BeautifulSoup(
        response.json()['body']['storage']['value'],
        'html.parser'
        )

    with open('%s_requirements.csv' % (response.json()['title'].replace("/","-")), mode='w') as csv_file:
        fieldnames = ['#', 'Requirement', 'User Story', 'Importance']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        rows = iter(page_html.find('h2', text="Requirements").find_all_next('tr'))
        headers = [col.text for col in next(rows)]
        for row in rows:
            i=0
            values = []
            for col in row:
                content = ""
                if i == 2:
                    for idx, li in enumerate(row.findChildren('li')):
                        content += "- {0}\r\n".format(li.text)
                else:
                    content = col.text
                i+=1
                values.append(content)
            requirement_data = dict(zip(headers, values))
            writer.writerow(
                {'#': requirement_data['#'],
                 'Requirement': requirement_data['Requirement'],
                 'User Story': requirement_data['User Story'],
                 'Importance': requirement_data['Importance']
                 })

    print("Requirements file generated for %s." % (response.json()['title']))

if __name__ == "__main__":
    main()
