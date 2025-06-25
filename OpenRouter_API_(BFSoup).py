# # import requests
# # import json
# # from bs4 import BeautifulSoup

# # url = "https://openrouter.ai/deepseek/deepseek-chat-v3-0324/providers"

# # page = requests.get(url)

# # #print(page.status_code)  

# # #prints 200, meaning that the content is being pulled & server is responsive

# # soup = BeautifulSoup(page.text, 'html.parser')

# # print(soup)
# #ok its just printing gibberish, not really giving anything useful
# #tried inspect element to find the data, but they are disabling that, so the onyl way is to use LLM API calls

# import requests
# from bs4 import BeautifulSoup

# url = "https://openrouter.ai/deepseek/deepseek-chat-v3-0324/providers"
# response = requests.get(url)

# soup = BeautifulSoup(response.text, 'html.parser')

# # Find all <a> tags with the provider class
# provider_links = soup.select('a[href^="/provider/"]')
# providers = [a.text.strip() for a in provider_links]

# print("Providers found:")
# for provider in providers:
#     print("-", provider)


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import time

# options = Options()
# options.add_argument("--headless")  
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")

# driver = webdriver.Chrome(options=options)

# url = "https://openrouter.ai/deepseek/deepseek-chat-v3-0324/providers"
# driver.get(url)

# time.sleep(5)  

# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# provider_links = soup.find_all("a", class_="text-muted-foreground/80 underline underline-offset-2")
# providers = [link.text.strip() for link in provider_links]

# print("Providers found:")
# for provider in providers:
#     print("-", provider)

# driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

#set up chrome for the selenium package to open and parse through
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

url = "https://openrouter.ai/deepseek/deepseek-chat-v3-0324/providers"
driver.get(url)

#wait for the page to load in 
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "a"))
)

#wait for the images/tables to load in properly
time.sleep(2)

#creating a method for the edge case where there are multiple providers and to click on that button and then parse through to see
try:
    show_more_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show') and contains(text(), 'more')]"))
    )
    show_more_button.click()
    print("✅ Clicked 'Show more'")
    time.sleep(2)  
except:
    print("⚠️ No 'Show more' button found or already clicked.")

#get the html of the rendered page and then use beautiful soup to parse the page
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

#saw that the providers were labeled as providers/name so used that format to gather the info
provider_links = soup.find_all("a", class_="text-muted-foreground/80 underline underline-offset-2")
providers = [link.text.strip() for link in provider_links]

print("✅ Providers found:")
for p in providers:
    print("-", p)

driver.quit()


