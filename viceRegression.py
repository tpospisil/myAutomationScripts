#! python3/usr/bin/env

import unittest, time, datetime, names, sys, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


def formatDateTime(currentDateTime):
    if currentDateTime < 10:
        currentDateTime = '0' + str(currentDateTime)
    else:
        currentDateTime = str(currentDateTime)
    return currentDateTime

now = datetime.datetime.now()

# Append '0' if month, day, hour, or minute is less than 10
month = formatDateTime(now.month)
day = formatDateTime(now.day)
hour = formatDateTime(now.hour)
minute = formatDateTime(now.minute)
second = formatDateTime(now.second)

email = 'INSERTEMAILHERE'

claimNo = 'claim' + month + day + hour + minute + second
policyNo = 'policy' + month + day + hour + minute + second

firstName = names.get_first_name()
lastName = names.get_last_name()
currentAddress = '62 O\'Connell Street Upper'
currentCity = 'Dublin'
currentCounty = '4'
cars = {'Toyota':['Camry','Corolla','Prius'], 'Honda':['Accord','Civic','CR-V'], 'Ford':['F-150','Escape','Focus']}
make, models = random.choice(list(cars.items()))
model = random.choice(models)

class ViceRegressionSuite(unittest.TestCase):
    currentShopName = ''
    currentPinnedLocation = ''

    @classmethod
    def setUpClass(inst):
        inst.driver2 = webdriver.Chrome()
        inst.driver = webdriver.Chrome()
        inst.driver.implicitly_wait(30)
        inst.driver.get("https://vice-frontend-integration.snapsheet.tech/")

    def test_1viceLogin(self):
        self.assertEqual(False, self.driver.find_element_by_css_selector(
            '#app > div > div > div._1lWQjoWRvEuXiIoWRyOPYh > div > div:nth-child(6) > button').is_enabled())
        self.driver.find_element_by_css_selector(
            '[data-test-id="login_form_email_input"]').send_keys(
            email)
        self.driver.find_element_by_css_selector(
            '[data-test-id="login_form_password_input').send_keys(
            "INSERTPASSWORDHERE")
        self.driver.find_element_by_css_selector(
            '#app > div > div > div._1lWQjoWRvEuXiIoWRyOPYh > div > div:nth-child(6) > button').click()
        time.sleep(2)

    def test_2createClaim(self):
        # Select the 'Create Claim' button
        self.driver.find_element_by_css_selector(
            '#app > div > div > div._1YlF0xeG8atxX5hpNMebqS > div > div > button > span').click()
        time.sleep(1)

        # Verify that 'Create Claim' button is inactive without fields pre-populated
        self.assertEqual(False, self.driver.find_element_by_css_selector(
            '[data-test-id="new-short-claim-submit-button"]').is_enabled())

        # Populate Claim Number and Policy Number fields
        self.driver.find_element_by_css_selector(
            '#app > div > div > div._1YlF0xeG8atxX5hpNMebqS > div > label:nth-child(3) > input').send_keys(
            policyNo)
        self.driver.find_element_by_css_selector(
            '#app > div > div > div._1YlF0xeG8atxX5hpNMebqS > div > label:nth-child(4) > input').send_keys(
            claimNo)

        # Create Claim
        self.driver.find_element_by_css_selector(
            '[data-test-id="new-short-claim-submit-button"]').click()

    def test_3createExposure(self):
        # Select the 'New Exposure' button from the Exposure detail view screen
        self.driver.find_element_by_css_selector(
            '[data-test-id="exposure-list-view-new-button"]').click()
        time.sleep(2)

        # Verify that 'Save' is unavailable without fields populated
        self.assertEqual(False, self.driver.find_element_by_css_selector(
            '[data-test-id="exposure-new-view-save-button"]').is_enabled())

        # Verify that current handler is auto-populated
        handler = Select(self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div/div/div/div/div/select'))
        self.assertEqual('Tyler Tester', handler.first_selected_option.text)

        # Populate the available fields for the new exposure
        insuredOnPolicyCheck = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div/label/div')
        insuredOnPolicyCheck.click()
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.firstName"]/following-sibling::input[1]').send_keys(
            firstName)
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.surname"]/following-sibling::input[1]').send_keys(
            lastName)
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.address.address1"]/following-sibling::input[1]').send_keys(
            currentAddress)
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.address.city"]/following-sibling::input[1]').send_keys(
            currentCity)
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.address.region"]/following-sibling::input[1]').send_keys(
            currentCounty)
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.preferredContact"]/following-sibling::div[1]/label[1]/div/span').click()
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.email"]/following-sibling::input[1]').send_keys(
            email)
        self.driver.find_element_by_xpath(
            '//label[@for="claimant.phone"]/following-sibling::input[1]').send_keys(
            '3195412283')
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.registrationNumber"]/following-sibling::input[1]').send_keys(
            '182-D-12345')
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.vin"]/following-sibling::input[1]').send_keys(
            '19XFC2F54JE004299')
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.make"]/following-sibling::input[1]').send_keys(
            make)
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.model"]/following-sibling::input[1]').send_keys(
            model)
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.year"]/following-sibling::input[1]').send_keys(
            '2018')
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.address.address1"]/following-sibling::input[1]').send_keys(
            currentAddress)
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.address.city"]/following-sibling::input[1]').send_keys(
            currentCity)
        self.driver.find_element_by_xpath(
            '//label[@for="vehicle.address.region"]/following-sibling::input[1]').send_keys(
            currentCounty)

        #Verify that 'Save' button is now available with required fields populated
        self.assertEqual(True, self.driver.find_element_by_css_selector(
            '[data-test-id="exposure-new-view-save-button"]').is_enabled())
        self.driver.find_element_by_css_selector(
            '[data-test-id="exposure-new-view-save-button"]').click()
        time.sleep(2)

        # Navigate to the Exposures list view
        self.driver.find_element_by_css_selector(
            '[data-icon="arrow-circle-left"]').click()

        # Verify that the created exposure is listed
        self.assertEqual(firstName + ' ' + lastName, self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]').text)
        self.assertEqual(make + ' ' + model + ' 2018', self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]').text)
        time.sleep(3)

        # Select the newly-created exposure from the list view
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]').click()

        # Verify that the correct preferred contact information is published in the exposure header
        preferredContactHeader = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[3]/div').text
        self.assertEqual(email, preferredContactHeader[19:])

    def test_4assignShopSendLink(self):
        # Verify that no shop has been assigned
        self.assertEqual('No shop selected', self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]').text)

        # Select the 'Shop Locator' button
        self.driver.find_element_by_css_selector(
            '[data-test-id="shop-locator-card-button"]').click()
        time.sleep(3)

        # Verify that correct vehicle address and vehicle info is listed
        self.assertEqual(make + ' ' + model + ' 2018\n' + currentAddress + '\n' + currentCity + currentCounty, self.driver.find_element_by_css_selector(
            '[data-test-id="location-item-wrapper"]').text)
        initialLocations = self.driver.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')
        initialResults = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]').text
        self.assertEqual(initialResults[0], str(len(initialLocations) - 1))

        # Verify that both delivery options are available and that the send button in the bottom bar reads 'Send All' without a shop selected
        self.assertTrue(self.is_element_present(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/label[1]/div'))
        self.assertTrue(self.is_element_present(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/label[2]/div'))
        self.assertEqual('Send All', self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[2]/div/button').text)

        # Verify that shops list updates when user searches new address
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/input').send_keys(
            'cork', Keys.ENTER)
        time.sleep(2)
        searchLocations = self.driver.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')
        searchResults = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]').text
        self.assertEqual(False, initialResults == searchResults)
        self.assertTrue(searchResults, str(len(searchLocations) - 1))

        # Remove search address and verify that original results are displayed
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div/span').click()
        self.assertEqual(initialResults, self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]').text)
        time.sleep(1)

        # Select an available shop
        selectedShop = self.driver.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[1].text
        self.driver.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[1].click()
        time.sleep(2)

        # Verify that shop is pinned to top of results
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, '[data-test-id="location-item-unselect"]'))
        pinnedShopLocation = self.driver.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[1].text
        self.assertEqual(selectedShop, pinnedShopLocation[:-9])
        self.__class__.currentPinnedLocation = pinnedShopLocation

        # With email option selected, select 'Assign Shop'
        self.assertEqual('Assign Shop', self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[2]/div/button/span').text)
        self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div[2]/div/button/span').click()
        time.sleep(1)

        # Verify that correct info is listed in the modal. Then close the confirmation modal
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, '[data-icon="check-circle"]'))
        self.assertEqual('Success!', self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/h3/span').text)
        modalShopName = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div/p[2]').text
        self.assertEqual(modalShopName, selectedShop[:len(modalShopName)])
        self.driver.find_element_by_css_selector(
            '[data-test-id="locator-modal-close-button"]').click()

        # Verify that the correct shop is listed in exposure detail view
        shopCardName = self.driver.find_element_by_css_selector(
            '[data-test-id="shop-locator-card-details"] > div > span._13AJpbnc8oWgP-TGazCoK6').text
        self.assertEqual(shopCardName, selectedShop[:len(shopCardName)])
        self.__class__.currentShopName = shopCardName

    def test_5customer_NewShopOfChoice(self):
        # Select customer shop locator link from history
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[1]/div[4]/button[2]/span').click()
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div').click()
        time.sleep(1)
        customerLink = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div[1]/p[3]/a').text

        # Navigate to customer link URL in a new browser session
        self.driver2.get(customerLink)
        time.sleep(2)

        # Verify that current assigned shop's name is displayed on splash screen, then close splash screen
        self.assertEqual(self.__class__.currentShopName, self.driver2.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div[2]').text)
        self.driver2.find_element_by_css_selector(
            '[data-test-id="vendor-locator-start-button"]').click()

        # Verify that correct vehicle location and assigned shop location is listed in shop locator
        self.assertEqual(make + ' ' + model + ' 2018\n' + currentAddress + '\n' + currentCity + currentCounty, self.driver2.find_element_by_css_selector(
            '[data-test-id="location-item-wrapper"]').text)
        self.assertEqual('Assigned Shop\n' + self.__class__.currentPinnedLocation, self.driver2.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[1].text)

        # Select a new shop
        selectedShop = self.driver2.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[3].text
        self.driver2.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[3].click()
        time.sleep(1)
        pinnedShopLocation = self.driver2.find_elements_by_css_selector(
            '[data-test-id="location-item-wrapper"]')[1].text
        self.assertEqual(selectedShop, pinnedShopLocation[:-9])
        self.__class__.currentPinnedLocation = pinnedShopLocation

        # Select 'Assign Shop'
        self.assertEqual('Change Shop', self.driver2.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div/div[2]/div/button/span').text)
        self.driver2.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div/div[2]/div/button/span').click()
        time.sleep(1)
        modalShopName = self.driver2.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]').text
        self.assertEqual(modalShopName, selectedShop[:len(modalShopName)])

        self.driver2.quit()

    def test_6search_LocateCreatedClaim(self):
        # Return to Search page
        self.driver.find_element_by_css_selector(
            '[data-test-id="app-header-search-icon"]').click()
        time.sleep(1)
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, '[data-test-id="app-header-search-input"]'))
        self.driver.find_element_by_css_selector(
            '[data-test-id="app-header-search-input"]').send_keys(
            claimNo, Keys.ENTER)
        time.sleep(1)
        self.assertEqual('Search', self.driver.find_element_by_css_selector(
            '[data-test-id="app-header-wrapper"] > h1').text)

        # Locate newly-created claim by Claim Number
        self.assertEqual(policyNo, self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/ul/div/div[2]/div/span/p/span[2]').text)
        self.assertEqual(claimNo, self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/ul/div/div[3]/div/div/p[1]/a/span/em').text)

        # Clear search text
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/input').clear()
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/input').send_keys(
            ' ', Keys.BACKSPACE)
        self.assertEqual('Please start typing to initiate the search.', self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/p/span').text)

        # Search for the Exposure associated with the claim
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/input').send_keys(
            firstName + ' ' + lastName)
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/input').send_keys(
            ' ' + claimNo)
        self.assertEqual(claimNo, self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/ul/div/div[3]/div/div/p[1]/a/span/em').text)

        # Select the claim link to view the claim
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/div/div[2]/ul/div/div[3]/div/div/p[1]/a/span/em').click()
        time.sleep(1)

    def test_7verifyChangeOfShop(self):
        # Select the exposure from the exposure list view
        self.driver.find_element_by_css_selector(
            '[data-test-id="exposure-list-view-wrapper"] > div._2Uw5j9uUR0MxAnT-phN0EC > div').click()

        # Verify that Shop Info has been updated
        shopCardName = self.driver.find_element_by_css_selector(
            '[data-test-id="shop-locator-card-details"] > div > span._13AJpbnc8oWgP-TGazCoK6').text
        self.assertEqual(shopCardName, self.__class__.currentPinnedLocation[:len(shopCardName)])

    def test_8logout(self):
        # Log out
        self.driver.find_element_by_css_selector('[data-icon="user"]').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('[data-test-id="app-header-logout"]').click()
        self.assertEqual('https://vice-frontend-integration.snapsheet.tech/login', self.driver.current_url)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    @classmethod
    def tearDownClass(inst):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        inst.driver.quit()

if __name__ == "__main__":
    unittest.main()