from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pyquery import PyQuery as pq

def get_b64(art_hash):
    browser = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])
    browser.set_window_size(1400, 900)
    wait = WebDriverWait(browser, 10)

    browser.get('http://www.viidii.info/?http://www______rmdown______com/link______php?hash={}'.format(art_hash))

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=hidden]'))
    )

    html = browser.page_source
    doc = pq(html)
    b64 = doc.find('input[type=hidden]').attr('value')
    return b64