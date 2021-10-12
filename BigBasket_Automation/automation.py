
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait , Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

deriver_path ="/home/kirito/Documents/webScrapping/Selenium/chromedriver_linux64/chromedriver"

driver = webdriver.Chrome(deriver_path)
driver.implicitly_wait(10)
driver.get("https://www.bigbasket.com/")
dropdown_element = driver.find_element_by_id("navBarMegaNav")
dropdown_list = dropdown_element.find_elements_by_tag_name("a")
a = driver.f
# dropdown_element.click()


for list in dropdown_list:
    print(list.get_attribute("innerText"))

