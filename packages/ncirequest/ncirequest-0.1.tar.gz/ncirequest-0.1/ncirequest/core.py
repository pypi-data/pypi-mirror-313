import os
import random
import requests
import json
import cloudscraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from seleniumbase import SB
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential

# Environment configuration for cleaner logs
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'

# Instantiate fake user agent
ua = UserAgent()

# Common headers list for random selection
USER_AGENTS = [
    ua.random for _ in range(5)  # Generate 5 random user agents
]

# Requests session for handling requests
session = requests.Session()
scraper = cloudscraper.create_scraper()


# Helper function to get random header
def get_random_header():
    return {
        "User-Agent": random.choice(USER_AGENTS)
    }


# Function to check if a proxy is alive
def check_proxy_alive(proxy):
    proxychecker = "https://httpbin.org/ip"
    try:
        response = requests.get(proxychecker, proxies={"http": proxy, "https": proxy}, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


# Main function to handle the fetching logic
def sync(url, method=None, proxy=None, timeout=10, retry=3):
    available_methods = {
        'requests': fetch_html_with_requests,
        'cloudscraper': fetch_html_with_cloudscraper,
        'selenium': fetch_html_with_selenium,
        'seleniumbase': antibotbypassforselenium,
        'playwright': fetch_html_with_playwright
    }

    # Default to 'requests' if no method is specified
    if method is None:
        method = 'requests'

    method_func = available_methods.get(method)
    if not method_func:
        raise ValueError(f"Invalid method {method} specified.")

    headers = get_random_header()

    try:
        content, status_code = method_func(url, proxy, timeout, retry, headers)
        return handle_output(content, status_code)
    except Exception as e:
        print(f"Error: {e}")
        return None


# Add the timeout and retry logic here
def fetch_html_with_requests(url, proxy, timeout, retry, headers):
    try:
        session.headers.update(headers)
        if proxy and check_proxy_alive(proxy):
            response = session.get(url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
        else:
            response = session.get(url, timeout=timeout)
        return response.text, response.status_code
    except requests.RequestException as e:
        raise Exception(f"Error with requests: {e}")


# Implement other fetch methods (cloudscraper, selenium, etc.)

def fetch_html_with_cloudscraper(url, proxy, timeout, retry, headers):
    scraper.headers.update(headers)
    if proxy and check_proxy_alive(proxy):
        response = scraper.get(url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
    else:
        response = scraper.get(url, timeout=timeout)
    return response.text, response.status_code


def fetch_html_with_selenium(url, proxy, timeout, retry, headers):
    options = Options()
    options.add_argument(f'user-agent={headers["User-Agent"]}')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    return html_content, 200


# Define other fetch functions similarly ...

# Handle different output formats (json, xml, js, etc.)
def handle_output(content, status_code):
    if status_code != 200:
        return f"Failed with status code {status_code}"

    try:
        return {
            'html': content,
            'json': json.dumps(json.loads(content), indent=4),
            'xml': content,  # Convert content to XML if possible
            'js': content,  # Extract JS if necessary
            'statuscode': status_code
        }
    except Exception as e:
        return f"Error processing output: {e}"

