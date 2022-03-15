# -*- coding: utf-8 -*-
"""
Example command: python twitter_follower_scraper.py
"""
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager


def is_valid_url(url: str) -> bool:
    """Checks whether a URL is valid or not
    Args:
        url (str): the URL to be checked
    Returns:
        bool: True if the URL is valid and False otherwise
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def scrape_twitter_follower(url: str):
    """Scrapes the number of followers of a specific account on Twitter
    Args:
        url (str): the URL of the Twitter account
    Returns:
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--remote-debugging-port=9225')

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(url)
    scrape_option = {
        'by': webdriver.common.by.By.XPATH,
        'value': '//a[contains(@href, "/followers")]'
    }
    browser.implicitly_wait(20)
    try:
        follower_count_el = browser.find_element(**scrape_option)
    except NoSuchElementException as ex:
        print('Cannot extract the follower data of the Twitter account: %s' % ex.msg)
        raise ex
    follower_count = follower_count_el.text
    browser.close()
    print(f'The Twitter account has {follower_count}')


if __name__ == '__main__':
    twitter_account = input('URL of the Twitter account: ')
    if is_valid_url(twitter_account):
        try:
            scrape_twitter_follower(twitter_account)
        except NoSuchElementException:
            print('Please input a valid Twitter account and try again!')
        sys.exit()
    print('Please input a valid url!')
