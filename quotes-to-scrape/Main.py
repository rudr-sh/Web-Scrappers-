from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import json
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver=webdriver.Chrome(options=chrome_options)
driver.get(f"https://quotes.toscrape.com/page/1/")
button=True
quotes=[]
quote={}
print("Getting data...")
while button:
    try:
        data=driver.find_elements(By.CSS_SELECTOR,value=".quote")
        data=[i.text.replace('(about)','') for i in data]    
        for new_quote in data:
            line =new_quote.split('“')[1].split('”')[0]
            quote["Quote"]=line
            Author=new_quote.split("\nby ")[1].split(" \nTags:")[0]
            quote["Author"]=Author.strip()
            try:
                tag=new_quote.split("\nTags: ")[1]
            except IndexError:
                tag=""
            quote["Tags"]=tag
            quotes.append(quote)
            quote={}
    except NoSuchElementException:
        print("No such element was found.")
    try:
        next_page=driver.find_element(By.CSS_SELECTOR,value=".next a")
        next_page.click()
        sleep(2)
    except NoSuchElementException:
        if quotes:
            print("The scrapping is done.")
        else:
            print("The scraping failed try again.")
        button=False
driver.quit()
with open('quotes.json',"w") as file:
    json.dump(quotes,file)
