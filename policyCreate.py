#! python3/usr/bin/env

import datetime, time, names, random
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def formatDateTime(currentDateTime):
    "Function to prepend a '0' to date/time values which are less than 10"
    if currentDateTime < 10:
        currentDateTime = '0' + str(currentDateTime)
    else:
        currentDateTime = str(currentDateTime)
    return currentDateTime

def main():

    # Grab and format current date/time
    now = datetime.datetime.now()
    month = formatDateTime(now.month)
    day = formatDateTime(now.day)
    hour = formatDateTime(now.hour)
    minute = formatDateTime(now.minute)
    second = formatDateTime(now.second)

    # Create policy info
    policyNumber = 'test' + month + day + hour + minute + second
    firstName = names.get_first_name()
    lastName = names.get_last_name()
    fullName = firstName + ' ' + lastName

    # Launch browser
    browser = webdriver.Chrome()

    # Obtain random VIN
    browser.get('https://www.randomvin.com')
    time.sleep(2)
    randomVIN = browser.find_element_by_xpath('//*[@id="Result"]/h2')
    randomVIN = randomVIN.text

    # Login to Policy Photos portal as adjuster
    browser.get('https://ssm-policy-photos-stage.herokuapp.com/login')
    time.sleep(2)
    loginEmail = browser.find_element_by_id('login-email')
    loginEmail.send_keys('FNAME.LNAME@snapsheet.me')
    loginPwd = browser.find_element_by_id('login-password')
    loginPwd.send_keys('PASSWORD')
    loginButton = browser.find_element_by_id('login-submit')
    loginButton.click()
    time.sleep(1)

    #Create new policy
    newPolicyButton = browser.find_element_by_css_selector('#data-bind-node > div > div:nth-child(1) > div.Lq_E5WAFUEsPt941M8WdU > div:nth-child(1) > nav > div > ul > li._2PR717ayeR1-0Zt_Ew9cY6 > button')
    newPolicyButton.click()
    time.sleep(1)

    #Input Policy Number for new policy
    policyNumberInput = browser.find_element_by_id('modal-input-policy-number')
    policyNumberInput.send_keys(policyNumber)
    policyNumberOk = browser.find_element_by_xpath('//*[@id="new-policy-modal"]/div/div/div[2]/form/div[2]/button[2]')
    policyNumberOk.click()
    time.sleep(2)

    # Populate the Policy Info card
    policyFirstName = browser.find_element_by_id('first-name')
    policyFirstName.send_keys(firstName)
    policyLastName = browser.find_element_by_id('last-name')
    policyLastName.send_keys(lastName)
    policyPhone = browser.find_element_by_id('phone')
    policyPhone.send_keys('111' + str(random.randint(1000000,10000000)))
    policyAddress1 = browser.find_element_by_id('address1')
    policyAddress1.send_keys('2127 N Richmond St')
    policyCity = browser.find_element_by_id('city')
    policyCity.send_keys('Chicago')
    policyState = Select(browser.find_element_by_id('postal-state'))
    policyState.select_by_visible_text('Illinois')
    policyZip = browser.find_element_by_id('zip-code')
    policyZip.send_keys('60647')

    # Populate the Vehicles card
    policyVIN = browser.find_element_by_id('vehicles[0]-vin')
    policyVIN.send_keys(randomVIN)
    time.sleep(1)
    policyLicensePlate = browser.find_element_by_id('vehicles[0]-plate')
    policyLicensePlate.send_keys('IL' + minute + second)
    licensePlateState = Select(browser.find_element_by_id('vehicles[0]-plate-state'))
    licensePlateState.select_by_visible_text('Illinois')
    time.sleep(1)
    savePolicyRequest = browser.find_element_by_xpath('//*[@id="data-bind-node"]/div/div[1]/div[2]/form/div[2]/div[2]/button')
    savePolicyRequest.click()

    time.sleep(4)
    print('Policy #: ' + policyNumber)
    print('Zip Code: 60647')
    browser.quit()

if __name__ == "__main__":
    main()