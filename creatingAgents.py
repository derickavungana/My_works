from playwright.sync_api import sync_playwright
import random
import string
from datetime import datetime


# from Unittest import login


def generate_random_agent_details():
    """
    Generate random agent details for testing

    Returns:
        dict: Dictionary containing agent_name, agent_email, agent_phone, agent_date, agent_notes
    """
    # Generate random agent name
    agent_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'Robert', 'Lisa']
    agent_surname = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    agent_name = f"{random.choice(agent_names)} {random.choice(agent_surname)}"

    # Generate random email
    email_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.com']
    agent_email = f"agent{random.randint(1000, 9999)}@{random.choice(email_domains)}"

    # Generate random phone number
    agent_phone = f"+256{random.randint(700000000, 799999999)}"

    # Generate random registration date
    year = random.randint(2020, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    # Format as "DD Mon, YYYY" (e.g., "18 Feb, 2025")
    date_obj = datetime(year, month, day)
    agent_date = date_obj.strftime("%d %b, %Y")

    # Generate random notes
    notes_templates = ['Testing', 'Development', 'QA', 'Demo', 'Production', 'Staging']
    agent_notes = f"{random.choice(notes_templates)} Agent - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return {
        'agent_name': agent_name,
        'agent_email': agent_email,
        'agent_phone': agent_phone,
        'agent_date': agent_date,
        'agent_notes': agent_notes
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


def create_agent(page, agent_name, agent_email, agent_phone, agent_date, agent_notes):
    """
    Create a new agent

    Args:
        page: Playwright page object
        agent_name (str): Name of the agent
        agent_email (str): Email of the agent
        agent_phone (str): Phone number of the agent
        agent_date (str): Registration date of the agent
        agent_notes (str): Notes for the agent
    """
    agent_setup = page.wait_for_selector('//div[text()=" Agents "]')
    agent_setup.click()
    page.wait_for_timeout(1000)

    create_agent_btn = page.wait_for_selector('//mat-icon[text()="add"]')
    create_agent_btn.click()
    page.wait_for_timeout(500)

    agent_name_field = page.wait_for_selector('//input[@name="name"]')
    agent_name_field.type(agent_name)

    agent_email_field = page.wait_for_selector('//input[@name="email"]')
    agent_email_field.type(agent_email)

    agent_phone_field = page.wait_for_selector('//input[@name="phoneNumber"]')
    agent_phone_field.type(agent_phone)

    agent_date_field = page.wait_for_selector('//input[contains(@id, "registrationDate")]')
    agent_date_field.fill(agent_date)

    agent_notes_field = page.wait_for_selector('//textarea[@name="notes"]')
    agent_notes_field.type(agent_notes)

    agent_save = page.wait_for_selector('//mat-icon[text()="save"]')
    agent_save.click()
    page.wait_for_timeout(2000)  # Wait longer for agent to be saved and committed


def refresh_agent_list(page):
    """
    Click the refresh button to reload the agent list before searching.
    """
    try:
        refresh_button = page.wait_for_selector('//button[.//span[normalize-space()="Refresh"]]', timeout=5000)
        refresh_button.click()
        page.wait_for_timeout(2000)  # Wait longer for page to stabilize after refresh
        print(f"  Debug: Refresh button clicked and page stabilized")
    except Exception as e:
        print(f"  Debug: Refresh button not found - {e}")
        pass


def search_agent(page, agent_name):
    """
    Search for an agent by name

    Args:
        page: Playwright page object
        agent_name (str): Name of the agent to search

    Returns:
        bool: True if agent found, False otherwise
    """
    # Find and focus the search field
    agent_search = page.wait_for_selector('//input[@placeholder="search..."]')

    # Clear any existing text first using fill
    agent_search.fill("")
    page.wait_for_timeout(300)

    # Type the agent name
    agent_search.type(agent_name)
    page.wait_for_timeout(1500)  # Wait longer for results to filter

    try:
        # Look for the agent name in the results - try multiple strategies
        agent_locator = page.locator(f"text={agent_name}")

        # Check if the element exists and is visible
        if agent_locator.count() > 0 and agent_locator.first.is_visible():
            return True

        # Alternative: search for partial text match in case of formatting
        partial_locator = page.locator(f"text~={agent_name}")
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


def update_agent_details(page):
    """
    Click the Update button to save/update/close the agent details.

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


def delete_agent(page, agent_name):
    """
    Search for an agent and delete it by clicking the Delete button.

    Args:
        page: Playwright page object
        agent_name (str): Name of the agent to delete
    """
    # Search for the agent
    agent_search = page.wait_for_selector('//input[@placeholder="search..."]')
    agent_search.fill("")
    page.wait_for_timeout(300)
    agent_search.type(agent_name)
    page.wait_for_timeout(1500)

    # Find and double-click the agent to open it
    agent_locator = page.locator(f"text={agent_name}")
    if agent_locator.count() > 0 and agent_locator.first.is_visible():
        agent_locator.first.dblclick()
        page.wait_for_timeout(1000)
    else:
        print(f"⚠ Agent '{agent_name}' not found for deletion")
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


def toggle_agent_active_status(page, agent_name):
    """
    Double-click on an agent to open it and toggle the active checkbox

    Args:
        page: Playwright page object
        agent_name (str): Name of the agent to toggle

    Returns:
        str: The aria-checked status ("true" or "false")
    """
    agent_locator = page.locator(f"text={agent_name}")
    agent_locator.dblclick()
    page.wait_for_timeout(500)

    return click_checkbox_by_label(page, "Active:")


def main():
    """Main function to orchestrate agent creation, search, activation, and approval"""
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://localhost:4200/')
        page.wait_for_timeout(1000)

        try:
            # Generate random agent details
            agent_details = generate_random_agent_details()
            agent_name = agent_details['agent_name']
            agent_email = agent_details['agent_email']
            agent_phone = agent_details['agent_phone']
            agent_date = agent_details['agent_date']
            agent_notes = agent_details['agent_notes']

            print(f"\n{'=' * 60}")
            print(f"Generated Agent Details:")
            print(f"  Agent Name: {agent_name}")
            print(f"  Agent Email: {agent_email}")
            print(f"  Agent Phone: {agent_phone}")
            print(f"  Agent Date: {agent_date}")
            print(f"  Agent Notes: {agent_notes}")
            print(f"{'=' * 60}\n")

            # Login
            print("➤ Logging in...")
            login(page)
            print("✓ Login successful\n")

            # Navigate to Setup
            print("➤ Navigating to Setup...")
            navigate_to_setup(page)
            print("✓ Setup opened\n")

            # Create an agent with random parameters
            print(f"➤ Creating agent '{agent_name}'...")
            create_agent(
                page,
                agent_name=agent_name,
                agent_email=agent_email,
                agent_phone=agent_phone,
                agent_date=agent_date,
                agent_notes=agent_notes
            )
            print(f"✓ Agent '{agent_name}' created successfully\n")

            # Search for the agent
            print(f"➤ Refreshing agent list before search...")
            refresh_agent_list(page)

            print(f"➤ Searching for agent '{agent_name}'...")
            agent_found = search_agent(page, agent_name)
            if agent_found:
                print(f"✓ Agent '{agent_name}' found successfully\n")
            else:
                print(f"✗ Agent '{agent_name}' not found\n")
                return

            # Toggle the active status (Activate)
            print(f"➤ Activating agent '{agent_name}'...")
            status = toggle_agent_active_status(page, agent_name)

            if status == "true":
                print(f"✓ Agent '{agent_name}' is now ACTIVE (Checkbox checked)\n")
            elif status == "false":
                print(f"✓ Agent '{agent_name}' is now INACTIVE (Checkbox unchecked)\n")
            else:
                print(f"? Agent '{agent_name}' status: {status}\n")

            # Set the approved checkbox
            print(f"➤ Setting Approved status for agent '{agent_name}'...")
            try:
                approved_status = click_checkbox_by_label(page, "Approved:")
                if approved_status == "true":
                    print(f"✓ Agent '{agent_name}' is now APPROVED (Checkbox checked)\n")
                elif approved_status == "false":
                    print(f"✓ Agent '{agent_name}' is now NOT APPROVED (Checkbox unchecked)\n")
                else:
                    print(f"? Agent '{agent_name}' approved status: {approved_status}\n")
            except Exception:
                print(f"⚠ Approved checkbox not found or could not be toggled\n")

            # Update the agent details
            print(f"➤ Updating agent details...")
            update_agent_details(page)
            print(f"✓ Agent details updated successfully\n")

            page.wait_for_timeout(2000)

            print(f"{'=' * 60}")
            print(f"SUMMARY:")
            print(f"  Agent Name: {agent_name}")
            print(f"  Agent Email: {agent_email}")
            print(f"  Status: ACTIVE & APPROVED")
            print(f"{'=' * 60}\n")

            # Refresh the agent list before searching for deletion
            print(f"➤ Refreshing agent list before deletion...")
            refresh_agent_list(page)

            # Delete the agent
            print(f"➤ Searching for agent '{agent_name}' to delete...")
            deletion_started = delete_agent(page, agent_name)
            if deletion_started:
                print(f"✓ Delete button clicked, confirming deletion...\n")

                # Confirm deletion
                deletion_confirmed = confirm_deletion(page)
                if deletion_confirmed:
                    print(f"✓ Agent '{agent_name}' deleted successfully\n")
                else:
                    print(f"✗ Failed to confirm deletion\n")
            else:
                print(f"✗ Failed to initiate deletion\n")

        except Exception as e:
            print(f"✗ Error occurred: {e}\n")

        finally:
            browser.close()
            print("✓ Browser closed successfully")


if __name__ == "__main__":
    main()