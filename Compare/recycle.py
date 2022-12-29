import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException
from datetime import datetime
import os
from time import sleep
import csv



options1 = webdriver.ChromeOptions()
options1.add_experimental_option('excludeSwitches', ['enable-logging'])
options1.add_argument("window-size=1920x1480")
options1.add_argument("disable-dev-shm-usage")
options1.add_argument("--headless")
driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=options1) 


def price_scrape():
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",scope)
    client = gspread.authorize(creds)
    sheet_name = 'Sheet1'
    spreadsheet_key = '1uSs2uq_VLGusQ6x-fCKsNtDPHxnVeyhXLoW63PjozfE'
    sheet = client.open_by_key(spreadsheet_key)
    
     
    filename = "data.csv"
    with open(filename, 'w', encoding='utf-8', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["PHONE NAME", "SIZE", "NETWORK", "CONDITION", "RECYCLER", "HIGHEST PRICE"])

    urls = ['https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-11',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-11-pro',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-11-pro-max',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-12',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-12-mini',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-12-pro',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-12-pro-max',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-13',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-13-mini',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-13-pro',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-13-pro-max',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-7',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-7-plus',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-8',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-8-plus',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-se',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-se-2020',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-se-2022',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-x',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-xr',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-xs',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-xs-max',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s10',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s10-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s10-lite',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s10-plus',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-6',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-6-plus',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-6s',
            'https://www.compareandrecycle.co.uk/mobile-phones/apple-iphone-6s-plus',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s20',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s20-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s20-plus',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s20-plus-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s21-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s21-fe-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s21-plus-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s21-ultra-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s22-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s22-ultra-5g',
            'https://www.compareandrecycle.co.uk/mobile-phones/samsung-galaxy-s22-plus-5g']


    wait=WebDriverWait(driver,10)
    for url in urls:
        page = driver.execute_script("window.open('{}','_blank');".format(url))
        handles = driver.window_handles
        main_window = driver.current_window_handle
        driver.switch_to.window(handles[-1])
        sleep(5)
            
        try:
            cookie_button = driver.find_element("xpath", "//span[@class='cookie_acceptButton__gs5MX']").click()
        except NoSuchElementException:
            pass
    
        q=1
        while True:
            try:    
                driver.find_element(By.XPATH,f"(//span[contains(@class,'filter-box')] )[{q}]").click()
                
                j=0
                while True:
                    try:
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.network-options > div > div > span"))).click()
                        networks=wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.selectboxit-options.selectboxit-list>li")))
                        networks[j].click()
                        sleep(2)
                        i=0
                        while True:
                            try:
                                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.condition-options > div > div > span"))).click()
                                condition=wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.selectboxit-options.selectboxit-list>li")))
                                condition[i].click()
                                sleep(2)
                                Phone_Name = driver.find_element("xpath","//h2").text
                                size = driver.find_element("xpath",f"(//span[contains(@class,'filter-box')] )[{q}]").text
                                Networks = driver.find_element("xpath", "//div[@class='network-options']//span[@class='selectboxit selectboxit-enabled selectboxit-btn']/span[@class='selectboxit-text']").text
                                Conditions = driver.find_element("xpath", "//div[@class='condition-options']//span[@class='selectboxit selectboxit-enabled selectboxit-btn']/span[@class='selectboxit-text']").text
                                try:
                                    if driver.find_element("xpath","//div[@class='comparison-row '][1]/span/span/img").get_attribute("alt") == "Gr8 Mobile":
                                        Prices = driver.find_element("xpath", "//div[@class='comparison-table']/div[@class='comparison-row '][2]/span[@class='comparison-cell price sort']/div[1]").text.replace("up to", "")
                                        Recyclers = driver.find_element("xpath","//div[@class='comparison-row '][2]/span/span/img").get_attribute("alt")
                                        with open (filename, 'a', encoding='utf-8') as file:
                                            file.write(Phone_Name + "," + size + "," + Networks + "," + Conditions + "," + Recyclers + "," + Prices + "\n")               
                                    else:
                                        Prices = driver.find_element("xpath", "//div[@class='comparison-table']/div[@class='comparison-row '][1]/span[@class='comparison-cell price sort']/div[1]").text.replace("up to", "")
                                        Recyclers = driver.find_element("xpath","//div[@class='comparison-row '][1]/span/span/img").get_attribute("alt")
                                        with open (filename, 'a', encoding='utf-8') as file:
                                            file.write(Phone_Name + "," + size + "," + Networks + "," + Conditions + "," + Recyclers + "," + Prices + "\n")
                                except NoSuchElementException:
                                    with open (filename, 'a', encoding='utf-8') as file:
                                        file.write(Phone_Name + "," + size + "," + Networks + "," + Conditions + "," + "None" + "," + "None" + "\n")
                                    
                                i+=1
                            except:
                                break
                        j+=1
                    except:
                        break
                q+=1
            except:
                break

                                                        
            
        driver.close()
        driver.switch_to.window(main_window)
    sheet.values_clear("Sheet1")    
    sheet.values_update(sheet_name, params={'valueInputOption': 'USER_ENTERED'}, body={'values':list(csv.reader(open(filename)))})       

while True:
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json",scope)
    client = gspread.authorize(creds)
    sheet_name = 'Sheet1'
    spreadsheet_key = '1uSs2uq_VLGusQ6x-fCKsNtDPHxnVeyhXLoW63PjozfE'
    sheet = client.open_by_key(spreadsheet_key)
    
    sheet.values_update('Sheet1!I4', params={'valueInputOption': 'USER_ENTERED'}, body={'values':[["Update in Progress ........."]]} )
    
    price_scrape()
    
    sheet.values_update('Sheet1!I3', params={'valueInputOption': 'USER_ENTERED'}, body={'values':[["Last Update: {}".format(datetime.now())]]})
    
    sleep(3600)