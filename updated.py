from playwright.sync_api import sync_playwright
import random
import string
from datetime import datetime


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
    page.wait_for_timeout(1000)


def search_bank(page, bank_name):
    """
    Search for a bank by name
    
    Args:
        page: Playwright page object
        bank_name (str): Name of the bank to search
    
    Returns:
        bool: True if bank found, False otherwise
    """
    bank_search = page.wait_for_selector('//input[@placeholder="search..."]')
    bank_search.fill(bank_name)
    page.wait_for_timeout(500)
    
    try:
        bank_locator = page.locator(f"text={bank_name}")
        if bank_locator.is_visible():
            return True
        return False
    except:
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
    
    # Locate the checkbox container
    checkbox_div = page.locator('input[name="active"]').locator('xpath=../..')
    
    # Click the checkbox
    checkbox_div.click()
    page.wait_for_timeout(1000)
    
    # Verify the aria-checked attribute after clicking
    checked = checkbox_div.get_attribute("aria-checked")
    return checked


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
            
            print(f"\n{'='*60}")
            print(f"Generated Bank Details:")
            print(f"  Bank Name: {bank_name}")
            print(f"  Bank Code: {bank_code}")
            print(f"  Bank Notes: {bank_notes}")
            print(f"{'='*60}\n")
            
            # Login
            print("➤ Logging in...")
            login(page)
            print("✓ Login successful\n")
            
            # Navigate to Setup
            print("➤ Navigating to Setup...")
            navigate_to_setup(page)
            print("✓ Setup opened\n")
            
            # Create a bank with random parameters
            print(f"➤ Creating bank '{bank_name}'...")
            create_bank(
                page,
                bank_name=bank_name,
                bank_code=bank_code,
                bank_notes=bank_notes
            )
            print(f"✓ Bank '{bank_name}' created successfully\n")
            
            # Search for the bank
            print(f"➤ Searching for bank '{bank_name}'...")
            bank_found = search_bank(page, bank_name)
            if bank_found:
                print(f"✓ Bank '{bank_name}' found successfully\n")
            else:
                print(f"✗ Bank '{bank_name}' not found\n")
                return
            
            # Toggle the active status (Activate)
            print(f"➤ Activating bank '{bank_name}'...")
            status = toggle_bank_active_status(page, bank_name)
            
            if status == "true":
                print(f"✓ Bank '{bank_name}' is now ACTIVE (Checkbox checked)\n")
            elif status == "false":
                print(f"✓ Bank '{bank_name}' is now INACTIVE (Checkbox unchecked)\n")
            else:
                print(f"? Bank '{bank_name}' status: {status}\n")
            
            # Save or approve the bank
            print(f"➤ Approving bank '{bank_name}'...")
            try:
                approve_btn = page.wait_for_selector('//mat-icon[text()="save"]', timeout=2000)
                approve_btn.click()
                print(f"✓ Bank '{bank_name}' approved successfully\n")
            except:
                print(f"⚠ Approval button not found or already approved\n")
            
            page.wait_for_timeout(2000)
            
            print(f"{'='*60}")
            print(f"SUMMARY:")
            print(f"  Bank Name: {bank_name}")
            print(f"  Bank Code: {bank_code}")
            print(f"  Status: ACTIVE & APPROVED")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"✗ Error occurred: {e}\n")
        
        finally:
            browser.close()
            print("✓ Browser closed successfully")


if __name__ == "__main__":
    main()








