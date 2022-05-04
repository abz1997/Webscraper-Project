from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import json
from tqdm import tqdm
from datetime import datetime
import random


class Scraper:

    """ This class contains the blueprints for a webscraper

    This class will access a website and gather information
    on different products listed and will store it in a 
    dictionary. The data from the webscraping session will
    be saved as json file.

    Attributes:
        url : The website that will be webscraped.
        driver: The driver that will be used for webscraping.
    """

    def __init__(self):
        options = Options()
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--no-sandbox") 
        # options.add_argument('--allow-running-insecure-content')
        # options.add_argument('--ignore-certificate-errors')
        options.add_argument('--window-size=1920,1080')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        # disable the banner "Chrome is being controlled by automated test software"
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        #options.add_argument('--headless') 
        
        self.url = 'http://books.toscrape.com/'
        self.driver = Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(self.url)
        self.counter = 0
        self.link_list = []
        self.item_dict = {'UPC': [], 'title':[], 'product_type': [],'genre':[] ,
                        'URL': [], 'image_link':[], 'price_excl_tax': [], 
                        'price_incl_tax':[],'tax':[],'availability': [], 
                        'number_of_reviews':[] }
        self.now = datetime.now()
        self.dt_string = self.now.strftime("%d.%m.%Y %H:%M:%S")
        self.newpath = f'./scraped_data/{self.dt_string}'
        


    def item_container(self):

        """Makes the webscraper find the container with all the products
           and then stores the links for all the products in a list on that page. 
           The webscraper then goes to then next page where the links are also
           collected. This repeats until there are no more pages remaining.
           The number of links are then printed."""

        print('Collecting item links...')
        while True:   # collects list of items from all pages
        #for i in range(2): # the range indicates the number of pages you would like to collect a list of items from

            try:
                items_xpath = '//*[@id="default"]/div/div/div/div/section/div[2]/ol'
                items = self.driver.find_element(By.XPATH, items_xpath)
                item_list = items.find_elements(By.XPATH, './li')

                for item in item_list:
                    a_tag = item.find_element(by = By.TAG_NAME, value = 'a')
                    link = a_tag.get_attribute('href')
                    self.link_list.append(link)
            
            except NoSuchElementException:
                pass

            try:
                x = random.randint(1,5)
                time.sleep(x)
                page_xpath = '//*[@id="default"]/div/div/div/div/section/div[2]/div/ul'
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, page_xpath)))
                page = self.driver.find_element(By.XPATH, page_xpath)
                #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                page_next = page.find_element(By.CLASS_NAME,'next')
                next = page_next.find_element(by = By.TAG_NAME, value = 'a')
                next_page = next.get_attribute('href')
                self.driver.get(next_page)

            except NoSuchElementException:
                print(f'There are {len(self.link_list)} items')
                break
        
        return self.link_list

    
    def collect_data(self):
        """The webscraper then checks out the links in the list and 
           stores information about these products in a dictionary. The 
           information stored include the URL, title, genre, product type, 
           price(including tax),price(excluding tax), tax, availability,
           number of reviews and a link to the image """

        #length = int(input('How many items would you like to scrape? '))
        for i in tqdm(self.link_list):
            self.driver.get(i)
            y = random.randint(1,2)
            time.sleep(y)

            self.item_dict['URL'].append(str(i))

            try: 
                upc_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[1]/td'
                upc = self.driver.find_element(By.XPATH, upc_xpath).text
                self.item_dict['UPC'].append(upc)
            except NoSuchElementException:
                self.item_dict['UPC'].append('N/A')

            try: 
                title_xpath = '//*[@id="content_inner"]/article/div[1]/div[2]/h1'
                title = self.driver.find_element(By.XPATH, title_xpath).text
                self.item_dict['title'].append(title)
            except NoSuchElementException:
                self.item_dict['title'].append('N/A')

            try: 
                genre_xpath = '//*[@id="default"]/div/div/ul/li[3]/a'
                genre = self.driver.find_element(By.XPATH, genre_xpath).text
                self.item_dict['genre'].append(genre)
            except NoSuchElementException:
                self.item_dict['genre'].append('N/A')

            try:
                product_type_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[2]/td'
                product_type = self.driver.find_element(By.XPATH, product_type_xpath).text
                self.item_dict['product_type'].append(str(product_type))
            except NoSuchElementException:
                self.item_dict['product_type'].append('N/A')  

            try:
                price_excl_tax_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[3]/td'
                price_excl_tax = self.driver.find_element(By.XPATH, price_excl_tax_xpath).text
                self.item_dict['price_excl_tax'].append(str(price_excl_tax))
            except NoSuchElementException:
                self.item_dict['price_excl_tax'].append('N/A')

            try: 
                price_incl_tax_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[4]/td'
                price_incl_tax = self.driver.find_element(By.XPATH, price_incl_tax_xpath).text
                self.item_dict['price_incl_tax'].append(price_incl_tax)
            except NoSuchElementException:
                self.item_dict['price_incl_tax'].append('N/A')

            try: 
                tax_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[5]/td'
                tax = self.driver.find_element(By.XPATH, tax_xpath).text
                self.item_dict['tax'].append(tax)
            except NoSuchElementException:
                self.item_dict['tax'].append('N/A')

            try: 
                availability_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[6]/td'
                availability = self.driver.find_element(By.XPATH, availability_xpath).text
                self.item_dict['availability'].append(availability)
            except NoSuchElementException:
                self.item_dict['availability'].append('N/A')
            
            try: 
                number_of_reviews_xpath = '//*[@id="content_inner"]/article/table/tbody/tr[7]/td'
                number_of_reviews = self.driver.find_element(By.XPATH, number_of_reviews_xpath).text
                self.item_dict['number_of_reviews'].append(number_of_reviews)
            except NoSuchElementException:
                self.item_dict['number_of_reviews'].append('N/A')

            try:
                find_pic_xpath = '//*[@id="product_gallery"]/div/div/div'
                find_pic = self.driver.find_element(By.XPATH, find_pic_xpath)
                img_tag = find_pic.find_element(by = By.TAG_NAME, value = 'img')
                img_link = img_tag.get_attribute('src')
                # if not os.path.exists(self.newpath):
                #    os.makedirs(self.newpath)
                # urllib.request.urlretrieve(img_link, f'{self.newpath}/{UPC}.jpg')
                self.item_dict['image_link'].append(img_link)
            except NoSuchElementException:
                self.item_dict['image_link'].append('N/A')

            self.counter +=1

        print(f'Collected items: : {self.counter}')
        self.driver.quit()
        return self.item_dict

    def save_data(self):
        """The data collected is then presented as a dataframe. 
            The data is also saved in the specified directory
            with the date time recorded in the directory name."""

        df = pd.DataFrame.from_dict(self.item_dict)
        print(df)
        
        if not os.path.exists(self.newpath):
            os.makedirs(self.newpath)
        #df.to_csv(f'{self.newpath}/data.csv', index=False)
        with open(f'{self.newpath}/data.json', 'w') as fp:
            json.dump(self.item_dict, fp, indent = 4)
        

if __name__ == "__main__":
    bot = Scraper()
    bot.item_container()
    bot.collect_data()
    bot.save_data()
