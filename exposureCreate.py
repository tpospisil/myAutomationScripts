#! python3/usr/bin/env

import time, datetime, names, sys, random
from selenium import webdriver
from selenium.webdriver.support.ui import Select

def main():

    now = datetime.datetime.now().strftime('%m%d%H%M%S')

    email = 'tyler.pospisil+test@snapsheet.me'

    claimNo = 'claim' + now
    policyNo = 'policy' + now

    firstName = names.get_first_name()
    lastName = names.get_last_name()
    currentAddress = '62 O\'Connell Street Upper'
    currentCity = 'Dublin'
    currentCounty = '4'
    cars = {'Toyota':['Camry','Corolla','Prius'], 'Honda':['Accord','Civic','CR-V'], 'Ford':['F-150','Escape','Focus']}
    make, models = random.choice(list(cars.items()))
    model = random.choice(models)

    driver = webdriver.Chrome()

    # Navigate to webpage
    driver.get("https://vice-frontend-integration.snapsheet.tech/")

    # Sign in
    driver.find_element_by_css_selector(
        '[data-test-id="login_form_email_input"]').send_keys(
        email)
    driver.find_element_by_css_selector(
        '[data-test-id="login_form_password_input').send_keys(
        "2Plustwoequalsfive!")
    driver.find_element_by_css_selector(
        '#app > div > div > div._1lWQjoWRvEuXiIoWRyOPYh > div > div:nth-child(6) > button').click()
    time.sleep(2)

    # Create New Claim
    driver.find_element_by_css_selector(
        '#app > div > div > div.O2oH4V0LOoizIYDgzvgNj > div > div._266sD5YxjUkjzOakD2jBHv > button > span').click()
    driver.find_element_by_css_selector(
        '#app > div > div > div._1YlF0xeG8atxX5hpNMebqS > div > label:nth-child(3) > input').send_keys(
        policyNo)
    driver.find_element_by_css_selector(
        '#app > div > div > div._1YlF0xeG8atxX5hpNMebqS > div > label:nth-child(4) > input').send_keys(
        claimNo)
    driver.find_element_by_css_selector(
        '[data-test-id="new-short-claim-submit-button"]').click()
    time.sleep(1)

    # Select 'New Exposure'
    driver.find_element_by_css_selector(
        '[data-test-id="exposure-list-view-new-button"]').click()

    # Populate Exposure fields
    driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/div/div[1]/div/label/div').click()
    driver.find_element_by_xpath(
        '//label[@for="claimant.firstName"]/following-sibling::input[1]').send_keys(
        firstName)
    driver.find_element_by_xpath(
        '//label[@for="claimant.surname"]/following-sibling::input[1]').send_keys(
        lastName)
    driver.find_element_by_xpath(
        '//label[@for="claimant.address.address1"]/following-sibling::input[1]').send_keys(
        currentAddress)
    driver.find_element_by_xpath(
        '//label[@for="claimant.address.city"]/following-sibling::input[1]').send_keys(
        currentCity)
    driver.find_element_by_xpath(
        '//label[@for="claimant.address.region"]/following-sibling::input[1]').send_keys(
        currentCounty)
    driver.find_element_by_xpath(
        '//label[@for="claimant.preferredContact"]/following-sibling::div[1]/label[1]/div/span').click()
    driver.find_element_by_xpath(
        '//label[@for="claimant.email"]/following-sibling::input[1]').send_keys(
        email)
    driver.find_element_by_xpath(
        '//label[@for="claimant.phone"]/following-sibling::input[1]').send_keys(
        '13195412283')
    driver.find_element_by_xpath(
        '//label[@for="vehicle.registrationNumber"]/following-sibling::input[1]').send_keys(
        '182-D-12345')
    driver.find_element_by_xpath(
        '//label[@for="vehicle.vin"]/following-sibling::input[1]').send_keys(
        '19XFC2F54JE004299')
    driver.find_element_by_xpath(
        '//label[@for="vehicle.make"]/following-sibling::input[1]').send_keys(
        make)
    driver.find_element_by_xpath(
        '//label[@for="vehicle.model"]/following-sibling::input[1]').send_keys(
        model)
    driver.find_element_by_xpath(
        '//label[@for="vehicle.year"]/following-sibling::input[1]').send_keys(
        '2018')
    driver.find_element_by_xpath(
        '//label[@for="vehicle.address.address1"]/following-sibling::input[1]').send_keys(
        currentAddress)
    driver.find_element_by_xpath(
        '//label[@for="vehicle.address.city"]/following-sibling::input[1]').send_keys(
        currentCity)
    driver.find_element_by_xpath(
        '//label[@for="vehicle.address.region"]/following-sibling::input[1]').send_keys(
        currentCounty)

    # Click 'Save' to save new exposure
    driver.find_element_by_css_selector(
        '[data-test-id="exposure-new-view-save-button"]').click()
    time.sleep(2)

    print('\nYour Claim Number is %s.\n' % claimNo)

    driver.quit()

if __name__ == "__main__":
    main()