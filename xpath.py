from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as play:
        browser=play.chromium.launch(headless=False)
        page=browser.new_page()
        page.goto('https://localhost:4200/')

        signin_element=page.wait_for_selector('#signin-button')
        signin_element.click()
        page.wait_for_timeout(1000)

        # xpath - Relative xpath '//'
        #Using attribute  - //tagname[@attributename = "value"]
        username_element=page.wait_for_selector('//input[@name="Username"]')
        username_element.type('testuser')
        password_element=page.wait_for_selector('//input[@name="Password"]')
        password_element.type('Pass123$')
        login_element=page.wait_for_selector('//button[@name="button"]')
        login_element.click()
        page.wait_for_timeout(5000)

except:
    print('An error occurred')
finally:
    browser.close()
