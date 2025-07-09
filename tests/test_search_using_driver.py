'''
This test goes to each url in the *.txt file, input "driver" in the search box
and then prints out how many driver jobs were in the search result; or no driver
jobs were found in the search result. Example: Found 20 jobs for https://fusionsite.stratasjobs.com
or https://blanchardcat.stratasjobs.com didn't have any listed jobs.
'''


import pytest
from pathlib import Path
from playwright.sync_api import Playwright, expect, sync_playwright
import time

url_file_path = Path(__file__).parent/"reach_jobs_domain.txt"
with open(url_file_path, "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

@pytest.mark.parametrize("url", urls)
def test_driver_search_on_job_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--start-maximized"])
        context = browser.new_context()
        page = context.new_page()

        response = page.goto(url, wait_until="domcontentloaded")
        assert response is not None, f"No response received for {url}"
        assert response.status == 200, f"Unexpected status code for {url}: {response.status}"

        job_search_box = page.locator("#job-search")
        if job_search_box.count() > 0:
            job_search_box.fill("driver")
            time.sleep(5)
            page.click("#submit-search")
            time.sleep(5)

            job_links = page.locator("#job-listings-wrapper").locator("a")
            num_of_jobs = job_links.count()
            if num_of_jobs > 0:
                print(f"Found {num_of_jobs} jobs for {url}\n")
            else:
                expect(page.locator("#job-listings-wrapper")).to_contain_text("No jobs match your search criteria.")
                print(f"{url} didn't have any listed jobs.\n")

        else:
            print(f"{url} doesn't have any search option.\n")

        context.close()
        browser.close()
