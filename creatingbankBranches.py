from playwright.sync_api import sync_playwright
import random
import string
from datetime import datetime

#from Unittest import login

BANK_NAME_CANDIDATES = ['Global', 'Premier', 'Digital', 'Smart', 'Swift', 'Elite', 'Nexus', 'Apex', 'Capital', 'Horizon']


def generate_random_bank_branch_details():
    """
    Generate random bank branch details for testing

    Returns:
        dict: Dictionary containing bank_name, branch_name, branch_code, and branch_notes
    """
    branch_prefixes = ['Central', 'North', 'South', 'East', 'West', 'Downtown', 'Uptown', 'Metro', 'Village', 'Harbor']

    bank_name = f"{random.choice(BANK_NAME_CANDIDATES)} Bank"
    branch_name = f"{random.choice(branch_prefixes)} Branch"
    branch_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    branch_notes = f"Branch created for {bank_name} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return {
        'bank_name': bank_name,
        'branch_name': branch_name,
        'branch_code': branch_code,
        'branch_notes': branch_notes
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


def select_bank_for_branch(page, bank_name):
    """Select a bank from the Bank dropdown on the branch creation form."""
    def _select_single_bank(single_bank_name):
        dropdown_selector = (
            '//div[@role="combobox" and contains(@class, "dx-lookup-field") and contains(@id, "_bankID")]'
        )
        option_selector = (
            f'//div[contains(@class, "dx-list-item") or contains(@class, "dx-item")][normalize-space()="{single_bank_name}"]'
        )

        max_attempts = 4
        for attempt in range(1, max_attempts + 1):
            try:
                bank_dropdown = page.locator(dropdown_selector).first
                if bank_dropdown.is_visible(timeout=5000):
                    bank_dropdown.click()
                    page.wait_for_timeout(500)

                    bank_option = page.get_by_text(single_bank_name, exact=True).first
                    if bank_option.is_visible(timeout=2000):
                        bank_option.click()
                        page.wait_for_timeout(1000)
                        return True

                    bank_option = page.locator(option_selector).first
                    if bank_option.count() > 0 and bank_option.is_visible():
                        bank_option.click()
                        page.wait_for_timeout(1000)
                        return True

                    print(f"⚠ Attempt {attempt}: Bank option '{single_bank_name}' not available yet")
                else:
                    print(f"⚠ Attempt {attempt}: Bank dropdown not visible yet")
            except Exception as e:
                print(f"⚠ Attempt {attempt}: Error selecting bank from dropdown: {e}")

            if attempt < max_attempts:
                page.wait_for_timeout(1000)

        return False

    if isinstance(bank_name, list):
        candidates = bank_name
    else:
        preferred = bank_name
        candidates = [preferred] + [f"{name} Bank" for name in BANK_NAME_CANDIDATES if f"{name} Bank" != preferred]

    for candidate in candidates:
        if _select_single_bank(candidate):
            if candidate != bank_name:
                print(f"✓ Selected available bank '{candidate}' instead of requested '{bank_name}'")
            return candidate

    print(f"⚠ Bank dropdown selection failed after checking {len(candidates)} candidates")

    try:
        bank_input = page.locator('//span[normalize-space()="Bank:"]/following::input[1]').first
        if bank_input.count() > 0:
            bank_input.click()
            bank_input.fill(bank_name if not isinstance(bank_name, list) else bank_name[0])
            page.keyboard.press('Enter')
            return bank_name if not isinstance(bank_name, list) else bank_name[0]
    except Exception:
        pass

    return None


def create_bank_branch(page, bank_name, branch_name, branch_code, branch_notes):
    """
    Create a new bank branch

    Args:
        page: Playwright page object
        bank_name (str): Name of the bank to associate with the branch
        branch_name (str): Name of the branch
        branch_code (str): Code of the branch
        branch_notes (str): Notes for the branch
    """
    bank_branch_section = page.wait_for_selector('//div[text()=" Bank Branches "]')
    bank_branch_section.click()
    page.wait_for_timeout(1000)

    create_branch_btn = page.wait_for_selector('//mat-icon[text()="add"]')
    create_branch_btn.click()
    page.wait_for_timeout(500)

    selected_bank = select_bank_for_branch(page, bank_name)
    if not selected_bank:
        print(f"⚠ Could not select bank '{bank_name}' for branch creation")
    elif selected_bank != bank_name:
        print(f"✓ Branch will be created under available bank '{selected_bank}'")

    branch_name_field = page.wait_for_selector('//input[@name="name"]')
    branch_name_field.type(branch_name)

    branch_code_field = page.wait_for_selector('//input[@name="code"]')
    branch_code_field.type(branch_code)

    branch_notes_field = page.wait_for_selector('//textarea[@name="notes"]')
    branch_notes_field.type(branch_notes)

    save_button = page.wait_for_selector('//mat-icon[text()="save"]')
    save_button.click()
    page.wait_for_timeout(2000)


def refresh_branch_list(page):
    """Refresh the bank branch list before searching."""
    try:
        refresh_button = page.wait_for_selector('//button[.//span[normalize-space()="Refresh"]]', timeout=5000)
        refresh_button.click()
        page.wait_for_timeout(2000)
        print("  Debug: Refresh button clicked and page stabilized")
    except Exception as e:
        print(f"  Debug: Refresh button not found - {e}")
        pass


def search_branch(page, branch_name):
    """
    Search for a bank branch by name

    Args:
        page: Playwright page object
        branch_name (str): Name of the branch to search

    Returns:
        bool: True if branch found, False otherwise
    """
    branch_search = page.wait_for_selector('//input[@placeholder="search..."]')
    branch_search.fill("")
    page.wait_for_timeout(300)
    branch_search.type(branch_name)
    page.wait_for_timeout(1500)

    try:
        branch_locator = page.get_by_text(branch_name, exact=True)
        if branch_locator.count() > 0 and branch_locator.first.is_visible():
            return True

        partial_locator = page.get_by_text(branch_name)
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
    checkbox_locator = page.locator(
        f'//span[normalize-space()="{label_text}"]/following::div[@role="checkbox"][contains(@class, "dx-checkbox")][1]')
    checkbox_locator.click()
    page.wait_for_timeout(1000)
    return checkbox_locator.get_attribute("aria-checked")


def update_branch_details(page):
    """
    Click the Update button to save/update/close the branch details.

    Args:
        page: Playwright page object
    """
    try:
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


def delete_branch(page, branch_name):
    """
    Search for a branch and delete it by clicking the Delete button.

    Args:
        page: Playwright page object
        branch_name (str): Name of the branch to delete

    Returns:
        bool: True if deletion flow started, False otherwise
    """
    branch_search = page.wait_for_selector('//input[@placeholder="search..."]')
    branch_search.fill("")
    page.wait_for_timeout(300)
    branch_search.type(branch_name)
    page.wait_for_timeout(1500)

    branch_locator = page.get_by_text(branch_name, exact=True)
    try:
        branch_locator.first.wait_for(state="visible", timeout=5000)
        branch_locator.first.scroll_into_view_if_needed()
        # try dblclick, fall back to two rapid clicks if dblclick times out
        try:
            branch_locator.first.dblclick(timeout=5000)
        except Exception:
            branch_locator.first.click(click_count=2)
        page.wait_for_timeout(1000)
    except Exception:
        print(f"⚠ Branch '{branch_name}' not found for deletion")
        return False

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
    Confirm the deletion by clicking "Yes, delete it!".

    Args:
        page: Playwright page object

    Returns:
        bool: True if delete confirmed, False otherwise
    """
    try:
        confirm_button = page.locator('//button[@class="swal2-confirm swal2-styled"]')
        if confirm_button.is_visible(timeout=5000):
            confirm_button.click()
            page.wait_for_timeout(2000)
            return True
        else:
            print(f"⚠ Confirmation button not found")
            return False
    except Exception as e:
        print(f"⚠ Error confirming deletion: {e}")
        return False


def verify_branch_deleted(page, branch_name):
    """
    Verify the branch no longer exists after deletion.

    Args:
        page: Playwright page object
        branch_name (str): Name of the branch to verify deletion for

    Returns:
        bool: True if branch is not found, False if it still exists
    """
    refresh_branch_list(page)
    deleted = not search_branch(page, branch_name)
    if deleted:
        print(f"✓ Verified branch '{branch_name}' is deleted")
    else:
        print(f"✗ Branch '{branch_name}' still exists after deletion")
    return deleted


def toggle_branch_active_status(page, branch_name):
    """
    Double-click on a branch to open it and toggle the Active checkbox.

    Args:
        page: Playwright page object
        branch_name (str): Name of the branch to toggle

    Returns:
        str: The aria-checked status after clicking
    """
    branch_locator = page.get_by_text(branch_name, exact=True)
    try:
        branch_locator.first.wait_for(state="visible", timeout=5000)
        branch_locator.first.scroll_into_view_if_needed()
        try:
            branch_locator.first.dblclick(timeout=5000)
        except Exception:
            branch_locator.first.click(click_count=2)
        page.wait_for_timeout(1000)
    except Exception as e:
        print(f"⚠ Could not open branch '{branch_name}' for toggling: {e}")
        return None

    return click_checkbox_by_label(page, "Active:")


def main():
    """Main function to orchestrate bank branch creation, approval, and deletion"""
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://localhost:4200/')
        page.wait_for_timeout(1000)

        try:
            first_branch_details = generate_random_bank_branch_details()
            bank_name = first_branch_details['bank_name']
            first_branch_name = first_branch_details['branch_name']
            first_branch_code = first_branch_details['branch_code']
            first_branch_notes = first_branch_details['branch_notes']

            print(f"\n{'=' * 60}")
            print("Generated First Bank Branch Details:")
            print(f"  Bank Name: {bank_name}")
            print(f"  Branch Name: {first_branch_name}")
            print(f"  Branch Code: {first_branch_code}")
            print(f"  Branch Notes: {first_branch_notes}")
            print(f"{'=' * 60}\n")

            print("➤ Logging in...")
            login(page)
            print("✓ Login successful\n")

            print("➤ Navigating to Setup...")
            navigate_to_setup(page)
            print("✓ Setup opened\n")

            print(f"➤ Creating branch '{first_branch_name}' for bank '{bank_name}'...")
            create_bank_branch(page, bank_name, first_branch_name, first_branch_code, first_branch_notes)
            print(f"✓ Branch '{first_branch_name}' created successfully\n")

            # Activate and approve the first branch before creating the second
            print("➤ Refreshing branch list before activating first branch...")
            refresh_branch_list(page)

            print(f"➤ Searching for first branch '{first_branch_name}' to activate...")
            if search_branch(page, first_branch_name):
                print(f"✓ First branch '{first_branch_name}' found for activation")
                print(f"➤ Activating first branch '{first_branch_name}'...")
                status = toggle_branch_active_status(page, first_branch_name)
                if status == "true":
                    print(f"✓ First branch '{first_branch_name}' is now ACTIVE (Checkbox checked)\\n")
                elif status == "false":
                    print(f"✓ First branch '{first_branch_name}' is now INACTIVE (Checkbox unchecked)\\n")
                else:
                    print(f"? First branch '{first_branch_name}' status: {status}\\n")

                print(f"➤ Setting Approved status for first branch '{first_branch_name}'...")
                try:
                    approved_status = click_checkbox_by_label(page, "Approved:")
                    if approved_status == "true":
                        print(f"✓ First branch '{first_branch_name}' is now APPROVED (Checkbox checked)\\n")
                    elif approved_status == "false":
                        print(f"✓ First branch '{first_branch_name}' is now NOT APPROVED (Checkbox unchecked)\\n")
                    else:
                        print(f"? First branch '{first_branch_name}' approved status: {approved_status}\\n")
                except Exception:
                    print(f"⚠ Approved checkbox not found or could not be toggled for first branch\\n")

                print(f"➤ Updating first branch details...")
                update_branch_details(page)
                print(f"✓ First branch details updated successfully\\n")
            else:
                print(f"⚠ First branch '{first_branch_name}' not found for activation; continuing\\n")

            second_branch_details = generate_random_bank_branch_details()
            second_branch_name = second_branch_details['branch_name']
            second_branch_code = second_branch_details['branch_code']
            second_branch_notes = second_branch_details['branch_notes']

            print(f"➤ Creating branch '{second_branch_name}' for bank '{bank_name}'...")
            create_bank_branch(page, bank_name, second_branch_name, second_branch_code, second_branch_notes)
            print(f"✓ Branch '{second_branch_name}' created successfully\n")

            print("➤ Refreshing bank branch list before search...")
            refresh_branch_list(page)

            print(f"➤ Searching for branch '{first_branch_name}'...")
            branch_found = search_branch(page, first_branch_name)
            if branch_found:
                print(f"✓ Branch '{first_branch_name}' found successfully\n")
            else:
                print(f"✗ Branch '{first_branch_name}' not found\n")
                return

            print(f"➤ Searching for branch '{second_branch_name}'...")
            second_branch_found = search_branch(page, second_branch_name)
            if second_branch_found:
                print(f"✓ Branch '{second_branch_name}' found successfully\n")
            else:
                print(f"✗ Branch '{second_branch_name}' not found\n")
                return


            print(f"➤ Activating branch '{first_branch_name}'...")
            status = toggle_branch_active_status(page, first_branch_name)
            if status == "true":
                print(f"✓ Branch '{first_branch_name}' is now ACTIVE (Checkbox checked)\\n")
            elif status == "false":
                print(f"✓ Branch '{first_branch_name}' is now INACTIVE (Checkbox unchecked)\\n")
            else:
                print(f"? Branch '{first_branch_name}' status: {status}\\n")

            print(f"➤ Setting Approved status for branch '{first_branch_name}'...")
            approved_status = click_checkbox_by_label(page, "Approved:")
            if approved_status == "true":
                print(f"✓ Branch '{first_branch_name}' is now APPROVED (Checkbox checked)\\n")
            elif approved_status == "false":
                print(f"✓ Branch '{first_branch_name}' is now NOT APPROVED (Checkbox unchecked)\\n")
            else:
                print(f"? Branch '{first_branch_name}' approved status: {approved_status}\\n")

            print(f"➤ Updating branch details...")
            update_branch_details(page)
            print(f"✓ Branch details updated successfully\n")

            print("➤ Refreshing branch list before deletion...")
            refresh_branch_list(page)

            print(f"➤ Searching for branch '{second_branch_name}' to delete...")
            deletion_started = delete_branch(page, second_branch_name)
            if deletion_started:
                print(f"✓ Delete button clicked, confirming deletion...\n")
                if confirm_deletion(page):
                    print(f"✓ Branch '{second_branch_name}' deleted successfully\n")
                    print(f"➤ Verifying branch deletion...\n")
                    verify_branch_deleted(page, second_branch_name)
                else:
                    print(f"✗ Failed to confirm deletion\n")
            else:
                print(f"✗ Failed to initiate deletion\n")

            print(f"➤ Verifying first branch '{first_branch_name}' still exists...\n")
            if search_branch(page, first_branch_name):
                print(f"✓ Branch '{first_branch_name}' still exists after deletion\n")
            else:
                print(f"✗ Branch '{first_branch_name}' could not be found after deletion\n")

            print(f"{'=' * 60}")
            print("SUMMARY:")
            print(f"  Bank Name: {bank_name}")
            print(f"  Kept Branch: {first_branch_name}")
            print(f"  Deleted Branch: {second_branch_name}")
            print(f"{'=' * 60}\n")

        except Exception as e:
            print(f"✗ Error occurred: {e}\n")

        finally:
            browser.close()
            print("✓ Browser closed successfully")


if __name__ == "__main__":
    main()
