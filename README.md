# CoinMarketCap Scraper

This project provides a Django REST framework API for scraping cryptocurrency data from [CoinMarketCap](https://coinmarketcap.com/). It allows you to fetch details such as price, market cap, volume, and social links for a list of cryptocurrencies.

## Features

- Scrape cryptocurrency data from CoinMarketCap.
- REST API for starting a scraping job and checking its status.
- Extracts details including price, market cap, volume, and social links.
- Input validation to ensure proper cryptocurrency acronyms.
- Utilizes Django REST framework serializers for structured JSON responses.

## Installation

### Prerequisites

- Python 3.6+
- Django 3.2+
- Django REST Framework
- Selenium
- ChromeDriver

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/coinmarketcap-scraper.git
    cd coinmarketcap-scraper
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the Django project:**

    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

5. **Download and place the ChromeDriver executable in your system's PATH:**

    - You can download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
    - update the chromium path in settings.py

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

## Usage

### Start Scraping Job

Endpoint: `http://127.0.0.1:8000/api/taskmanager/start_scraping`  
Method: `POST`

#### Request Body

```json
{
    "coins": ["DUKO", "BTC", "ETH"]
}
```

### Check Scraping Status

Endpoint: `http://127.0.0.1:8000/api/taskmanager/scraping_status/<job_id>`  
Method: `GET`

#### Response Body

```json
{
  "job_id": "<UUID>",
  "tasks": [
    {
      "coin": "DUKO",
      "output": {
        "price": 0.003913,
        "price_change": -5.44,
        "market_cap": 37814377,
        "market_cap_rank": 740,
        "volume": 4583151,
        "volume_rank": 627,
        "volume_change": 12.21,
        "circulating_supply": 9663955990,
        "total_supply": 9999609598,
        "diluted_market_cap": 39127766,
        "contracts": [
          {
            "name": "solana",
            "address": "HLptm5e6rTgh4EKgDpYFrnRHbjpkMyVdEeREEa2G7rf9"
          }
        ],
        "official_links": [
          {
            "name": "website",
            "link": "https://dukocoin.com"
          }
        ],
        "socials": [
          {
            "name": "twitter",
            "url": "https://twitter.com/dukocoin"
          },
          {
            "name": "telegram",
            "url": "https://t.me/+jlScZmFrQ8g2MDg8"
          }
        ]
      }
    },
    {
      "coin": "BTC",
      "output": {
        // ...BTC details
      }
    },
    {
      "coin": "ETH",
      "output": {
        // ...ETH details
      }
    }
  ]
}
```
