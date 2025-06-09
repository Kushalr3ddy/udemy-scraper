#https://easylearn.ing

from selenium import webdriver

url = 'https://easylearn.ing'
chrome = webdriver.Firefox()
chrome.get(url)
chrome.quit()