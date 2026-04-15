import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_site(url):
    try: 
        response = requests.get(url, headers=headers, timeout=20)

        soup = BeautifulSoup(response.text, "html.parser")

        return soup
    
    except:
        return False
