from playwright.sync_api import sync_playwright

with sync_playwright() as play:
    browser=play.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto('https://localhost:4200/')

    signin_element=page.wait_for_selector('#signin-button', timeout=3000)
    signin_element.click()

    #using attributes
    #reset_password=page.wait_for_selector('//a[@href="/Account/ForgotPassword"]', timeout=3000)
    #reset_password.click()

    #using text
    reset_pass=page.wait_for_selector('//a[text()="Forgot Password?"]').click()

    email_element=page.wait_for_selector('#Email', timeout=3000)
    email_element.type('testtrustee@test.com')
    submit_element=page.wait_for_selector('//input[@value="Submit"]', timeout=5000)
    submit_element.click()
    page.wait_for_timeout(20000)

