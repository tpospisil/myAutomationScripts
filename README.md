# myAutomationScripts
Fun scripts to automate boring manual tasks :+1:


## batchCreateDeliveredEstimate.py
This script will automatically create a batch of assignments, which in turn are pushed all the way through the claim creation and estimate delivery workflow. The script will prompt the user in `terminal` to enter the number of estimates they would like to deliver. There is a small amount of setup work required for each user:

**Pre-requisite non-standard python libraries:**
- selenium (via pip install)
- ChromeDriver
  - https://pypi.org/project/chromedriver_installer/
- names (via pip install)
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
- selenium (via pip install)
- names (via pip install)
  - Generates random name for each assignment
- Firefox browser should be installed on the computer. Also requires 
  
**Changes required in the script:**
- Comment out all QA servers other than the one of interest (two locations--*before* and *within* the `for` loop)
- Alter the string sent to `loginEmail` to match intended user's username for the target server
- Alter the string sent to `loginPwd` to match intended user's password for the target server
- Default carrier is `Philadelphia Insurance`. To use another provider, simply alter the string sent to `selectProvider` to match the text displayed for the provider of interest in the Carrier dropdown.

## deliverEstimate.py
This script will automatically push a claim through the estimate delivery workflow. The script takes one command line argument in the form of the URL to the **claim** in **CORE**. The script will throw an exception if the wrong URL has been included, or if the URL is not properly formatted. There is a small amount of setup work required for each user:

**Pre-requisite non-standard python libraries:**
- selenium (via pip install)
- ChromeDriver
  - https://pypi.org/project/chromedriver_installer/
- validators (via pip install)
  - Used to check for proper URL formatting
  
**Changes required in the script:**
- Comment out all QA servers other than the one of interest (two locations--*before* and *within* the `for` loop)
- Alter the string sent to `loginEmail` to match intended user's username for the target server
- Alter the string sent to `loginPwd` to match intended user's password for the target server
- Alter the string sent to `chooseFile` to match the file path of the estimate to be uploaded

**Limitations:**
- The script is not currently set up to handle claims which have been marked as `ptl == true`
