import os 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from time import sleep

ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'
FORM_URL = os.environ['GOOGLE_DOCS_URL']
CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
HEADERS = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br', 
    'accept-language': 'en-US,en;q=0.9', 
    'sec-fetch-mode': 'cors', 
    'sec-fetch-site': 'same-origin', 
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
}

class RentalScraper: 

    def __init__(self, path):
        self.driver = webdriver.Chrome(executable_path=path)
        self.data = []

    def get_rental_data(self): 
        response = requests.get(ZILLOW_URL, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')  
        rentals = soup.find_all('div', class_='list-card-info')
        for item in rentals[:-1]: 
            entry = {}
            entry['address'] = item.find('address').text
            entry['price'] = item.find('div', class_='list-card-price').text.split()[0]
            entry['link'] = 'https://www.zillow.com/' + item.find('a', class_='list-card-link').get('href')
            self.data.append(entry)

    def input_data(self): 
        for item in self.data: 
            
            sleep(1)
            self.driver.get(FORM_URL)
            sleep(1)

            address, price, link = self.driver.find_elements_by_xpath(
                '//div[@class="freebirdFormeditorViewItemContent"]//div[@class="quantumWizTextinputSimpleinputContentArea"]//input[@type="text"]'
            )
            address.send_keys(item['address'])
            price.send_keys(item['price'])
            link.send_keys(item['link'])

            self.driver.find_element_by_xpath('//span[@class="appsMaterialWizButtonPaperbuttonContent exportButtonContent"]').click()

        self.driver.quit()



bot = RentalScraper(CHROME_DRIVER_PATH)

bot.get_rental_data()
bot.input_data()