from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver=webdriver.Chrome(options=chrome_options)
driver.get("https://books.toscrape.com/catalogue/page-1.html")
WebDriverWait(driver=driver,timeout=2).until(lambda _:driver.find_element(By.CSS_SELECTOR,value="li.col-xs-6.col-sm-4.col-md-3.col-lg-3"))
store=[]
nxt=True
Page_num=1
while nxt:
    try:
        data=driver.find_elements(By.CSS_SELECTOR,value="li.col-xs-6.col-sm-4.col-md-3.col-lg-3")
        itterate=0
        data2=[i.text for i in data]
        for i in data2:
            strings=i.split("\n")
            title=strings[0]
            price=float(strings[1].replace("£",""))
            condition=strings[2]
            rating=data[itterate].find_element(By.CLASS_NAME,value="star-rating").get_attribute("class")
            rating=rating.removeprefix("star-rating ")
            image=data[itterate].find_element(By.CSS_SELECTOR,value="img").get_attribute("src")
            book={"No.":f"{Page_num}",
                "Title":title,
                "Price":f"£{price}",
                "Condition":condition,
                "Rating":f"{rating}/Five",
                "image":image}
            store.append(book)
            itterate+=1
            Page_num+=1
    except NoSuchElementException:
        print("Data couldn't be extracker :(")
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,value="li.next a")
        next_page.click()
    except NoSuchElementException:
        if store:
            print(f"Data extraction complete.\nBooks Extracted:{len(store)}")
        else:
            print("Data extraction failed")
        nxt=False
with open("data.json","w")as file:
    json.dump(store,file)
driver.quit()
