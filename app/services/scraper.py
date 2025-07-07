# is-it-in-yet/app/services/scraper.py

from playwright.sync_api import sync_playwright, TimeoutError
import logging

# Define a more comprehensive set of selectors. This can be expanded over time.
# The order matters: we try the most specific ones first.
SITE_SELECTORS = {
    'amazon': {
        'name': ['#productTitle'],
        'price': ['.a-price .a-offscreen', 'span[data-a-size="xl"] .a-offscreen'],
        'image': ['#landingImage', '#imgTagWrapperId img'],
        'in_stock_text': ['#add-to-cart-button', '#buy-now-button'],
        'out_of_stock_text': ['currently unavailable', 'out of stock'],
    },
    'default': {
        'name': ['h1', '[itemprop="name"]', '[class*="product-name"]', '[class*="product-title"]'],
        'price': ['[itemprop="price"]', '[class*="price"]', '[class*="Price"]'],
        'image': ['img[src*="product"]', 'img[class*="product-image"]', '#main-image'],
        'in_stock_text': ['add to cart', 'add to basket', 'buy now'],
        'out_of_stock_text': ['out of stock', 'sold out', 'unavailable'],
    }
}

def get_site_key(url: str) -> str:
    """Determines which set of selectors to use based on the URL."""
    if 'amazon' in url:
        return 'amazon'
    # Add more site-specific keys here in the future (e.g., 'ebay', 'walmart')
    return 'default'

def scrape_product_data(url: str) -> dict:
    """
    Scrapes a given product URL to extract its name, price, image, and stock status.
    This version is more robust with better waiting and more selectors.
    """
    data = {'status': 'Scrape Failed', 'name': None, 'image_url': None, 'price': None}
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            logging.info(f"Navigating to {url}...")
            page.goto(url, timeout=90000, wait_until='domcontentloaded')
            
            # Wait for the network to be mostly idle, a good sign that dynamic content has loaded.
            page.wait_for_load_state('networkidle', timeout=30000)
            logging.info("Page loaded, network is idle. Starting scrape.")

            site_key = get_site_key(url)
            selectors = SITE_SELECTORS[site_key]

            # --- Helper function to find the first matching element ---
            def query_selector_with_list(selector_list):
                for selector in selector_list:
                    element = page.query_selector(selector)
                    if element:
                        logging.info(f"Found element with selector: '{selector}'")
                        return element
                logging.warning(f"Could not find any element for selectors: {selector_list}")
                return None

            # --- Extract Data ---
            name_element = query_selector_with_list(selectors['name'])
            if name_element:
                data['name'] = name_element.inner_text().strip()

            image_element = query_selector_with_list(selectors['image'])
            if image_element:
                # Try 'src', but fall back to 'data-src' for lazy-loaded images
                data['image_url'] = image_element.get_attribute('src') or image_element.get_attribute('data-src')

            price_element = query_selector_with_list(selectors['price'])
            if price_element:
                data['price'] = price_element.inner_text().strip()

            # --- Determine Stock Status ---
            page_content_lower = page.content().lower()
            
            if any(text.lower() in page_content_lower for text in selectors['out_of_stock_text']):
                data['status'] = 'Out of Stock'
            else:
                # Check for an "in stock" indicator
                for text in selectors['in_stock_text']:
                    # Check if an element with this text exists
                    if text in page_content_lower:
                        data['status'] = 'In Stock'
                        break
            
            browser.close()
            logging.info(f"Scrape successful for {url}. Status: {data['status']}")
            return data

        except TimeoutError as e:
            logging.error(f"Timeout error while scraping {url}. The page took too long to load. Error: {e}")
            data['status'] = 'Error: Timeout'
            return data
        except Exception as e:
            logging.error(f"An unexpected error occurred while scraping {url}. Error: {e}", exc_info=True)
            data['status'] = 'Error: Scrape Failed'
            return data