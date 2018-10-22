#! python3/usr/bin/env

def formatDateTime(currentDateTime):
    "Function to prepend a '0' to date/time values which are less than 10"
    if currentDateTime < 10:
        currentDateTime = '0' + str(currentDateTime)
    else:
        currentDateTime = str(currentDateTime)
    return currentDateTime

def main():

    import datetime, time, names, random, sys
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select

    userInput = input('\nHow many estimates would you like to deliver?\n')

    try:
        numberOfAssignments = int(userInput)
    except:
        print('That\'s not a number...')
        sys.exit(1)

    # Launch Firefox browser
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

    for i in range(0, numberOfAssignments):

        # Grab current date/time
        now = datetime.datetime.now()

        # Append '0' if month, day, hour, or minute is less than 10
        month = formatDateTime(now.month)
        day = formatDateTime(now.day)
        hour = formatDateTime(now.hour)
        minute = formatDateTime(now.minute)
        second = formatDateTime(now.second)

        # Create claim number (with date/time stamp) and random owner name
        claimNo = 'test' + month + day + hour + minute + second
        firstName = names.get_first_name()
        lastName = names.get_last_name()

        # Grab a random VIN from randomvin.com
        browser.get('https://www.randomvin.com')
        time.sleep(2)
        randomVIN = browser.find_element_by_css_selector('#Result > h2:nth-child(1)')
        randomVIN = randomVIN.text

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

        # Navigate to Assignment page and begin creating a new assignment
        assignmentPage = browser.find_element_by_css_selector('#assignments > a:nth-child(1)')
        assignmentPage.click()
        newAssignElem = browser.find_element_by_css_selector('span.action_item:nth-child(1) > a:nth-child(1)')
        newAssignElem.click()

        # Now populate the New Assignment page...

        # Populate the 'Claim Details' section
        selectProvider = Select(browser.find_element_by_id('assignment_provider_id')) #create instance of Select class to grab provider dropdown
        #selectProvider.select_by_visible_text('USAA') # Use select method to select USAA from dropdown
        selectProvider.select_by_visible_text('Philadelphia Insurance') # ***Use this for STAGE***
        estimatingSystem = Select(browser.find_element_by_id('assignment_estimating_system_id'))
        #estimatingSystem.select_by_visible_text('Ccc Staff')
        estimatingSystem.select_by_visible_text('Ccc Appraiser')
        claimParty = Select(browser.find_element_by_id('assignment_claim_type'))
        claimParty.select_by_visible_text('IV')
        processType = Select(browser.find_element_by_id('assignment_category_id'))
        processType.select_by_visible_text('Standard')
        claimNumber = browser.find_element_by_css_selector('#assignment_claim_number')
        claimNumber.send_keys(claimNo)
        fullClaimNumber = browser.find_element_by_css_selector('#assignment_full_claim_number')
        fullClaimNumber.send_keys(claimNo)
        lossDate = browser.find_element_by_css_selector('#assignment_loss_date')
        lossDate.send_keys()

        # Populate the 'Vehicle Details' section
        vin = browser.find_element_by_css_selector('#assignment_vin')
        vin.send_keys(randomVIN)

        # Populate the 'Owner Details' section
        ownerName = browser.find_element_by_css_selector('#assignment_owner_name')
        ownerName.send_keys(firstName + ' ' + lastName)
        altPhone = browser.find_element_by_css_selector('#assignment_preferred_phone_number')
        altPhone.send_keys('111' + str(random.randint(1000000, 10000000)))
        email = browser.find_element_by_css_selector('#assignment_email')
        email.send_keys(firstName.lower() + '.' + lastName.lower() + '@hotmail.com')
        address = browser.find_element_by_css_selector('#assignment_address1')
        address.send_keys('123 Fake St')
        zipCode = browser.find_element_by_css_selector('#assignment_zip_code')
        zipCode.send_keys('60647')
        time.sleep(0.5)

        # Populate the 'Estimating Location of Record' section
        copyAddress = browser.find_element_by_css_selector('#addr_copy')
        locationType = Select(browser.find_element_by_id('assignment_location_type'))
        time.sleep(1)
        locationType.select_by_visible_text('Home')
        copyAddress.click()

        # Click 'Create Assignment' and we're golden
        createAssignment = browser.find_element_by_css_selector('.actions > ol:nth-child(1) > li:nth-child(1) > input:nth-child(1)')
        createAssignment.click()

        # Now create a claim

        createClaim = browser.find_element_by_css_selector('.fancy_button')
        createClaim.click()

        creationReason = Select(browser.find_element_by_id('claim_manual_creation_reason'))
        time.sleep(0.5)
        creationReason.select_by_visible_text('Email')
        creationComments = browser.find_element_by_css_selector('#claim_manual_creation_comments')
        creationComments.send_keys('Test')
        claimPIN = browser.find_element_by_css_selector('#claim_user_attributes_password')
        claimPIN.send_keys('1234')
        claimButton = browser.find_element_by_css_selector('.single_click_only_button')
        claimButton.click()

        # Assign an estimator

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
        time.sleep(1)

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
        chooseFile.send_keys('/Users/USERNAME/Downloads/Prelim Estimate1.pdf')  # Will need to at least update username for other users
        time.sleep(2)
        checkHeader = browser.find_element_by_css_selector('#pdf-compliance-checker-modal-content > div > div.modal-header')
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(checkHeader, -5, 5)
        action.click()
        action.perform()
        time.sleep(1.5)
        createEst = browser.find_element_by_xpath('//*[@id="estimate_submit_action"]/input')
        createEst.click()
        time.sleep(1)

        # Send the estimate
        sendEst = browser.find_element_by_css_selector('#action_items_sidebar_section > div > ul:nth-child(2) > li:nth-child(2) > a')
        sendEst.click()

    browser.quit()

    print('\nYour %d estimates have been delivered :)\n' % numberOfAssignments)

if __name__ == "__main__":
    main()