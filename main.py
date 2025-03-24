import os
import sys
import logging
from camoufox.sync_api import Camoufox
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

load_dotenv()
login = os.getenv("LOGIN")
pwd = os.getenv("PASSWORD")

if not login or not pwd:
    logger.error("Missing LOGIN or PASSWORD environment variables.")
    sys.exit(1)


def main():

    accounts = []

    def login(page, login, pwd):
        page.goto('https://business.comcast.com/')
        page.click('.sign-in-link')
        page.wait_for_selector('#sign-in-form', timeout=15_000)
        try:
            page.click(".onetrust-close-btn-handler")
        except Exception:
            logger.warning("Cookie banner close button not found or already closed.")
        logger.info("Filling username...")
        page.fill('.bcp-form-content input[name="user"]', login)
        page.click('button[id="sign_in"]')
        logger.info("Filling password...")
        page.wait_for_selector('input[name="passwd"]', timeout=15_000)
        page.fill('input[name="passwd"]', pwd)
        page.click('button[id="sign_in"]')
        page.wait_for_selector('#account-management-heading', timeout=15_000)
        logger.info("Login successful")


    def get_accounts(response):
        nonlocal accounts
        if "ss-service-navigation" in response.url:
            try:
                intercepted_json = response.json()
                accounts = [i.get('key', None) for i in intercepted_json.get('accounts')]
                # logger.info(f'Intercepted accounts: {accounts}')
            except Exception as e:
                pass

    def download_bill(page, account):
        logger.info(f'Processing account: {account}')
        try:
            page.goto(f'https://business.comcast.com/account/dashboard/accounts/{account}')
            page.goto('https://business.comcast.com/account/bill')
            with page.expect_download() as download_info:
                page.click(".bsd-panel .bsd-bill-actions-view-bill")
            download = download_info.value
            filename = account + '_' + download.suggested_filename
            path = os.path.join("output", filename)
            download.save_as(path)
            logger.info(f'Download completed for account: {account}')
            logger.info(f'File saved at: {path}')
        except Exception as e:
            logger.error(f'Error processing account {account}: {e}')


    with Camoufox() as browser:
        page = browser.new_page()
        logger.info('Starting...')
        page.on("response", get_accounts)
        login(page, os.getenv("LOGIN"), os.getenv("PASSWORD"))
        logger.info(f"Total accounts: {len(accounts)}")
        for account in accounts:
            download_bill(page, account)
        logger.info(f'Process completed!')
        logger.info(f'Total number of accounts: {len(accounts)}')
        browser.close()

if __name__ == "__main__":
    main()
