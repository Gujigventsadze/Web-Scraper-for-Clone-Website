import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

chrome_opts = webdriver.ChromeOptions()
chrome_opts.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_opts)

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
html = response.text

soup = BeautifulSoup(html, "html.parser")

house_list = soup.find_all("li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")

houses_array = []

for house in house_list:
    price = house.find("span", class_="PropertyCardWrapper__StyledPriceLine").text.split()[0].replace("/mo", "").replace("+", "")
    address = house.find("a", class_="StyledPropertyCardDataArea-anchor")
    link = address.get("href")
    houses_array.append({
        "price": price,
        "address": address.text.strip(),
        "link": link
    })


def submit_form(price, address, link):
    wait = WebDriverWait(driver, 10)
    address_input = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    address_input.click()
    address_input.send_keys(address)

    price_input = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    price_input.click()
    price_input.send_keys(price)

    link_input = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')))
    link_input.click()
    link_input.send_keys(link)

    submit_btn = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    submit_btn.click()

    submit_again = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')))
    submit_again.click()

driver.get("https://forms.gle/tYbHWdN5jn1YmykP6")
for house in houses_array:
    price = house["price"]
    address = house["address"]
    link = house["link"]
    submit_form(price, address, link)


