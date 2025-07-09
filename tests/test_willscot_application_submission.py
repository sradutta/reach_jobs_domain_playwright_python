'''
As the name suggests, it navigates to the WillScot page and clicks
on the first job that is listed on the page. It then fills in the
form, submit and assert that the form-submission-success-message
is shown.

Since WillScot's form changes based on license-type, the test loops through
all the license-types.

This can be a flaky test as form fields might change based on the job.
'''

import pytest
from playwright.sync_api import sync_playwright, expect
import time

@pytest.mark.parametrize("url",['https://willscotjobs.stratasjobs.com/',])
@pytest.mark.parametrize("license_type", ["Class A CDL", "Class 1 Canadian License", "Neither"])
def test_willscot_application_submission(url,license_type):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # change to True in CI
        context = browser.new_context()
        page = context.new_page()

        # Navigate and open job listing
        page.goto(url, wait_until='domcontentloaded')
        page.get_by_role("heading", name="Local CDL-A Driver Tech").first.click()

        # Fill in common form fields
        page.get_by_label('First').fill('Test')
        time.sleep(5)
        page.get_by_label('Last').fill('Test')
        time.sleep(5)
        page.get_by_text('Email*').fill('pmtesting@randallreilly.com')
        time.sleep(5)
        page.get_by_label('Phone*').fill('6315555555')
        page.get_by_label('City').fill('NYC')
        page.get_by_label('State / Province / Region').fill('NY')
        page.get_by_label('ZIP / Postal Code').fill('10001')
        page.locator('.ginput_address_country select').select_option(value="United States")

        # Choose license type
        page.get_by_label('Do you have a valid Class A CDL or a Class 1 license?').select_option(value=license_type)

        if license_type == "Class A CDL":
            page.get_by_label('How much Class A driving experience do you have?').select_option(value='4+ years')

        elif license_type == "Class 1 Canadian License":
            page.get_by_label('Are you legally authorized to work in Canada and/or do you currently hold a valid work permit to work in Canada?').select_option(value='Yes')
            page.get_by_label('How much AZ/Class 1 Canadian Commercial driving experience do you have?').select_option('4+ years')
            page.get_by_label('Do you have experience with a Toter truck?').select_option(value='Yes')
            page.get_by_label('How much experience do you have with a Toter truck?').select_option(value='4+ years')

        # Final shared fields
        page.get_by_label('Do you have wide-load hauling experience?').select_option(value='Yes')
        page.locator('#clickwrap-consent-checkbox').check()

        # Submission or rejection handling
        if license_type == "Neither":
            expect(page.get_by_text("We're sorry, you do not meet the current requirements.")).to_be_visible()
        else:
            page.get_by_text('I Agree, Submit', exact=True).click()
            expect(page.locator('.container')).to_contain_text(
                'Thank you for your interest in WillScot. We are currently reviewing submissions. No further action is required at this time.'
            )

        browser.close()
