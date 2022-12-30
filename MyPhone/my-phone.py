import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import os
import csv
from time import sleep

def price_scrape():
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name("sell-cell.json",scope)
    client = gspread.authorize(creds)
    sheet_name = 'Sheet1'
    spreadsheet_key = 'Key Here'
    sheet = client.open_by_key(spreadsheet_key)
    
    filename = "data2.csv"
    with open(filename, 'w', encoding='utf-8', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["PHONE NAME", "SIZE", "NETWORK", "CONDITION", "RECYCLER", "HIGHEST PRICE"])


    options1 = webdriver.ChromeOptions()
    # options1.add_argument('--start-maximized')
    options1.add_experimental_option('excludeSwitches', ['enable-logging'])
    options1.add_argument("window-size=1920x1480")
    options1.add_argument("disable-dev-shm-usage")
    options1.add_argument("--headless")
    driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=options1)
    
    urls = ["links here"]  #place links here 

    wait=WebDriverWait(driver,10)
    for url in urls:
        r = requests.get(url)
        soup = bs(r.text, 'html.parser')
        dom = etree.HTML(str(soup))
        
        links = dom.xpath("//div[@class='select-model-device-form']/div[1]/div[@class='select-options']//a")
        for link in links:
            Condition_link = link.xpath(".//@href")
            condition_text = link.xpath(".//text()")
            
            for l in Condition_link:
                new_req = requests.get(l)
                soup2 = bs(new_req.text, 'html.parser')
                dom = etree.HTML(str(soup2))
            
                links_2 = dom.xpath("//div[@class='select-model-device-form']/div[2]/div[@class='select-options']/div/a")
                for link2 in links_2:
                    capacity_link = link2.xpath(".//@href")
                    capacity_text = link2.xpath(".//text()")
                    
                    for k in capacity_link:
                        page = driver.execute_script("window.open('{}','_blank');".format(k))
                        handles = driver.window_handles
                        main_window = driver.current_window_handle
                        driver.switch_to.window(handles[-1])
                        sleep(5)
                        
                        phone = driver.find_element("xpath", "//div[@class='heading']/h1").text    
                        dropdown = Select(driver.find_element("xpath","//select"))
                        for opt in dropdown.options:
                            opt.click()
                            options = opt.text
                            sleep(3)
                            name = phone.strip().split(" ")[:-1]
                            phone_name =' '.join(name)
                            sizes = ' '.join([str(size) for size in capacity_text])
                            conditions = ' '.join([str(condition) for condition in condition_text])
                            try:
                                if driver.find_element("xpath", "//table/tbody/tr[2]/td/a/img").get_attribute("alt") == "Gr8 Mobile":
                                    price = wait.until(EC.visibility_of_element_located((By.XPATH,"//table/tbody/tr[3]/td[2]")))
                                    recycle = wait.until(EC.visibility_of_element_located((By.XPATH,"//table/tbody/tr[3]/td/a/img")))
                                else:
                                    price = wait.until(EC.visibility_of_element_located((By.XPATH,"//table/tbody/tr[2]/td[2]")))
                                    recycle = wait.until(EC.visibility_of_element_located((By.XPATH,"//table/tbody/tr[2]/td/a/img")))
                                with open (filename, 'a', encoding='utf-8') as file:
                                    file.write(phone_name.replace("Sell","").replace("My","").replace("New","").replace("Broken","") + "," + sizes + "," + options + "," + conditions + "," + recycle.get_attribute('alt') + "," + price.text + "\n")
                            except:
                                with open (filename, 'a', encoding='utf-8') as file:
                                    file.write(phone_name.replace("Sell","").replace("My","").replace("New","").replace("Broken","") + "," + sizes + "," + options + "," + conditions + "," + "None" + "," + "None" + "\n")
                                    
                            
                        driver.close()
                        driver.switch_to.window(main_window)
                        
                        
    sheet.values_clear("Sheet1")    
    sheet.values_update(sheet_name, params={'valueInputOption': 'USER_ENTERED'}, body={'values':list(csv.reader(open(filename)))}) 
    

while True:
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name("sell-cell.json",scope)
    client = gspread.authorize(creds)
    sheet_name = 'Sheet1'
    spreadsheet_key = 'Key Here'
    sheet = client.open_by_key(spreadsheet_key)
    sheet.values_update('Sheet1!I4', params={'valueInputOption': 'USER_ENTERED'}, body={'values':[["Update in Progress ........."]]} )
    
    price_scrape()
    
    sheet.values_update('Sheet1!I3', params={'valueInputOption': 'USER_ENTERED'}, body={'values':[["Last Update: {}".format(datetime.now())]]})
    
    sleep(3600)
