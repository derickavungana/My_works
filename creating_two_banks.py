from playwright.sync_api import sync_playwright
import random
import string
from datetime import datetime

#from Unittest import login


def generate_random_bank_details():
    """
    Generate random bank details for testing

    Returns:
        dict: Dictionary containing random bank_name, bank_code, and bank_notes
    """
    # Generate random bank name
    bank_names = ['Global', 'Premier', 'Digital', 'Smart', 'Swift', 'Elite', 'Nexus', 'Apex', 'Capital', 'Horizon']
    bank_types = ['Bank', 'Financial', 'Trust', 'Savings', 'Credit', 'Securities']
    bank_name = f"{random.choice(bank_names)} {random.choice(bank_types)}"

    # Generate random bank code (3-5 uppercase letters)
    bank_code = ''.join(random.choices(string.ascii_uppercase, k=random.randint(3, 5)))

    # Generate random notes
    notes_templates = ['Testing', 'Development', 'QA', 'Demo', 'Production', 'Staging']
    bank_notes = f"{random.choice(notes_templates)} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return {
        'bank_name': bank_name,
        'bank_code': bank_code,
        'bank_notes': bank_notes
    }
def login(page, username='Admin', password='Pass123$'):
    """
    Login to the application

    Args:
        page: Playwright page object
        username (str): Username for login
        password (str): Password for login
    """
    sign_button = page.wait_for_selector('#signin-button')
    sign_button.click()
    page.wait_for_timeout(1000)

    username_field = page.wait_for_selector('#Username')
    username_field.type(username)

    password_field = page.wait_for_selector('#passwordField')
    password_field.type(password)

    login_button = page.wait_for_selector('button[name="button"]')
    login_button.click()
    page.wait_for_timeout(1000)


def navigate_to_setup(page):
    """Navigate to the Setup section"""
    setup = page.wait_for_selector('//div[text()=" Setup "]')
    setup.click()
    page.wait_for_timeout(1000)


def create_bank(page, bank_name, bank_code, bank_notes):
    """
    Create a new bank

    Args:
        page: Playwright page object
        bank_name (str): Name of the bank
        bank_code (str): Code for the bank
        bank_notes (str): Notes for the bank
    """
    bank_setup = page.wait_for_selector('//div[text()=" Banks "]')
    bank_setup.click()
    page.wait_for_timeout(1000)

    create_bank_btn = page.wait_for_selector('//mat-icon[text()="add"]')
    create_bank_btn.click()
    page.wait_for_timeout(500)

    bank_name_field = page.wait_for_selector('//input[@name="name"]')
    bank_name_field.type(bank_name)

    bank_code_field = page.wait_for_selector('//input[@name="code"]')
    bank_code_field.type(bank_code)

    bank_notes_field = page.wait_for_selector('//textarea[@name="notes"]')
    bank_notes_field.type(bank_notes)

    bank_save = page.wait_for_selector('//mat-icon[text()="save"]')
    bank_save.click()
    page.wait_for_timeout(2000)  # Wait longer for bank to be saved and committed


def refresh_bank_list(page):
    """
    Click the refresh button to reload the bank list before searching.
    """
    try:
        refresh_button = page.wait_for_selector('//button[.//span[normalize-space()="Refresh"]]', timeout=5000)
        refresh_button.click()
        page.wait_for_timeout(2000)  # Wait longer for page to stabilize after refresh
        print(f"  Debug: Refresh button clicked and page stabilized")
    except Exception as e:
        print(f"  Debug: Refresh button not found - {e}")
        pass


def search_bank(page, bank_name):
    """
    Search for a bank by name

    Args:
        page: Playwright page object
        bank_name (str): Name of the bank to search

    Returns:
        bool: True if bank found, False otherwise
    """
    # Find and focus the search field
    bank_search = page.wait_for_selector('//input[@placeholder="search..."]')

    # Clear any existing text first using fill
    bank_search.fill("")
    page.wait_for_timeout(300)

    # Type the bank name
    bank_search.type(bank_name)
    page.wait_for_timeout(1500)  # Wait longer for results to filter

    try:
        # Look for the bank name in the results - try multiple strategies
        bank_locator = page.locator(f"text={bank_name}")

        # Check if the element exists and is visible
        if bank_locator.count() > 0 and bank_locator.first.is_visible():
            return True

        # Alternative: search for partial text match in case of formatting
        partial_locator = page.locator(f"text~={bank_name}")
        if partial_locator.count() > 0 and partial_locator.first.is_visible():
            return True

        return False
    except Exception as e:
        print(f"  Debug: Search error - {e}")
        return False


def click_checkbox_by_label(page, label_text):
    """
    Click a checkbox control based on the visible label text.
    Targets DevExpress checkbox with role="checkbox" and class="dx-widget dx-checkbox"

    Args:
        page: Playwright page object
        label_text (str): The visible label text for the checkbox (e.g. "Active:" or "Approved:")

    Returns:
        str: The aria-checked status ("true" or "false") after clicking
    """
    # Find the checkbox div with role="checkbox" that follows the label
    checkbox_locator = page.locator(
        f'//span[normalize-space()="{label_text}"]/following::div[@role="checkbox"][contains(@class, "dx-checkbox")][1]')

    # Click the checkbox
    checkbox_locator.click()
    page.wait_for_timeout(1000)

    # Return the aria-checked status
    return checkbox_locator.get_attribute("aria-checked")


def update_bank_details(page):
    """
    Click the Update button to save/update/close the bank details.

    Args:
        page: Playwright page object
    """
    try:
        # Try multiple selector strategies to find the Update button
        selectors = [
            '//button//span[contains(@class, "mdc-button__label") and contains(text(), "Update")]',
            '//button[contains(., "Update")]',
            '//button//span[contains(text(), "Update")]',
            'button:has-text("Update")',
        ]

        update_button = None
        for selector in selectors:
            try:
                update_button = page.locator(selector).first
                if update_button.is_visible(timeout=2000):
                    print(f"  Debug: Found Update button with selector: {selector}")
                    break
            except:
                continue

        if update_button and update_button.is_visible():
            update_button.click()
            page.wait_for_timeout(2000)
            print(f"✓ Update button clicked successfully")
        else:
            print(f"⚠ Update button not found with any selector")
    except Exception as e:
        print(f"⚠ Error clicking Update button: {e}")
        pass


def delete_bank(page, bank_name):
    """
    Search for a bank and delete it by clicking the Delete button.

    Args:
        page: Playwright page object
        bank_name (str): Name of the bank to delete
    """
    # Search for the bank
    bank_search = page.wait_for_selector('//input[@placeholder="search..."]')
    bank_search.fill("")
    page.wait_for_timeout(300)
    bank_search.type(bank_name)
    page.wait_for_timeout(1500)

    # Find and double-click the bank to open it
    bank_locator = page.locator(f"text={bank_name}")
    if bank_locator.count() > 0 and bank_locator.first.is_visible():
        bank_locator.first.dblclick()
        page.wait_for_timeout(1000)
    else:
        print(f"⚠ Bank '{bank_name}' not found for deletion")
        return False

    # Click the Delete button
    try:
        delete_button = page.locator('//span[normalize-space()="Delete"]').first
        if delete_button.is_visible():
            delete_button.click()
            page.wait_for_timeout(1000)
            return True
        else:
            print(f"⚠ Delete button not found")
            return False
    except Exception as e:
        print(f"⚠ Error clicking Delete button: {e}")
        return False


def confirm_deletion(page):
    """
    Confirm the deletion by clicking "Yes, delete it!" button in the popup.

    Args:
        page: Playwright page object

    Returns:
        bool: True if deletion confirmed, False otherwise
    """
    try:
        # Find the confirmation button
        confirm_button = page.locator('//button[@class="swal2-confirm swal2-styled"]')
        if confirm_button.is_visible(timeout=5000):
            confirm_button.click()
            page.wait_for_timeout(2000)  # Wait for deletion to complete
            return True
        else:
            print(f"⚠ Confirmation button not found")
            return False
    except Exception as e:
        print(f"⚠ Error confirming deletion: {e}")
        return False


def toggle_bank_active_status(page, bank_name):
    """
    Double-click on a bank to open it and toggle the active checkbox

    Args:
        page: Playwright page object
        bank_name (str): Name of the bank to toggle

    Returns:
        str: The aria-checked status ("true" or "false")
    """
    bank_locator = page.locator(f"text={bank_name}")
    bank_locator.dblclick()
    page.wait_for_timeout(500)

    return click_checkbox_by_label(page, "Active:")


def main():
    """Main function to orchestrate bank creation, search, activation, and approval"""
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://localhost:4200/')
        page.wait_for_timeout(1000)

        try:
            # Generate random bank details
            bank_details = generate_random_bank_details()
            bank_name = bank_details['bank_name']
            bank_code = bank_details['bank_code']
            bank_notes = bank_details['bank_notes']

            print(f"\n{'=' * 60}")
            print(f"Generated Bank Details:")
            print(f"  Bank Name: {bank_name}")
            print(f"  Bank Code: {bank_code}")
            print(f"  Bank Notes: {bank_notes}")
            print(f"{'=' * 60}\n")

            # Login
            print("➤ Logging in...")
            login(page)
            print("✓ Login successful\n")

            # Navigate to Setup
            print("➤ Navigating to Setup...")
            navigate_to_setup(page)
            print("✓ Setup opened\n")

            # Create the first bank with random parameters
            print(f"➤ Creating first bank '{bank_name}'...")
            create_bank(
                page,
                bank_name=bank_name,
                bank_code=bank_code,
                bank_notes=bank_notes
            )
            print(f"✓ First bank '{bank_name}' created successfully\n")

            # Activate and approve the first bank
            print(f"➤ Refreshing bank list before search...")
            refresh_bank_list(page)

            print(f"➤ Searching for first bank '{bank_name}'...")
            bank_found = search_bank(page, bank_name)
            if bank_found:
                print(f"✓ First bank '{bank_name}' found successfully\n")
            else:
                print(f"✗ First bank '{bank_name}' not found\n")
                return

            print(f"➤ Activating bank '{bank_name}'...")
            status = toggle_bank_active_status(page, bank_name)

            if status == "true":
                print(f"✓ Bank '{bank_name}' is now ACTIVE (Checkbox checked)\n")
            elif status == "false":
                print(f"✓ Bank '{bank_name}' is now INACTIVE (Checkbox unchecked)\n")
            else:
                print(f"? Bank '{bank_name}' status: {status}\n")

            print(f"➤ Setting Approved status for bank '{bank_name}'...")
            try:
                approved_status = click_checkbox_by_label(page, "Approved:")
                if approved_status == "true":
                    print(f"✓ Bank '{bank_name}' is now APPROVED (Checkbox checked)\n")
                elif approved_status == "false":
                    print(f"✓ Bank '{bank_name}' is now NOT APPROVED (Checkbox unchecked)\n")
                else:
                    print(f"? Bank '{bank_name}' approved status: {approved_status}\n")
            except Exception:
                print(f"⚠ Approved checkbox not found or could not be toggled\n")

            print(f"➤ Updating bank details...")
            update_bank_details(page)
            print(f"✓ Bank details updated successfully\n")

            page.wait_for_timeout(2000)

            print(f"{'=' * 60}")
            print(f"SUMMARY for first bank:")
            print(f"  Bank Name: {bank_name}")
            print(f"  Bank Code: {bank_code}")
            print(f"  Status: ACTIVE & APPROVED")
            print(f"{'=' * 60}\n")

            # Create a second bank
            second_bank_details = generate_random_bank_details()
            second_bank_name = second_bank_details['bank_name']
            second_bank_code = second_bank_details['bank_code']
            second_bank_notes = second_bank_details['bank_notes']

            print(f"➤ Refreshing bank list before creating second bank...")
            refresh_bank_list(page)

            print(f"➤ Creating second bank '{second_bank_name}'...")
            create_bank(
                page,
                bank_name=second_bank_name,
                bank_code=second_bank_code,
                bank_notes=second_bank_notes
            )
            print(f"✓ Second bank '{second_bank_name}' created successfully\n")

            print(f"➤ Refreshing bank list before verifying banks...")
            refresh_bank_list(page)

            print(f"➤ Verifying first bank '{bank_name}' still exists...")
            if search_bank(page, bank_name):
                print(f"✓ First bank '{bank_name}' still exists\n")
            else:
                print(f"⚠ First bank '{bank_name}' could not be found after creating second bank\n")

            print(f"➤ Verifying second bank '{second_bank_name}' exists...")
            if search_bank(page, second_bank_name):
                print(f"✓ Second bank '{second_bank_name}' found successfully\n")
            else:
                print(f"✗ Second bank '{second_bank_name}' not found\n")
                return

            # Delete the second bank
            print(f"➤ Refreshing bank list before deletion...")
            refresh_bank_list(page)

            print(f"➤ Searching for second bank '{second_bank_name}' to delete...")
            deletion_started = delete_bank(page, second_bank_name)
            if deletion_started:
                print(f"✓ Delete button clicked, confirming deletion...\n")
                deletion_confirmed = confirm_deletion(page)
                if deletion_confirmed:
                    print(f"✓ Second bank '{second_bank_name}' deleted successfully\n")
                else:
                    print(f"✗ Failed to confirm deletion for second bank\n")
            else:
                print(f"✗ Failed to initiate deletion for second bank\n")

        except Exception as e:
            print(f"✗ Error occurred: {e}\n")

        finally:
            browser.close()
            print("✓ Browser closed successfully")


if __name__ == "__main__":
    main()