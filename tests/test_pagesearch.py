'''
This test takes each url from the *.txt file. It thennavigates to the URL,
and takes the first job that it is listed. It then searches by that job,
and return how many such jobs were found. Through this proces, it is
testing the page and also the search function.
'''

import pytest
from playwright.sync_api import Playwright, expect, sync_playwright
from pathlib import Path
import time

url_file_path = Path(__file__).parent/"reach_jobs_domain.txt"
with open(url_file_path, "r",encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

@pytest.mark.parametrize("url",urls)
def test_pagesearch(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=["--start-maximized"])
        context = browser.new_context()
        page = context.new_page()
        page.goto(url,wait_until="domcontentloaded")

        if not page.locator('#job-listings-wrapper').is_visible():
            print(f"Job Listing Wrapper not visible for {url}.\n")
        else:
            job_listing_wrapper = page.locator('#job-listings-wrapper')
            text = job_listing_wrapper.inner_text()
            nojobtext1 = 'No jobs match your search criteria. Please try a different search.'
            nojobtext2 = 'No jobs match your search criteria. Getting suggested jobs.'

            if nojobtext1 in text or nojobtext2 in text:
                print(f"No jobs are found for {url}.\n")
            else:
                page.wait_for_selector('#job-listings-wrapper .listing h3.listing-title', timeout=50000)
                search_term_locator = page.locator('#job-listings-wrapper .listing h3.listing-title').first
                raw_search_term = search_term_locator.text_content()
                search_term_with_dash = raw_search_term.strip() if raw_search_term else ''
                search_term = search_term_with_dash.split(" - ")[0]
                print(f"[{search_term}] {url}")

                if len(search_term) > 0:
                    page.locator("#job-search").fill(search_term)
                    time.sleep(5)
                    page.click("#submit-search")
                    time.sleep(9)

                    job_listings = page.locator('#job-listings-wrapper .listing')
                    num_of_jobs_listed = job_listings.count()

                    assert num_of_jobs_listed > 0, f"Expected jobs for search term '{search_term}' on {url}, but found none."
                    print(f"The number of jobs listed, based on the search term, is {num_of_jobs_listed}")
                else:
                    print('No search term could be extracted.')

        context.close()
        browser.close()



