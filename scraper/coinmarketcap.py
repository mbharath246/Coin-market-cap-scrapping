import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

class CoinMarketCap:
    def __init__(self, chrome_driver_path):
        self.chrome_driver_path = chrome_driver_path

    def scrape_data(self, coin):
        url = f'https://coinmarketcap.com/currencies/{coin.lower()}/'
        service = Service(executable_path=self.chrome_driver_path)
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        
        data = {}
        
        try:
            element = driver.find_element(By.CSS_SELECTOR, 'span[data-role="coin-name"]')
            price_element = driver.find_element(By.CSS_SELECTOR,'span.sc-d1ede7e3-0.fsQm.base-text')
            volume_market = driver.find_elements(By.CSS_SELECTOR, 'dd.sc-d1ede7e3-0.hPHvUM.base-text')
            all_ranks = driver.find_elements(By.CSS_SELECTOR,'span.text.slider-value.rank-value')

            ranks = [rank.text.split('#')[-1] for rank in all_ranks]
            volume_market = [val_mar.text for val_mar in volume_market]

            data['coin'] = element.text.strip()
            data['price'] = price_element.text.split('$')[1]
            data['market_cap_rank'] = ranks[0]
            data['volume_rank'] = ranks[1]
            market = volume_market[0].split('\n')
            volume_all = volume_market[1].split('\n')
            volume_change = volume_market[2]
            circulating_supply = volume_market[3].split()[0]
            total_supply = volume_market[4].split()[0]
            diluted_market_cap = volume_market[-1].split()[-1].split('$')[1]

            data['price_change'] = market[0]
            data['market_cap'] = market[1].split('$')[1]
            data['volume'] = volume_all[1].split('$')[1]
            data['volume_change'] = volume_change
            data['circulating_supply'] = circulating_supply
            data['total_supply'] = total_supply
            data['diluted_market_cap'] = diluted_market_cap

            # Extract contract address
            contract_link = driver.find_element(By.XPATH, '//a[@class="chain-name"]')
            data['contracts'] = [{
                'name': contract_link.text.split(':')[0].strip().lower(),
                'address': contract_link.get_attribute("href").split('/')[-1]
            }]

            # Extract official links
            website_name = driver.find_elements(By.XPATH, '//a[@rel="nofollow noopener"]')
            links_names = [web.text for web in website_name]
            all_links = [web.get_attribute("href") for web in website_name]
            data['official_links'] = [{
                'name': links_names[1].lower(),
                'link': all_links[1]
            }]

            # Extract social links
            data['socials'] = []
            for i in range(2, len(links_names)):
                parts = links_names[i].split('\n')
                cleaned_name = parts[1].strip().lower() if len(parts) > 1 else links_names[i].strip().lower()
                social_entry = {
                    "name": cleaned_name,
                    "url": all_links[i]
                }
                data['socials'].append(social_entry)
        finally:
            driver.quit()

        return data
