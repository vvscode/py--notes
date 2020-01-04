from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def get_browser():
  chrome_options = ChromeOptions()
  chrome_options.add_argument("--headless")
  browser_instance = webdriver.Chrome(options=chrome_options)
  return browser_instance

def get_google_results(keyword, results):
  browser = get_browser()
  browser.get(f'https://www.google.com/search?q={keyword}')
  links = list(map(lambda el: el.get_attribute('href'), browser.find_elements_by_css_selector('.srg .r a')))
  results.extend(links)

def get_bing_results(keyword, results):
  browser = get_browser()
  browser.get(f'https://www.bing.com/search?q={keyword}')
  links = list(map(lambda el: el.get_attribute('innerHTML'), browser.find_elements_by_css_selector('#b_results .b_attribution cite')))
  results.extend(links)

if __name__ == '__main__':
  keyword = input('Eneter keyword: ').strip()

  bing_results = []
  bing_tread = Thread(target=get_bing_results, args=[keyword, bing_results])
  bing_tread.start()

  google_results = []
  google_tread = Thread(target=get_google_results, args=[keyword, google_results])
  google_tread.start()

  bing_tread.join()
  google_tread.join()

  print('Bing results:')
  print('\n'.join(bing_results))

  print('Googe results:')
  print('\n'.join(google_results))

  with open(f'{keyword}_results.txt', 'w') as fp:
    fp.write('Bing:\n')
    fp.write('\n'.join(bing_results))

    fp.write('\n\n')

    fp.write('Google:\n')
    fp.write('\n'.join(google_results))