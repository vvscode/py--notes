import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def translate(text, target_language):
  browser_instance = None
  try:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  

    browser_instance = webdriver.Chrome(options=chrome_options)
    url = f'https://www.bing.com/translator?from=auto&to={target_language}&text={text}'
    browser_instance.get(url)
    time.sleep(1)
    return browser_instance.execute_script("return document.querySelector('#tta_output_ta').value;");
  except Exception as ex:
    print('Something went wrong: ', ex)
  finally:
    if browser_instance:
      browser_instance.quit()

if __name__ == '__main__':
  text_to_translate = 'Hello, World'
  target_language = 'de'
  translated_text = translate(text_to_translate, target_language)
  message = f'Translation for `{text_to_translate}` to `{target_language}` language is `{translated_text}`'
  print(message)
  with open('translations.txt', 'a') as fp:
    fp.write(f'{message}\n')