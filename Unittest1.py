from playwright.sync_api import sync_playwright
import random
import string
from datetime import datetime


def generate_random_broker_details():
    names = ['Home', 'Global', 'Prime', 'First', 'Core']
    broker_name = f"{random.choice(names)} Broker"
    broker_code = ''.join(random.choices(string.ascii_uppercase, k=4))
    phone = f'+256{random.randint(700000000,799999999)}'
    email = f"{broker_code.lower()}@example.com"
    # Match creatingAgents.py date format: "DD Mon, YYYY" (e.g., "18 Feb, 2025")
    registration_date = datetime.now().strftime("%d %b, %Y")
    notes = f"Auto-created {datetime.now().isoformat()}"
    cash_account_name = f"{broker_code} Cash Account"
    cash_account_code = broker_code[:3]
    currency = 'United States dollar'
    bank_branch = 'Home Bank Branch'
    core_mode = 'NONE'
    account_number = str(random.randint(1000000000, 9999999999))
    iban = f'UG{random.randint(10**9, 10**10-1)}'
    allow_overdrawing = True

    return {
        'broker_name': broker_name,
        'broker_code': broker_code,
        'phone': phone,
        'email': email,
        'registration_date': registration_date,
        'notes': notes,
        'cash_account_name': cash_account_name,
        'cash_account_code': cash_account_code,
        'currency': currency,
        'bank_branch': bank_branch,
        'core_mode': core_mode,
        'account_number': account_number,
        'iban': iban,
        'allow_overdrawing': allow_overdrawing,
    }


def login(page, username='Admin', password='Pass123$'):
    signin = page.wait_for_selector('#signin-button')
    signin.click()
    page.wait_for_timeout(1000)

    username_field = page.wait_for_selector('//input[@name="Username"]')
    username_field.type(username)
    password_field = page.wait_for_selector('//input[@name="Password"]')
    password_field.type(password)
    login_btn = page.wait_for_selector('//button[@name="button"]')
    login_btn.click()
    page.wait_for_timeout(2000)


def navigate_to_setup(page):
    setup = page.wait_for_selector('//div[text()=" Setup "]')
    setup.click()
    page.wait_for_timeout(1000)


def refresh_list(page):
    try:
        refresh = page.wait_for_selector('//mat-icon[text()="refresh"]', timeout=3000)
        refresh.click()
        page.wait_for_timeout(1500)
    except Exception:
        pass


def create_broker(page, details: dict):
    # Open Brokers screen
    broker_nav = page.wait_for_selector('//div[text()=" Brokers "]')
    broker_nav.click()
    page.wait_for_timeout(500)

    # Click Add
    add_btn = page.wait_for_selector('//mat-icon[text()="add"]')
    add_btn.click()
    page.wait_for_timeout(300)

    # Fill fields (best-effort selectors)
    name_field = page.wait_for_selector('//input[@name="name"]')
    name_field.fill(details['broker_name'])

    code_field = page.wait_for_selector('//input[@name="code"]')
    code_field.fill(details['broker_code'])

    phone_field = page.locator('//input[@name="phoneNumber" or @placeholder="Phone Number" ]').first
    phone_field.fill(details['phone'])

    email_field = page.locator('//input[@name="email" or @placeholder="Email"]').first
    email_field.fill(details['email'])

    reg_field = page.locator('//div[contains(@class, "dx-datebox") and .//input[@name="registrationDate"]]//input[@role="combobox" and contains(@id, "_registrationDate")]').first
    try:
        reg_field.fill(details['registration_date'])
    except Exception:
        # Fallback to the hidden date input
        try:
            hidden_reg = page.locator('//input[@type="hidden" and @name="registrationDate"]').first
            hidden_reg.evaluate("(node, value) => node.value = value", details['registration_date'])
        except Exception:
            pass

    notes_field = page.locator('//textarea[@name="notes"]').first
    try:
        notes_field.fill(details['notes'])
    except Exception:
        pass

    save = page.wait_for_selector('//mat-icon[text()="save"]')
    save.click()
    page.wait_for_timeout(1500)


def add_cash_account(page, details: dict):
    try:
        add_ca = page.locator('//span[contains(., "Add Cash Account") or contains(., "Add Cash Account") ]').first
        add_ca.click()
        page.wait_for_timeout(500)

        ca_name = page.locator('//input[@name="name" and @placeholder="Name"]').first
        ca_name.fill(details['cash_account_name'])

        ca_code = page.locator('//input[@name="code" and @placeholder="Code"]').first
        ca_code.fill(details['cash_account_code'])

        ca_currency = page.locator('//select[@name="currency"] | //input[@placeholder="Currency"]').first
        try:
            ca_currency.select_option(label=details['currency'])
        except Exception:
            try:
                ca_currency.fill(details['currency'])
            except Exception:
                pass

        bank_branch = page.locator('//select[@name="bankBranch"] | //input[@placeholder="Bank Branch"]').first
        try:
            bank_branch.select_option(label=details['bank_branch'])
        except Exception:
            try:
                bank_branch.fill(details['bank_branch'])
            except Exception:
                pass

        core_mode = page.locator('//select[@name="coreMode"] | //input[@placeholder="Core Banking Realtime Integration Mode:"]').first
        try:
            core_mode.select_option(label=details['core_mode'])
        except Exception:
            pass

        acct_num = page.locator('//input[@name="accountNumber"]').first
        acct_num.fill(details['account_number'])

        iban = page.locator('//input[@name="iban"]').first
        try:
            iban.fill(details['iban'])
        except Exception:
            pass

        notes = page.locator('//textarea[@name="notes"]').first
        try:
            notes.fill(details['notes'])
        except Exception:
            pass

        if details.get('allow_overdrawing'):
            try:
                over = page.locator('//span[normalize-space()="Allow Overdrawing"]/following::div[@role="checkbox"][1]').first
                over.click()
            except Exception:
                pass

        save_update = page.locator('//mat-icon[text()="save"] | //mat-icon[text()="update"]').first
        save_update.click()
        page.wait_for_timeout(1000)
    except Exception:
        pass


def search_broker(page, broker_name: str) -> bool:
    search = page.wait_for_selector('//input[@placeholder="search..."]')
    search.fill("")
    page.wait_for_timeout(200)
    search.type(broker_name)
    page.wait_for_timeout(1200)

    try:
        locator = page.locator(f'text="{broker_name}"')
        if locator.count() > 0 and locator.first.is_visible():
            return True
        partial = page.locator(f'text={broker_name}')
        if partial.count() > 0 and partial.first.is_visible():
            return True
        return False
    except Exception:
        return False


def click_checkbox_by_label(page, label_text: str):
    checkbox_locator = page.locator(
        f'//span[normalize-space()="{label_text}"]/following::div[@role="checkbox"][contains(@class, "dx-checkbox")][1]')
    try:
        checkbox_locator.click()
        page.wait_for_timeout(500)
        return checkbox_locator.get_attribute("aria-checked")
    except Exception:
        # fallback: try input checkbox
        try:
            inp = page.locator(f'//input[@name and preceding::label[normalize-space()="{label_text}"]]')
            inp.click()
            page.wait_for_timeout(500)
            return inp.get_attribute('checked')
        except Exception:
            return None


def update_broker_details(page):
    try:
        selectors = [
            '//button//span[contains(text(), "Update")]',
            '//mat-icon[text()="update"]',
            'button:has-text("Update")'
        ]
        for sel in selectors:
            try:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=1500):
                    btn.click()
                    page.wait_for_timeout(1000)
                    return
            except Exception:
                continue
    except Exception:
        pass


def toggle_broker_active_status(page, broker_name: str):
    try:
        loc = page.locator(f'text="{broker_name}"').first
        loc.dblclick()
        page.wait_for_timeout(500)
    except Exception:
        try:
            loc = page.locator(f'text={broker_name}').first
            loc.click()
            page.wait_for_timeout(500)
        except Exception:
            pass

    return click_checkbox_by_label(page, "Active:")


def main():
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://localhost:4200/')
        page.wait_for_timeout(1000)

        try:
            details = generate_random_broker_details()
            print(f"Creating broker: {details['broker_name']}")

            login(page)
            navigate_to_setup(page)
            create_broker(page, details)
            refresh_list(page)

            found = search_broker(page, details['broker_name'])
            if not found:
                print(f"Broker '{details['broker_name']}' not found after create")
                browser.close()
                return

            # Toggle active and approved
            status = toggle_broker_active_status(page, details['broker_name'])
            print(f"Active status after toggle: {status}")

            try:
                appr = click_checkbox_by_label(page, "Approved:")
                print(f"Approved status after toggle: {appr}")
            except Exception:
                pass

            # Add cash account details
            add_cash_account(page, details)

            # Update/save
            update_broker_details(page)

            print(f"Completed broker creation for {details['broker_name']}")

        except Exception as e:
            print(f"Error in main: {e}")

        finally:
            browser.close()


if __name__ == "__main__":
    main()
