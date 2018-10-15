#! python3/usr/bin/env

import sys, validators, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def main():

    # Check to see if user included cmd line argument
    if len(sys.argv) <= 1:
        raise Exception('\nYou forgot to include a command line argument, fool.\n')

    # Verify that user included a valid URL
    if validators.url(sys.argv[1]) != True:
        raise Exception('\nCommand line argument contains an invalid URL.\n')

    # Verify that user included a URL for a CLAIM from CORE
    if 'admin/claim' not in sys.argv[1]:
        raise Exception('\nPlease include the Claim object\'s URL from CORE.\n')

    # Start Chrome using webdriver
    browser = webdriver.Chrome()

    # Navigate to the appropriate QA server
    browser.get('http://snapsheet-stage.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa1.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa2.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa3.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa4.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa5.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa6.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa7.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa8.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa9.herokuapp.com/admin/assignments')
    #browser.get('http://snapsheet-qa10.herokuapp.com/admin/assignments')

    # login to QA server
    loginEmail = browser.find_element_by_css_selector('#admin_user_email')
    loginEmail.send_keys('FNAME.LNAME@snapsheet.me')
    loginPwd = browser.find_element_by_css_selector('#admin_user_password')
    loginPwd.send_keys('PASSWORD')
    loginButton = browser.find_element_by_css_selector('#admin_user_submit_action > input:nth-child(1)')
    loginButton.click()

    # Update the claim to assign an Estimator
    browser.get(sys.argv[1])
    editClaimButton = browser.find_element_by_css_selector('#titlebar_right > div > span:nth-child(1) > a')
    editClaimButton.click()
    selectEstimator = Select(browser.find_element_by_id('claim_estimator_id'))
    selectEstimator.select_by_visible_text('Tyler Pospisil')
    selectDifficulty = Select(browser.find_element_by_id('claim_estimate_difficulty'))
    selectDifficulty.select_by_visible_text('3')
    updateClaim = browser.find_element_by_css_selector('#claim_submit_action > input')
    updateClaim.click()

    # Enter values in the TL Calculator
    tlCalc = browser.find_element_by_css_selector('#action_items_sidebar_section > div > ul:nth-child(4) > li:nth-child(2) > a')
    tlCalc.click()
    estimate = browser.find_element_by_css_selector('body > div:nth-child(2) > div > div.ss-modal._3u47kAiKnAh22wv4gXcJ3Q > div.ss-modal__content.F9i9J7Q5cYDYgqOwwnWay > div > span:nth-child(2) > div.Rb0AZgudLayuw-gWl8sbx > fieldset > div:nth-child(1) > input')
    estimate.send_keys('111')
    laborHours = browser.find_element_by_css_selector('body > div:nth-child(2) > div > div.ss-modal._3u47kAiKnAh22wv4gXcJ3Q > div.ss-modal__content.F9i9J7Q5cYDYgqOwwnWay > div > span:nth-child(2) > div.Rb0AZgudLayuw-gWl8sbx > fieldset > div:nth-child(2) > input')
    laborHours.send_keys('1')
    actualCashValue = browser.find_element_by_css_selector('body > div:nth-child(2) > div > div.ss-modal._3u47kAiKnAh22wv4gXcJ3Q > div.ss-modal__content.F9i9J7Q5cYDYgqOwwnWay > div > span:nth-child(2) > div.Rb0AZgudLayuw-gWl8sbx > fieldset > div:nth-child(3) > input')
    actualCashValue.send_keys('1111')
    calculate = browser.find_element_by_css_selector('body > div:nth-child(2) > div > div.ss-modal._3u47kAiKnAh22wv4gXcJ3Q > div.ss-modal__content.F9i9J7Q5cYDYgqOwwnWay > div > span:nth-child(2) > div._2I5ln0cxMWegRK7PjN635M > div > button._1ddaHvgRumc0fwrsJkuMz1')
    calculate.click()
    time.sleep(1)
    saveTL = browser.find_element_by_css_selector('body > div:nth-child(2) > div > div.ss-modal._3u47kAiKnAh22wv4gXcJ3Q > div.ss-modal__content.F9i9J7Q5cYDYgqOwwnWay > div > div.MiQhWZQWIPXENeDbL0TQ1 > button')
    saveTL.click()
    time.sleep(2)

    # Select 'Start Estimate', then select 'Upload Estimate'
    startEst = browser.find_element_by_css_selector('#start_estimate_button')
    startEst.click()
    time.sleep(1)
    uploadEst = browser.find_element_by_css_selector('#action_items_sidebar_section > div > ul:nth-child(2) > li:nth-child(2) > a')
    uploadEst.click()

    # Attach PDF
    readyToSend = browser.find_element_by_css_selector('#estimate_disposition_ready_to_send')
    readyToSend.click()
    chooseFile = browser.find_element_by_css_selector('#estimate_pdf_doc')
    chooseFile.send_keys('/Users/username/Downloads/Prelim Estimate1.pdf') # Modify file path to point to estimate you would like to upload
    time.sleep(1)
    checkHeader = browser.find_element_by_css_selector('#pdf-compliance-checker-modal-content > div > div.modal-header')
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(checkHeader, -5, 5)
    action.click()
    action.perform()
    time.sleep(1)
    createEst = browser.find_element_by_xpath('//*[@id="estimate_submit_action"]/input')
    createEst.click()
    time.sleep(1)

    # Send the estimate
    sendEst = browser.find_element_by_css_selector('#action_items_sidebar_section > div > ul:nth-child(2) > li:nth-child(2) > a')
    sendEst.click()

    # Exit the browser
    browser.quit()
    print('\nAll done! Estimate delivered :)\n')

if __name__ == "__main__":
    main()