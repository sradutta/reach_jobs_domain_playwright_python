'''
This test takes only one URL that is being passed through a pytest parametrization.
It navigates to the URL and takes the name of the first job that is listed
on the page. It then pastes the job in the input search box,
searches by that job, and returns the number of such jobs that were found.
Through this process, it is testing the page and also the search function.
'''

import pytest
from playwright.sync_api import Playwright, expect, sync_playwright
import time

@pytest.mark.parametrize("url", ["https://mcktrucking.stratasjobs.com/",]) # change the url here or input as many as you want
def test_individual_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=["--start-maximized"])
        context = browser.new_context()
        page = context.new_page()
        page.goto(url,wait_until='domcontentloaded')
        locator = page.locator('#job-listings-wrapper')

        if not locator.is_visible():
            print('Job Listing Wrapper not visible.')
        else:
            text = locator.inner_text()
            nojobtext1 = 'No jobs match your search criteria. Please try a different search.'
            nojobtext2 = 'No jobs match your search criteria. Getting suggested jobs.'

            if nojobtext1 in text or nojobtext2 in text:
                print("No jobs are found")
            else:
                page.wait_for_selector('#job-listings-wrapper .listing h3.listing-title', timeout=50000)
                search_term_locator = page.locator('#job-listings-wrapper .listing h3.listing-title').first
                raw_search_term = search_term_locator.text_content()
                search_term_with_dash = raw_search_term.strip() if raw_search_term else ''
                search_term = search_term_with_dash.split(" - ")[0]

                print(f"The search term is {search_term}\n")

                if len(search_term) > 0:
                    page.locator("#job-search").fill(search_term)
                    page.wait_for_timeout(5000)
                    page.click("#submit-search")
                    page.wait_for_timeout(9000)

                    job_listings = page.locator('#job-listings-wrapper .listing')
                    # print(f"The job listings are {job_listings}\n")
                    num_of_jobs_listed = job_listings.count()
                    # print(f"The number of jobs listed are {num_of_jobs_listed}")

                    assert num_of_jobs_listed > 0, "No jobs listed after search\n"
                    print(f"The number of jobs listed, based on the search term, is {num_of_jobs_listed}")
                else:
                    print('No search term could be extracted.\n')

            browser.close()
