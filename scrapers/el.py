#https://easylearn.ing

from selenium import webdriver
import notify
url = 'https://easylearn.ing'
chrome = webdriver.Firefox()
chrome.get(url)
chrome.quit()