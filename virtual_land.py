import requests
import random
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import string


## selenium for hospital page
starturl = "https://nonfungible.com/market/history/decentraland?filter=nftTicker%3DLAND&filter=saleType%3D&length=100&sort=blockTimestamp%3Ddesc&start=0"

driver = webdriver.Chrome(r'C:\Users\chengkun\chromedriver.exe')  # change the driver's directory here
driver.get(starturl)
# driver.find_element_by_xpath("//select[@aria-label='rows per page']/option[text()='50 rows']").click()
result = []
count = 0
# count is the amoutn of pages you are going through
while count < 1:  # set this yourself: this number is the returned 
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.rt-tr-group div.rt-td")))
    for my_ele in element:
        result.append(my_ele.text)
    sleeptime = random.uniform(2, 4)
    time.sleep(sleeptime)
    button = driver.find_element_by_xpath('//button[contains(text(), "Next")]')
    driver.execute_script("arguments[0].click();", button)

    count += 1

print(result)
print(count)


# Index has to start from index = 1, because in the returned result[]: second item is the land reference number, and it occurs every 8 elements (8 itmes each line on the website)
index = 1
# queried is a dictionary to store a structure: land reference -> properties.
queried = {}
# grouped is the final outcome of what we want to put inside the csv file.
grouped = []


while index < 800: # set this yourself: this number is number of parcels TIMES 8 (because the land reference number occurs every 8 elements)
    
    # check if this parcel has already been queried. if not, query it; else, 
    if result[index] not in queried:
        # double checked if this is right
        xhr = 'https://api.decentraland.org/v2/tiles/{}'
        r = requests.get(xhr.format(result[index]))
        if r.status_code != 200:
            print('Boo!')
            break
        # properties is whatever 
        properties = json.loads(r.text)
        print(properties)
        queried[result[index]] = properties
    else:
        properties = queried[result[index]]
    grouped.append([result[index], result[index + 4], result[index + 5], result[index + 6]], properties['data']['x'], properties['data']['y'], properties)
    index += 8
    sleeptime = random.uniform(2, 4)
    time.sleep(sleeptime)
    # if (index - 1) % 50 == 0:
    #     print('finish', index)

print('finished number of parcels', index % 8)

df = pd.DataFrame(grouped, columns=['asset_id', 'price', 'token_price', 'sale date', 'x', 'y', 'asset_properties'])
df.to_csv('virtual_land1.csv', index=False, header=True)
print(df)