import time

import pytest
from playwright.sync_api import expect, sync_playwright, Playwright
from pathlib import Path

url_file_path = Path(__file__).parent/"reach_jobs_domain.txt"
with open(url_file_path, "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

@pytest.mark.parametrize("url", urls)
def test_form_present_in_first_job_for_each_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=["--start-maximized"])
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(2)

        if not page.locator("#job-listings-wrapper").is_visible():
            print(f"No jobs are visible in the {url}.\n")
        else:
            try:
                page.get_by_text("No jobs match your search criteria. Please try a different search.").wait_for(timeout=50000)
                print(f"No jobs are visible in the {url}.\n")
            except:
                page.wait_for_selector('#job-listings-wrapper .listing h3.listing-title', timeout=50000)
                job_clicked = page.locator("#job-listings-wrapper .listing h3.listing-title").first.text_content()
                page.locator("#job-listings-wrapper .listing h3.listing-title").first.click(), f"Clicking on the first job was not successful for {url}.\n"
                print(f"{url}: {job_clicked}")
                try:
                    expect(page.get_by_text("Start Here", exact=True)).to_be_visible(timeout=50000), f"Start Here is not visible for {url}.\n"
                except:
                    expect(page.get_by_text("Complete Form to Start Application Process", exact=True)).to_be_visible(
                        timeout=30000), f"Complete Form is not visible for {url}.\n"
                expect(page.get_by_text("Name*")).to_be_visible(), f"Input field Name is not visible for {url}.\n"
                expect(page.get_by_label("Email*")).to_be_visible(), f"Input field Email is not visible for {url}.\n"
                expect(page.get_by_label("Phone*")).to_be_visible(), f"Input field Phone is not visible for {url}.\n"
                # expect(page.get_by_label("Zip*")).to_be_visible(), f"Input field Zip is not visible for {url}.\n"
                # consent_text = "I agree to receive marketing calls, SMS/MMS text messages, including an automated dialing system and/or artificial/pre-recorded voice, from or on behalf of Randall Reilly Talent, LLC and MCK Trucking. Msg and data rates may apply. Msg frequency varies. Consent is not a condition of any purchase. Opt out any time by replying STOP."

                try:
                    american_consent_text = "I agree to receive marketing calls, SMS/MMS text messages, including an automated dialing system and/or artificial/pre-recorded voice, from or on behalf of Randall Reilly Talent,"
                    expect(page.locator("label[for='clickwrap-consent-checkbox']")).to_contain_text(american_consent_text), f"Consent text was not visible for {url}.\n"
                    consent_checkbox = page.locator("#clickwrap-consent-checkbox")
                    assert not consent_checkbox.is_checked()
                    expect(page.get_by_role("button", name="Agree to Submit")).to_be_visible()

                    page.locator("#clickwrap-consent-checkbox").click()
                    page.get_by_role("button", name="I Agree, Submit").click()
                    error_msg = "There was a problem with your submission. Please review the fields below."
                    expect(page.get_by_text(error_msg)).to_be_visible()
                    time.sleep(2)
                except:
                    canadian_consent_text = "Please keep me up to date about job opportunities! I agree to receive automated marketing calls or text messages to the telephone number provided (including prerecorded and/or automated or autodialed calls or text messages), regardless of any previous registration on any Do Not Call list, and marketing emails to the email address provided from or on behalf of"
                    expect(page.locator(".internal-opt-in-statement")).to_contain_text(canadian_consent_text)
                    expect(page.get_by_role("button",name="I Agree, Submit")).to_be_visible()
                    page.get_by_role("button", name="I Agree, Submit").click()
                    error_msg = "There was a problem with your submission. Please review the fields below."
                    expect(page.get_by_text(error_msg)).to_be_visible()
                    time.sleep(2)

