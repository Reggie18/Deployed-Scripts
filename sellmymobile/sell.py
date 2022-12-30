import gspread
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.support.ui import Select
from datetime import datetime
import csv
from time import sleep

def price_scrape():
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name("sell-my-phone-credentials.json",scope)
    client = gspread.authorize(creds)
    spreadsheet_key = 'Key Here'
    sheet = client.open("Sell My Mobile").sheet1
    
    
    options1 = webdriver.ChromeOptions()
    # options1.add_argument('--start-maximized')
    options1.add_experimental_option('excludeSwitches', ['enable-logging'])
    options1.add_argument("window-size=1920x1480")
    options1.add_argument("disable-dev-shm-usage")
    options1.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options1)
    
    filename = "data.csv"
    with open(filename, 'w', encoding='utf-8', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["PHONE NAME", "SIZE", "NETWORK", "CONDITION", "RECYCLER", "HIGHEST PRICE"])
    
    urls = ["links here"]  #place links here

    wait=WebDriverWait(driver,10)
    for url in urls:
        page = driver.execute_script("window.open('{}','_blank');".format(url))
        handles = driver.window_handles
        main_window = driver.current_window_handle
        driver.switch_to.window(handles[-1])
        sleep(5)
            
        try:
            wait=WebDriverWait(driver,5)
            cookies = wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@class='cookie-policy-panel__accept-button cta cta--primary']")))
            cookies.click()
        except TimeoutException:
            pass
        for elem in driver.find_elements("xpath","//ul[@class='results-filter__conditions flexbox flexbox--center']/li"):
            condition = elem.text
            elem.click()
            sleep(2)
            dropdown = Select(driver.find_element("xpath","//label[@class='dtl-dropdown dtl-dropdown--results-networks']/select"))
            for opt in dropdown.options:
                opt.click()
                options = opt.text
                sleep(2)
                name = driver.find_element("xpath", "//h1[@class='results-header__title']").text
                names = name.strip().split(" ")[:-1]
                name_s = ' '.join(names)
                size = name.strip().split(" ")[-1:]
                size_s = ' '.join(size)
                try:
                    if driver.find_element("xpath", "//table/tbody/tr/td/img").get_attribute("alt") == str('Gr8 Mobile'):
                        price = driver.find_element("xpath", "//tbody[2]/tr/td[@class='device-results-table__cell device-results-table__cell--price']").text
                        recycler = driver.find_element("xpath", "//table/tbody[2]/tr/td/img").get_attribute("alt")
                    else:
                        price = driver.find_element("xpath", "//tbody[1]/tr/td[@class='device-results-table__cell device-results-table__cell--price']").text
                        recycler = driver.find_element("xpath", "//table/tbody/tr/td/img").get_attribute("alt")
                    with open (filename, 'a', encoding='utf-8') as file:
                            file.write(name_s + "," + size_s + "," + options + "," + condition + "," + recycler + "," + price + "\n")
                except:
                    with open (filename, 'a', encoding='utf-8') as file:
                        file.write(name_s + "," + size_s + "," + options + "," + condition + "," + "None" + "," + "None" + "\n")
                    
            
        driver.close()
        driver.switch_to.window(main_window)
    df = pd.read_csv('data.csv')
    
    df3 = pd.DataFrame(df)
    
    df3["PHONE NAME"] = df3["PHONE NAME"].astype(str).str.replace("Sell", "", regex=True)
    df3["PHONE NAME"] = df3["PHONE NAME"].astype(str).str.replace("'", "", regex=True)
    df3["PHONE NAME"] = df3["PHONE NAME"].astype(str).str.replace("[", "", regex=True)
    df3["PHONE NAME"] = df3["PHONE NAME"].astype(str).str.replace("]", "", regex=True)
    df3["PHONE NAME"] = df3["PHONE NAME"].astype(str).str.replace(",", " ", regex=True)
    
    df3["SIZE"] = df3["SIZE"].astype(str).str.replace("'", "", regex=True)
    df3["SIZE"] = df3["SIZE"].astype(str).str.replace("[", "", regex=True)
    df3["SIZE"] = df3["SIZE"].astype(str).str.replace("]", "", regex=True)
    
    
        
    Worksheet = 'sheet1'
    cell_to_start = 'A1'
    d2g.upload(
        df3,
        spreadsheet_key,
        credentials = creds,
        col_names = True,
        row_names = False,
        start_cell = cell_to_start,
        clean = True)

while True:
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name("sell-my-phone-credentials.json",scope)
    client = gspread.authorize(creds)
    spreadsheet_key = 'Key Here'
    sheet = client.open("Sell My Mobile").sheet1
    sheet.update_cell(3,9, "Update in Progress .......")
    
    price_scrape()
    
    sheet.update_cell(2,9, "Last Update: {}".format(datetime.now()))
    
    sleep(3600)
