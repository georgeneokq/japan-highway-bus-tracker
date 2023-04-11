from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from sys import exit
from datetime import datetime
from playsound import playsound

WEBSITE_URL = 'https://www.highwaybus.com/gp/info/serviceInfo'
DATE = '20221225'  # YYYYMMDD
SEARCH_KEYWORDS = ['金沢', '名古屋']

def main():
  chrome_options = Options()
  chrome_options.headless = False
  chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
  service = Service(executable_path=ChromeDriverManager().install())
  browser = webdriver.Chrome(service=service, options=chrome_options)
  browser.maximize_window()

  is_initial = True
  initial_option_count = 0
  initial_time = ''

  while True:
    browser.get(WEBSITE_URL)

    # Change date
    datepicker_element = browser.find_element(By.CSS_SELECTOR, 'input[type=text].hasDatepicker')
    datepicker_element.clear()
    datepicker_element.send_keys(DATE)
    datepicker_element.send_keys(Keys.ENTER)

    # Wait for options to load
    sleep(3)
    option_elements = browser.find_elements(By.CSS_SELECTOR, '#lineId option')

    # Get current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # Set initial statistics
    if is_initial:
      initial_option_count = len(option_elements)
      initial_time = current_time
      is_initial = False

    # Statistic: Number of routes increased since first check
    routes_increased = len(option_elements) - initial_option_count

    # Print setup/statistics
    print('')
    print(f'通知キーワード：{", ".join(SEARCH_KEYWORDS)}')
    print(f'{current_time}更新')
    if routes_increased > 0:
      print(f'{initial_time}から更に{routes_increased}つのルートのバスが運休になりました')

    # Print options and check if alarm should ring
    for option_element in option_elements:
      print(option_element.text)

      all_keywords_found = False
      for i, keyword in enumerate(SEARCH_KEYWORDS):
        if keyword not in option_element.text:
          break
        if i == len(SEARCH_KEYWORDS) - 1:
          all_keywords_found = True

      if all_keywords_found:
        notify(option_element.text)
        break

    sleep(3)

def notify(option_text):
  print(f'FOUND: {option_text}')
  try:
    playsound('sounds/alarm.mp3')
  except KeyboardInterrupt:
    exit()

if __name__ == '__main__':
  main()