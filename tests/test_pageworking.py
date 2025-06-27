
import pytest
from pathlib import Path
from playwright.sync_api import Playwright, expect, sync_playwright
import time

url_file_path = Path(__file__).parent/"reach_jobs_domain.txt"
with open(url_file_path, "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

@pytest.mark.parametrize("url", urls)
def test_pageworking(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,args=["--start-maximized"])
        context = browser.new_context()
        page = context.new_page()

        response = page.goto(url, wait_until="domcontentloaded")
        assert response is not None, f"No response received for {url}"
        assert response.status == 200, f"Unexpected response for {url}. Received response is {response.status}"

        context.close()
        browser.close()