# myAutomationScripts
Fun scripts to automate boring manual tasks :+1:

All scripts require Python 3.X


## status_report_vice.py
This script will generate three CSV files--one for the test pass/fail status for a given Milestone in a TestRail project and another two for the list of outstanding issues contained in given filter(s). Output files can be found in the current directory.

**Pre-requisites**
- testrail.py (http://docs.gurock.com/testrail-api2/bindings-python)
- TestRail API key (http://docs.gurock.com/testrail-api2/accessing)
- jira-python (https://jira.readthedocs.io/en/master/index.html)
- Jira API token (https://confluence.atlassian.com/cloud/api-tokens-938839638.html)

**Changes required in the script:**
- User will need to input their own Jira and TestRail username/email, as well as their respective API keys.

## configCreate.py
This script creates a new configuration and test run in TestRail for QA's regression testing. The script will output the test run URL in the console.

**Pre-requisites**
- testrail.py (http://docs.gurock.com/testrail-api2/bindings-python)
- TestRail API key (http://docs.gurock.com/testrail-api2/accessing)

**Changes required in the script:**
- User will need to input their own TestRail username/email, as well as their API key.

## batchCreateDeliveredEstimate.py
This script will automatically create a batch of assignments, which in turn are pushed all the way through the claim creation and estimate delivery workflow. The script will prompt the user in `terminal` to enter the number of estimates they would like to deliver. There is a small amount of setup work required for each user:

**Pre-requisite non-standard python libraries:**
- selenium (via `pip install`)
- ChromeDriver
  - https://pypi.org/project/chromedriver_installer/
- names (via `pip install`)
  - Generates random name for each assignment
  
**Changes required in the script:**
- Comment out all QA servers other than the one of interest (two locations--*before* and *within* the `for` loop)
- Alter the string sent to `loginEmail` to match intended user's username for the target server
- Alter the string sent to `loginPwd` to match intended user's password for the target server
- Alter the string sent to `chooseFile` to match the file path of the estimate to be uploaded
- Default carrier is `USAA`. To use another provider, simply alter the string sent to `selectProvider` to match the text displayed for the provider of interest in the Carrier dropdown.

## createAssignmentBatch.py
This script will automatically create a batch of assignments. The script will prompt the user in `terminal` to enter the number of assignments they would like to create. There is a small amount of setup work required for each user:

**Pre-requisite non-standard python libraries:**
- selenium (via `pip install`)
- names (via `pip install`)
  - Generates random name for each assignment
- Firefox browser should be installed on the machine
  - https://github.com/mozilla/geckodriver/releases
  
**Changes required in the script:**
- Comment out all QA servers other than the one of interest (two locations--*before* and *within* the `for` loop)
- Alter the string sent to `loginEmail` to match intended user's username for the target server
- Alter the string sent to `loginPwd` to match intended user's password for the target server
- Default carrier is `Philadelphia Insurance`. To use another provider, simply alter the string sent to `selectProvider` to match the text displayed for the provider of interest in the Carrier dropdown.

## deliverEstimate.py
This script will automatically push a claim through the estimate delivery workflow. The script takes one command line argument in the form of the URL to the **claim** in **CORE**. The script will throw an exception if the wrong URL has been included, or if the URL is not properly formatted. There is a small amount of setup work required for each user:

**Pre-requisite non-standard python libraries:**
- selenium (via `pip install`)
- ChromeDriver
  - https://pypi.org/project/chromedriver_installer/
- validators (via `pip install`)
  - Used to check for proper URL formatting
  
**Changes required in the script:**
- Comment out all QA servers other than the one of interest (two locations--*before* and *within* the `for` loop)
- Alter the string sent to `loginEmail` to match intended user's username for the target server
- Alter the string sent to `loginPwd` to match intended user's password for the target server
- Alter the string sent to `chooseFile` to match the file path of the estimate to be uploaded

**Limitations:**
- The script is not currently set up to handle claims which have been marked as `ptl == true`

## policyCreate.py
This script will automatically create a new Policy Request (single vehicle) on the Policy portal. There is a small amount of setup work required for each user:

**Pre-requisite non-standard python libraries:**
- selenium (via `pip install`)
- ChromeDriver
  - https://pypi.org/project/chromedriver_installer/
- names (via `pip install`)
  - Generates random name for each policy
  
**Changes required in the script:**
- Alter the string sent to `loginEmail` to match intended user's username for the target server
- Alter the string sent to `loginPwd` to match intended user's password for the target server

## exposureCreate.py (DEPRECATED)
Creates an claim and adds a single exposure in the `vice-frontend-integration` environment.

**Changes required in the script:**
- User will need to input their own email, password, and phone number

## addExposureToClaim.py (DEPRECATED)
Adds an exposure to an existing claim in the `vice-frontend-integration` environment. The script takes one command line argument in the form of the URL to an existing claim's exposure list view page. The script will throw an exception if the wrong URL has been included, or if the URL is not properly formatted.

**Changes required in the script:**
- User will need to input their own email, password, and phone number

## viceRegression.py (DEPRECATED)
This script will run a quick sanity check of base functionality of the `vice-frontend-integration` environment. Certain exceptions will capture and output a screenshot into the current directory.

**Changes required in the script:**
- User will need to input their own email, password, and phone number.
