import requests
import random
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

# SCRAPING
##################################################################  SCRAPE NONFUNGIBLE SITE  ############################################################################

test_url = "https://nonfungible.com/market/history/decentraland?filter=nftTicker%3DLAND&filter=saleType%3D&length=50&sort=blockTimestamp%3Ddesc&start=0"
start_url = "https://nonfungible.com/market/history/decentraland?filter=nftTicker%3DLAND&filter=saleType%3D&length=100&sort=blockTimestamp%3Ddesc&start=0"
driver = webdriver.Chrome(r'C:\Users\chengkun\chromedriver.exe')  # change the driver's directory to your local place
driver.maximize_window()
driver.get(test_url)
# iver.find_element_by_xpath("//select[@aria-label='rows per page']/option[text()='50 rows']").click()

result = []
page_count = 1
while page_count <= 1:  # set this yourself: this number is the returned
    # collect all present elements in the table
    # First return the table body: table body -> table_rows -> row-> 8 columns
    table_rows = WebDriverWait(driver, 1000).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.rt-tbody div.rt-tr-group'))
    )

    print(table_rows)
    print()
    print(
        "===================================================================  Page Divider  ===================================================================")
    print()
    row_count = 1
    for row in table_rows:
        print()
        print(
            "===================================================================  Row Divider  ===================================================================")
        print(row)
        print("page number:", page_count)
        print("row number:", row_count)
        print("---------------------visible content----------------------")

        # 1. Add columns in one row to the result
        for col in row.find_elements_by_css_selector('div.rt-td'):
            if col.text == "":
                print("<null>")
            else:
                print(col.text)
                result.append(col.text)

        # 2. Redirect to this row
        # Find it and click on it to open the tag

        # try:
        #     clickable_element = container.find_element_by_css_selector('div:first-child')
        #     action = webdriver.common.action_chains.ActionChains(driver)
        #     action.move_to_element(clickable_element)
        #     action.click()
        #     action.perform()
        # except:
        #     clickable_element = container.find_element_by_css_selector('div:nth-child(2)')
        #     action = webdriver.common.action_chains.ActionChains(driver)
        #     action.move_to_element(clickable_element)
        #     action.click()
        #     action.perform()

        ##### 2.1: choice one: click on the first child (not good)
        # clickable_element = row.find_element_by_css_selector('div.rt-td')
        # clickable_element.click()

        ##### 2.2: click on the center of clickable item (not stable)
        # print(row)
        # clickable_element = row.find_element_by_css_selector('div.rt-td:nth-last-child(1)')
        # print(clickable_element)
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element(clickable_element)
        # action.click()
        # action.perform()

        ##### 2.3: click on the center of img (not stable)
        # print(row)
        # clickable_element = row.find_element_by_css_selector('div.rt-td')
        # print(clickable_element)
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element(clickable_element)
        # action.click()
        # print(action.perform())

        ##### 2.4: click on the center of row (not stable)
        # print(row)
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element(row)
        # action.click()
        # action.perform()

        ##### 2.5 select by xPath (does not work properly)
        # print(row)
        # clickable_element = row.find_element_by_xpath("//div[@role = 'gridcell']")
        # print(clickable_element)
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element(clickable_element)
        # action.click()
        # action.perform()

        ##### 2.6: choose by explicit xPath (does not work properly)
        # print(row)
        # item = row.find_element_by_xpath("//div[@role = 'rowgroup']/div")
        # print(item)
        # action = webdriver.common.action_chains.ActionChains(driver)
        # action.move_to_element(item)
        # action.click()
        # action.perform()
        #
        # sleep_time = random.uniform(2, 3)
        # time.sleep(sleep_time)

        ##### 2.7: Use JavaScript + xPath (WORKING PERFECTLY: LONG LIVE JS!!!)
        print(row)
        click_xpath = '//*[@id="__next"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[{}]/div/div[2]'.format(
            row_count)
        click_element = driver.find_element_by_xpath(click_xpath)
        print(click_element)
        driver.execute_script("arguments[0].click();", click_element)

        inner_rows = WebDriverWait(driver, 1000).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.modal-text.d-inline-block'))
        )

        print("-----------------------PopUp Window----------------------")
        for pos in inner_rows:
            result.append(pos.text)
            print(pos.text)

        back = driver.find_element_by_css_selector('h5.modal-title button')
        back.click()
        sleep_time = random.uniform(2, 3)
        time.sleep(sleep_time)
        row_count += 1

    button = driver.find_element_by_xpath('//button[contains(text(), "Next")]')
    driver.execute_script("arguments[0].click();", button)

    page_count += 1

print(page_count)
print(result)

# QUERY
##################################################################  QUERY DECENTRALAND API  #########################################################################################

# Index has to start from index = 5, because in the returned result[]: 5th and 6th elements are land coordinates x , y. They occur every 12 elements
index = 5
# queried is a dictionary to store a structure: land reference -> properties.
queried = {}
# grouped is the final outcome of what we want to put inside the csv file.
grouped = []

while index < len(result) - 6:

    # check if this parcel has already been queried. if not, query it; else,
    if result[index - 4] not in queried.keys():
        # requests xhr resources from decentraland V2 API
        xhr = 'https://api.decentraland.org/v2/parcels/{}/{}'
        response = requests.get(xhr.format(result[index], result[index + 1]))
        if response.status_code != 200:
            print('Bad Connection to API!')
            break
        # properties is returned in json format
        properties = response.json()
        queried[result[index - 4]] = properties
        print(properties)
    else:
        properties = queried[result[index - 4]]
        print(properties)

    grouped.append([str(result[index - 4]), result[index - 3], result[index - 2], result[index - 1], result[index],
                    result[index + 1], result[index + 2], result[index + 3], result[index + 4], result[index + 5],
                    result[index + 6], properties])
    index += 12
    sleep_time = random.uniform(1, 2)
    time.sleep(sleep_time)

print('finished number of parcels', index % 12)

df = pd.DataFrame(grouped, columns=['asset_id', 'price', 'token_price', 'sale_date', 'x', 'y', 'to_road', 't0_genesis',
                                    'to_district', 'closest_genesis', 'closest_district', 'properties_json'])
df.to_csv('virtual_land1.csv', index=True, header=True)
print(df)
