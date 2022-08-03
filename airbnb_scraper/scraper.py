import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class AirbnbScraper():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
        }
        self.driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def __scroll_down_page(self, speed=10):
        time.sleep(5)
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            self.driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.driver.execute_script("return document.body.scrollHeight")

    def parse_url(self, url):
        self.driver.get(url)
        self.__scroll_down_page()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        elements = soup.select("div[itemprop='itemListElement']")
        for element in elements:
            title = element.find("span", class_="njbvqj3 dir dir-ltr").text

            price_block = element.find("div", class_="_i5duul")
            try:
                price_per_night = price_block.findAll("span", class_="a8jt5op dir dir-ltr")[0].text
            except Exception as e:
                print('Unable to get price per night')
                price_per_night = None
            try:
                price_total = price_block.findAll("span", class_="a8jt5op dir dir-ltr")[1].text
            except Exception as e:
                print('Unable to get total price')
                price_total = None

            print(title)
            print(price_total)
            print(price_per_night)
            print('\n\n')


if __name__ == '__main__':
    airbnb = AirbnbScraper()
    airbnb.parse_url(url='https://www.airbnb.co.in/s/New-York--NY--United-States/homes?query=New York, NY, United States&checkin=2020-03-12&checkout=2020-03-19&adults=4&children=1&infants=0&guests=5&place_id=ChIJOwg_06VPwokRYv534QaPC8g&refinement_paths[]=/for_you&toddlers=0&source=mc_search_bar&search_type=unknown')
