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

# create agents
    agent_setup = page.wait_for_selector('//div[text()=" Agents "]').click()
    page.wait_for_timeout(1000)
    create_agent = page.wait_for_selector('//mat-icon[text()="add"]').click()
    # page.wait_for_timeout(1000)
    # create_agent.click()
    agent_name = page.wait_for_selector('//input[@name="name"]')
    agent_name.type('Agent4')
    agent_email = page.wait_for_selector('//input[@name="email"]')
    agent_email.type('Agent4@gmail.com')
    agent_phone = page.wait_for_selector('//input[@name="phoneNumber"]')
    agent_phone.type('+2567291019773')
    # agent_date=page.wait_for_selector('//input[@type="text"]').click()
    # page.wait_for_timeout(1000)

    agent_date = page.get_by_label("registrationDate").fill("2020-02-02")
    #agent_date.type('12/12/2024')
    agent_notes = page.wait_for_selector('//textarea[@name="notes"]')
    agent_notes.type('Agent4')
    page.wait_for_timeout(1000)
    agent_save = page.wait_for_selector('//mat-icon[text()="save"]').click()
    # agent_save = page.wait_for_selector("//span[@class='mdc-button__label']").click()