import os
import sys
import random
from lxml import html
from time import sleep
from urllib.parse import quote
from selenium import webdriver
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from yarl import URL


def get_results(code):
    sites = html.fromstring(code).xpath('//h3[@class="r"]/a/@href')
    if len(sites) == 0:
        raise ValueError('no websites in result page')
    return sites


def understand_captcha(url, browser, proxy, UA):
    # Captcha Solving
    api_key = '5d7715dba5393cc85562e9177751bd4e'
    site_key = browser.find_element_by_id('recaptcha').get_attribute('data-sitekey')
    client = AnticaptchaClient(api_key)
    # task = NoCaptchaTask(url, site_key, 'http', proxy.host, proxy.port, UA)
    task = NoCaptchaTaskProxylessTask(url, site_key)
    job = client.createTask(task)
    job.join()
    captcha_result = job.get_solution_response()
    browser.execute_script("document.getElementById('g-recaptcha-response').style.display = '';")
    elem = browser.find_element_by_id('g-recaptcha-response')
    elem.send_keys(captcha_result)
    submit = browser.find_element_by_name('submit')
    submit.click()
    sleep(random.randint(1, 3))
    return browser


def crawler(country='US'):
    '''
    AU,Australia,Sydney,ip
    AU,Australia,,ip
    AU,Australia,Brisbane,ip
    US,United States,Smarr,ip
    US,United States,Las Vegas,ip
    !US,United States,New York,ip
    US,United States,Las Vegas,ip
    US,United States,Saint Louis,ip
    US,United States,Chicago,ip
    GB,United Kingdom,Thornton Heath,ip
    GB,United Kingdom,,ip
    GB,United Kingdom,,ip
    '''

    keys = []

    proxy = {'US': 'http://ip',
             'UK': 'http://ip',
             'AU': 'http://ip',
             'CA': 'http://ip'}

    google = {'US': 'google.com', 'UK': 'google.co.uk', 'AU': 'google.com.au', 'CA': 'google.ca'}

    result_file = f'data/google_sites_result_{country}.txt'
    input_file = f'data/google_input_keys_{country}.txt'
    parsed_file = f'data/google_parsed_keys_{country}.txt'

    with open(parsed_file, 'r', encoding='utf-8') as f1:
        result = f1.read()

    with open(input_file, 'r', encoding='utf-8') as f2:
        for line in f2:
            key = line.strip()
            if key not in result:
                keys.append(key)

    print(len(keys), 'Keys in Queue')

    UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    _options = webdriver.chrome.options.Options()
    _options.add_argument('--headless')
    _options.add_argument('--no-sandbox')
    _options.add_argument('--disable-notifications')
    _options.add_argument(f'--proxy-server={proxy[country]}')
    _driver = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver')
    browser = webdriver.Chrome(chrome_options=_options, executable_path=_driver)

    for k in keys:
        try:
            print('[SEND]', k)
            url = f'https://www.{google[country]}/search?q={quote(k)}&num=100'
            browser.get(url)
            sleep(random.randint(3, 7))
            code = browser.page_source
            if 'recaptcha' in code:
                browser = understand_captcha(url, browser, proxy, UA)
                code = browser.page_source
            sites = get_results(code)
            with open(result_file, 'a', encoding='utf-8') as result:
                for s in sites:
                    # result.write('{}\t{}\n'.format(k, s))
                    result.write(f'{URL(s).host}\n')
            with open(parsed_file, 'a', encoding='utf-8') as parsed:
                parsed.write(f'{k}\n')
            print('[OK]', k)
            sleep(random.randint(2, 8))
        except Exception as e:
            print(type(e), e, 'line: ', sys.exc_info()[-1].tb_lineno)
            browser.quit()
            browser = webdriver.Chrome(chrome_options=_options, executable_path=_driver)
    browser.quit()


def main():
    countries = ['US', 'UK', 'AU', 'CA']
    for c in countries:
        crawler(c)


if __name__ == '__main__':
    main()
