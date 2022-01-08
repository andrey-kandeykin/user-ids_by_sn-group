from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import random
import pickle
from auth_data import username, password, code
from bs4 import BeautifulSoup
import re
import csv


service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-notifications')

driver = webdriver.Chrome(
    service=service,
    options=options
)


def xpath_exists(url):
    try:
        driver.find_element(By.XPATH, url)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist

# login and come to group user list
def login(username, password, code):

    try:
        # there are firs sign in facebook and get cookie for next logins

        #     driver.get('https://facebook.com/login/')
        #     time.sleep(random.randrange(10, 15))
        #
        #     username_input = driver.find_element(By.ID, 'email')
        #     username_input.clear()
        #     username_input.send_keys(username)
        #
        #     password_input = driver.find_element(By.ID, 'pass')
        #     password_input.clear()
        #     password_input.send_keys(password)
        #     time.sleep(3)
        #
        #     login_button = driver.find_element(By.ID, 'loginbutton')
        #     login_button.click()
        #
        #     time.sleep(5)
        #     code_input = driver.find_element(By.ID, 'approvals_code')
        #     code_input.send_keys(code)
        #
        #     time.sleep(2)
        #     checkpoint_submit_button = driver.find_element(By.ID, 'checkpointSubmitButton')
        #     checkpoint_submit_button.click()
        #     pickle.dump(driver.get_cookies(), open(f'{username}_cookies', 'wb'))


        # group for parsing user ids: https://www.facebook.com/groups/2881801751903646


        driver.get('https://facebook.com/')

        for cookie in pickle.load(open(f'{username}_cookies', 'rb')):
            driver.add_cookie(cookie)

        time.sleep(2)
        driver.refresh()
        time.sleep(4)
        time.sleep(2)
        driver.get('https://www.facebook.com/groups/2881801751903646/members')



    except Exception as e:
        print(e)

# scroll to down page for get whole users list
def scroll():
    # scroll
    last_height = driver.execute_script('return document.body.scrollHeight')
    print('скроллим в конец страницы')

    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(random.randrange(3, 4))
        new_height = driver.execute_script('return document.body.scrollHeight')

        if new_height == last_height:
            print('scroll end')
            break
        last_height = new_height


    time.sleep(4)

# parse and save html, write user_id in csv file
def parser():
    html = driver.page_source

    with open('index.html', 'w', encoding="UTF-8-sig") as file:
        file.write(html)

    with open('index.html', 'r', encoding="UTF-8-sig") as file:
        html = file.read()

    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('a')


    urls = []
    for tag in tags:
        href = str(tag.get('href'))
        url = ''.join(re.findall(r'user/\d+/', href)).strip('user/')
        if url and url not in urls:
            urls.append(url)

    with open('users_id.csv', 'a', encoding='UTF-8-sig') as file:
        writer = csv.writer(file, delimiter=";", lineterminator='\n')
        for url in urls:
            writer.writerow([url])


if __name__ == '__main__':
    login(username, password, code)
    scroll()
    parser()
    driver.quit()
