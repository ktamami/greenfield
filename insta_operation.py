import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
load_dotenv()

driver_path = '/app/.chromedriver/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
#※headlessにしている
driver = webdriver.Chrome(options=options, executable_path=driver_path)

insta_url = "https://www.instagram.com/"
insta_id = os.environ.get("INSTA_ID")
insta_pass = os.environ.get("INSTA_PASS")
target_account = os.environ.get("INSTA_TARGET")


class InstaOperation:
    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=path)

    def login(self):
        self.driver.get(insta_url)
        time.sleep(2)
        self.driver.find_element_by_name("username").send_keys(insta_id, Keys.TAB, insta_pass, Keys.TAB, Keys.TAB, Keys.ENTER)
        time.sleep(2)

    def find_target(self):
        self.driver.get(insta_url + target_account)
        time.sleep(2)

    def get_latest_post(self):
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div/div[2]/div/div[1]/div/div/button').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div/button[6]').click()
        time.sleep(2)
        code = self.driver.find_element_by_xpath('/html/body/div[7]/div/div/div/textarea').text
        return code

    def overlay_code(self, latest_code):
        with open("static/insta.txt", mode="r") as file:
            previous_code = file.read()
        if latest_code != previous_code:
            with open("static/insta.txt", mode="w") as file:
                file.write(latest_code)


    def quit(self):
        self.driver.quit()

