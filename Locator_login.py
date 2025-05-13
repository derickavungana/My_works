from playwright.sync_api import sync_playwright

with sync_playwright() as play:

    browser=play.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto('https://localhost:4200/')
    page.wait_for_timeout(1000)


    sign_button=page.wait_for_selector('#signin-button')
    sign_button.click()
    page.wait_for_timeout(1000)

    Username=page.wait_for_selector('#Username')
    Username.type('Admin')
    #page.wait_for_timeout(3000)
    Password = page.wait_for_selector('#passwordField')
    Password.type('Pass123$')
    #page.wait_for_timeout(3000)

  # attributes 'input[name="value"]'
    Login=page.wait_for_selector('button[name="button"]')
    Login.click()
    page.wait_for_timeout(1000)

    setup = page.wait_for_selector('//div[text()=" Setup "]').click()
    #profile=page.query_selector('//span[text()="T"]').click()
    page.wait_for_timeout(1000)

# create banks
    bank_setup=page.wait_for_selector('//div[text()=" Banks "]').click()
    page.wait_for_timeout(1000)
    create_bank = page.wait_for_selector('//mat-icon[text()="add"]').click()
    bank_name=page.wait_for_selector('//input[@name="name"]')
    bank_name.type('Home Bank')
    bank_code=page.wait_for_selector('//input[@name="code"]')
    bank_code.type('HOME')
    bank_notes= page.wait_for_selector('//textarea[@name="notes"]')
    bank_notes.type('Testing')
    bank_save = page.wait_for_selector('//mat-icon[text()="save"]').click()

    #bank_refresh=page.wait_for_selector('//mat-icon[text()="refresh"]').click()
    bank_search=page.wait_for_selector('//input[@placeholder="search..."]')
    bank_search.type('Home Bank')
    bank_locator = page.locator("text=Home Bank")
    bank_locator.dblclick()
    #page.click("text=Home Bank")
    # If the clickable checkbox is nearby the input:
    # Locate the checkbox by looking for the input[name="active"] ancestor
    # First, locate the checkbox container
    checkbox_div = page.locator('input[name="active"]').locator('xpath=../..')

    # Click the checkbox (no need for evaluate here)
    checkbox_div.click()

    # Wait for DOM to update
    page.wait_for_timeout(5000)

# Verify the aria-checked attribute after clicking
checked = checkbox_div.get_attribute("aria-checked")
print(f"aria-checked value: {checked}")

# Check the state of the checkbox
if checked == "true":
    print("Checkbox is checked")
else:
    print("Checkbox is NOT checked")

page.wait_for_timeout(5000)








