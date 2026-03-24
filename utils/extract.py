import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    """Mengekstrak data produk dari satu halaman HTML"""
    try: 
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        cards = soup.find_all('div', class_='product-details')
        for card in cards:
            title_elem = card.find('h3', class_='product-title')
            title = title_elem.text.strip() if title_elem else None

            price_container = card.find('div', class_='price-container')
            if price_container:
                price_elem = price_container.find('span', class_='price')
                price = price_elem.text.strip() if price_elem else None
            else:
                price_elem = card.find('p', class_='price')
                price = price_elem.text.strip() if price_elem else None

            rating, colors, size, gender = None, None, None, None
            for p in card.find_all('p'):
                text = p.text.strip()
                if 'Rating:' in text: rating = text
                elif 'Colors' in text: colors = text
                elif 'Size:' in text: size = text
                elif 'Gender:' in text: gender = text

            products.append({
                'Title': title, 'Price': price, 'Rating': rating,
                'Colors': colors, 'Size': size, 'Gender': gender
            })
        return products
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None

def extract_data(total_pages=50):
    """Menjalankan proses scraping untuk seluruh halaman."""
    base_url = "https://fashion-studio.dicoding.dev"
    all_products = []
    
    for i in range(1, total_pages + 1):
        # Asumsi pola URL adalah ?page=x (sesuaikan jika berbeda)
        url = f"{base_url}/?page={i}" if i > 1 else base_url
        data = scrape_page(url)
        if data:
            all_products.extend(data)
            
    return all_products