import requests
import random
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import json


## selenium for hospital page
starturl = "https://nonfungible.com/market/history/decentraland?filter=nftTicker%3DLAND&filter=saleType%3D&length=100&sort=blockTimestamp%3Ddesc&start=0"

driver = webdriver.Chrome(r'C:\Users\chengkun\chromedriver.exe')  # change the driver's directory here
driver.get(starturl)
# driver.find_element_by_xpath("//select[@aria-label='rows per page']/option[text()='50 rows']").click()
result = []
count = 0
while count < 1:  # set
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.rt-tr-group div.rt-td")))
    for my_ele in element:
        result.append(my_ele.text)
    sleeptime = random.uniform(4, 6)
    time.sleep(sleeptime)
    button = driver.find_element_by_xpath('//button[contains(text(), "Next")]')
    driver.execute_script("arguments[0].click();", button)

    count += 1

print(result)
print(count)


# has to start from index = 1
index = 1
grouped = []
queried = {}

while index < 50:
    if result[index] not in queried:
        # double check if this is right
        r = requests.get('https://api.decentraland.org/v1/parcels/{}'.format(result[index]))
        if r.status_code != 200:
            print('Boo!')
            break
        properties = json.loads(r.text)
        print(properties)
        queried[result[index]] = properties
    else:
        properties = queried[result[index]]
    grouped.append([result[index], result[index + 4], result[index + 5], result[index + 6]] + [properties['data']['x'],
                                                                                               properties['data']['y'],
                                                                                               properties])
    index += 8
    sleeptime = random.uniform(4, 6)
    time.sleep(sleeptime)
    # if (index - 1) % 50 == 0:
    #     print('finish', index)

print('finished number of parcels', index % 8)

df = pd.DataFrame(grouped, columns=['asset_id', 'price', 'token_price', 'sale date', 'x', 'y', 'asset_properties'])
df.to_csv('virtual_land3.csv', index=False, header=True)
print(df)
