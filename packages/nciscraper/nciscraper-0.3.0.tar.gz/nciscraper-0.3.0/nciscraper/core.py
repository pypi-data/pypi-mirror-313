import os
import random
import requests
import json
import cloudscraper
from seleniumbase import SB
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_exponential

os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'

ua = UserAgent()

USER_AGENTS = [
    ua.random for _ in range(5)
]

session = requests.Session()
scraper = cloudscraper.create_scraper()


def get_random_header():
    return {
        "User-Agent": random.choice(USER_AGENTS)
    }


def check_proxy_alive(proxy):
    proxychecker = "https://httpbin.org/ip"
    try:
        response = requests.get(proxychecker, proxies={"http": proxy, "https": proxy}, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False


def fetch_html_with_requests(url, proxy, timeout, retry, headers):
    try:
        session.headers.update(headers)
        if proxy and check_proxy_alive(proxy):
            response = session.get(url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
        else:
            response = session.get(url, timeout=timeout)
        return response.text, response.status_code
    except requests.RequestException as e:
        print(f"Error fetching the page with requests: {e}")
        raise


def fetch_html_with_cloudscraper(url, proxy, timeout, retry, headers):
    scraper.headers.update(headers)
    if proxy and check_proxy_alive(proxy):
        response = scraper.get(url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
    else:
        response = scraper.get(url, timeout=timeout)
    return response.text, response.status_code


def fetch_html_with_selenium(url, proxy=None, timeout=10, retry=3, headers=None):
    driver = None
    headers = get_random_header()
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f'--user-agent={headers["User-Agent"]}')
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        html_content = driver.page_source
        return html_content, 200
    except Exception as e:
        return None, 500
    finally:
        if driver:
            driver.quit()

def antibotbypassforselenium(url, proxy=None, timeout=10, retry=3, headers=None):
    options = Options()
    options.add_argument("--headless")  # Ensure headless mode is enabled
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent automation detection
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging on port 9222
    if headers and "User-Agent" in headers:
        options.add_argument(f"user-agent={headers['User-Agent']}")
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    try:
        # Initialize SeleniumBase
        with SB(uc=True, headless=True) as sb:
            sb.driver.set_window_size(1920, 1080)  # Set a default window size
            sb.driver.set_page_load_timeout(timeout)  # Set a timeout for page loads
            sb.open(url)
            sb.sleep(timeout)  # Allow time for elements to load
            if sb.is_element_visible(".captcha-image"):
                print("Captcha detected!")
                try:
                    sb.uc_open_with_reconnect(url, retry)  # Retry mechanism
                    sb.uc_gui_click_captcha()  # Attempt to click CAPTCHA button
                    sb.uc_gui_handle_captcha()  # Handle CAPTCHA manually or integrate solver
                    print("Manual CAPTCHA solving required or integrate CAPTCHA-solving service here.")
                except Exception as e:
                    print(f"Error solving CAPTCHA: {e}")
                    print("Skipping CAPTCHA handling for now.")
            else:
                print("No CAPTCHA found, skipping CAPTCHA solving.")
            try:
                sb.remove_elements(".ad-banner")  # Remove ad banners if present
                sb.remove_elements("div.chat-widget")  # Remove any chat widgets if found
            except Exception as e:
                print(f"Error removing elements: {e}")
            return sb.get_page_source(), 200
    except Exception as e:
        print(f"Error fetching page with SeleniumBase: {e}")
        return None, 500


def fetch_html_with_playwright(url, proxy, timeout, retry, headers):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            if proxy:
                context.set_proxy(server=proxy)
            page = context.new_page()
            page.goto(url, timeout=timeout * 1000)
            page.wait_for_load_state("domcontentloaded")
            html_content = page.content()
            browser.close()
            return html_content, 200
    except Exception as e:
        print(f"Error fetching page with Playwright: {e}")
        raise


def handle_output(content, status_code):
    if status_code != 200:
        return {"error": f"Failed with status code {status_code}"}

    try:

        try:
            json_content = json.dumps(json.loads(content), indent=4)
        except json.JSONDecodeError:
            json_content = None

        return {
            'html': content,
            'json': json_content if json_content else "Not valid JSON",
            'xml': content,
            'js': content,
            'statuscode': status_code,
            'sourcecode': content
        }

    except Exception as e:
        return {"error": f"Error processing output: {e}"}


def sync(url, method=None, proxy=None, timeout=10, retry=3):
    available_methods = {
        'requests': fetch_html_with_requests,
        'cloudscraper': fetch_html_with_cloudscraper,
        'selenium': fetch_html_with_selenium,
        'seleniumbase': antibotbypassforselenium,
        'playwright': fetch_html_with_playwright
    }

    methods_to_try = list(available_methods.values())

    if method and method in available_methods:
        methods_to_try = [available_methods[method]]

    headers = get_random_header()

    for method_func in methods_to_try:
        try:
            content, status_code = method_func(url, proxy, timeout, retry, headers)
            if status_code == 200:
                print(f"Success from: {method_func.__name__}")
                return handle_output(content, status_code)
        except Exception as e:
            print(f"Error using method {method_func.__name__}: {e}. Trying next method...")

    print("All methods failed.")
    return {"error": "All methods failed."}
