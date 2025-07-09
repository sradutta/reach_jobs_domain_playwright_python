'''
As the name suggests, it navigates to the Werner page and clicks
on the first job that is listed on the page. It then fills in the
form, submits and asserts that the form-submission-success-message
is shown.

This can be a flaky test as form fields might change based on the job.
'''

import pytest
from playwright.sync_api import Playwright, expect, sync_playwright
import time
import re

@pytest.mark.parametrize("url", ['https://jobs.werner.com/', ])
def test_werner_application_submission(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=["--start-maximized"])  # Set headless=True if you don't need UI
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the page
        page.goto(url, wait_until='domcontentloaded')

        # Click on the first job listing
        page.locator('#job-listings-wrapper .listing h3.listing-title').first.click()

        # Fill out the form
        page.get_by_label('First').fill('Test')
        time.sleep(5)
        page.get_by_label('Last').fill('Test')
        time.sleep(2)
        page.get_by_text('Email*').fill('pmtesting@randallreilly.com')
        time.sleep(2)
        page.get_by_label('Phone*').fill('6315555555')
        time.sleep(2)
        page.get_by_label('Zip').fill('10001')
        page.get_by_label('Current Experience Level:*').select_option(value='6 or More Months')
        page.locator('#clickwrap-consent-checkbox').check()

        # Submit the form and wait for navigation
        with page.expect_navigation():
            page.get_by_text('I Agree, Submit', exact=True).click()

        # Assertions
        expect(page).to_have_url(re.compile(r".*confirmation-page=true"))
        expect(page.locator('.container')).to_contain_text(
            'Thank you for your interest in Werner. We are currently reviewing submissions. No further action is required at this time.'
        )
        browser.close()
