import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as bs

import json

options = Options()
#options.headless = True  # Enable headless mode for invisible operation
options.add_argument("--window-size=1920,1200")  # Define the window size of the browser





final_df = pd.DataFrame()

csv_dir ="./raw_layer"
for file in os.listdir(csv_dir):
    if file.endswith(".csv"):
        print(file)

    curr_df = pd.read_csv(os.path.join(csv_dir,file))
    #print(curr_df.head)

#discount price 
# //*[@id="u64-tabs--199-content-0"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[1]

# actual price
# //*[@id="u64-tabs--199-content-0"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[2]

# discount percent
# //*[@id="u64-tabs--199-content-0"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[3]

# duration left at this price
# //*[@id="u64-tabs--199-content-0"]/div[2]/div[1]/div[1]/div/div[3]/div/span


ffx =webdriver.Firefox()
ffx.get("https://www.udemy.com/course/chatgpt-for-product-management-innovation-h/?couponCode=ST19MT280525G3")
#discount_price = ffx.find_element(By.XPATH,"//*[@id=\"u64-tabs--199-content-0\"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[1]")
#print()
"""
try:
    element = WebDriverWait(ffx, 60).until(
        EC.presence_of_element_located((By.XPATH,"//*[@id=\"u64-tabs--199-content-0\"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div[1]"))
    )
finally:
    ffx.quit()
"""


ffx.implicitly_wait(30)

raw_html = ffx.page_source

soup  = bs(raw_html,features="lxml")

with open("bltest.html","w") as f:
    f.write(str(raw_html.encode("utf-8")))


#raw_price = soup.find_all("div",attrs={"class":"base-price-text-module--container--Sfv-5 ud-clp-price-text"})
raw_price =soup.find("script", type="application/ld+json")

raw_json = json.loads(raw_price.string)
with open("bronze.json","w") as f:
    f.write(json.dumps(raw_json))

#ffx.quit()