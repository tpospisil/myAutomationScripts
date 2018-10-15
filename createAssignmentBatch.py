#! python3/usr/bin/env

def main():

    import datetime, time, names, random, sys
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select

    userInput = input('\nHow many assignments would you like to create?\n')

    try:
        numberOfAssignments = int(userInput)
    except:
        print('That\'s not a number...')
        sys.exit(1)

    # Launch Firefox browser
    browser = webdriver.Firefox()

    # Navigate to the appropriate QA server ***NOTE: Don't forget to select the same server within the "for" loop below***
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
    loginEmail.send_keys('fname.lname@snapsheet.me') # Modify to send user name
    loginPwd = browser.find_element_by_css_selector('#admin_user_password')
    loginPwd.send_keys('PASSWORD') # Modify to send PASSWORD
    loginButton = browser.find_element_by_css_selector('#admin_user_submit_action > input:nth-child(1)')
    loginButton.click()

    for i in range(0,numberOfAssignments): # Define the number of assignments you would like to create

        # Grab current date/time
        now = datetime.datetime.now()

        # Append '0' if month, day, hour, or minute is less than 10
        if now.month < 10:
            month = '0' + str(now.month)
        else:
            month = str(now.month)
        if now.day < 10:
            day = '0' + str(now.day)
        else:
            day = str(now.day)
        if now.hour < 10:
            hour = '0' + str(now.hour)
        else:
            hour = str(now.hour)
        if now.minute < 10:
            minute = '0' + str(now.minute)
        else:
            minute = str(now.minute)
        if now.second < 10:
            second = '0' + str(now.second)
        else:
            second = str(now.second)

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

    browser.quit()

if __name__ == "__main__":
    main()