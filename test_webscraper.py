import unittest
from webscraper import Scraper
import os.path

class Test_scrape(unittest.TestCase):

    def setUp(self):
         self.bot = Scraper()
        
    def test_url(self):
        expected_value = 'http://books.toscrape.com/'
        actual_value = self.bot.url
        self.assertEqual(expected_value, actual_value)

    def test_item_container(self):
        expected_value = True
        all_links = self.bot.item_container()
        actual_value = all('http://books.toscrape.com/' in link for link in all_links)
        self.assertEqual(expected_value, actual_value)

    def test_collect_data(self):
        self.bot.item_container()
        self.bot.collect_data()
        if len(self.bot.item_dict['UPC']) > 1 :
            actual_value = True
        else:
            actual_value = False
        expected_value = True
        self.assertEqual(expected_value, actual_value)

    def test_save_data(self):
        self.bot.save_data()
        actual_value = os.path.isfile(f'./scraped_data/{self.bot.dt_string}/data.json') 
        self.assertTrue(actual_value)

if __name__ == "__main__": 
    unittest.main(verbosity=2, exit=False)