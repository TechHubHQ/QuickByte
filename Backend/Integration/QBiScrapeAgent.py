import json
import codecs
import random
import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Set the default encoding to UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


class ScrapeAgent:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.restaurants = {
            "restaurants": []
        }
        self.jumbo_tracker_details = []

    def setup_driver(self):
        """Initialize Chrome WebDriver and WebDriverWait with enhanced options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--disable-web-security')
        options.add_argument(
            f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def wait_for_images_to_load(self, max_wait_time=15):
        """Wait for all images to load on the page"""
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            images_loaded = self.driver.execute_script("""
                return Array.from(document.images).every(img => img.complete && img.naturalWidth > 0);
            """)
            if images_loaded:
                return True
            time.sleep(0.5)
        return False

    def scroll_page(self):
        """Scroll the page to load all dynamic content"""
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 3))
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        self.wait_for_images_to_load()

    def navigate_to_page(self, url, max_retries=3):
        """Navigate to the specified URL with retry mechanism and error handling"""
        retry_count = 0
        while retry_count < max_retries:
            try:
                self.driver.get(url)
                self.driver.maximize_window()
                time.sleep(random.uniform(2, 5))
                self.scroll_page()
                return True
            except Exception as e:
                retry_count += 1
                print(f"Connection attempt {retry_count} failed: {str(e)}")
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Could not establish connection.")
                    raise

    def find_best_food_element(self):
        """Find and return the 'Best Food' element using multiple selector strategies"""
        selectors = [
            (By.XPATH, "//*[contains(text(), 'Best Food')]"),
            (By.XPATH, "//h1[contains(text(), 'Best Food')]"),
            (By.XPATH, "//div[contains(text(), 'Best Food')]"),
            (By.CSS_SELECTOR, "[data-content='Best Food']"),
            (By.PARTIAL_LINK_TEXT, "Best Food")
        ]

        for selector in selectors:
            try:
                element = self.wait.until(
                    EC.presence_of_element_located(selector))
                self.wait.until(EC.element_to_be_clickable(selector))
                return element
            except (TimeoutException, NoSuchElementException):
                continue

        raise NoSuchElementException(
            "Could not find 'Best Food' element using any selector strategy")

    def find_jb_trackers(self):
        """Find all jumbo-tracker elements that appear after the Best Food element in the DOM"""
        try:
            best_food = self.find_best_food_element()
            best_food_location = best_food.location

            jumbo_trackers = self.driver.find_elements(
                By.CSS_SELECTOR, ".jumbo-tracker")

            filtered_trackers = []
            for tracker in jumbo_trackers:
                tracker_location = tracker.location
                if tracker_location['y'] > best_food_location['y']:
                    filtered_trackers.append(tracker)
                    # Store raw jumbo tracker details for comparison
                    self.jumbo_tracker_details.append({
                        'element': tracker,
                        'location': tracker_location,
                        'html': tracker.get_attribute('outerHTML'),
                        'text': tracker.text
                    })

            return filtered_trackers
        except NoSuchElementException:
            return []

    def extract_restaurant_details(self, element):
        """Extract details from a restaurant element"""
        try:
            text_content = element.text.split('\n')

            discount = next(
                (text for text in text_content if 'OFF' in text), None)
            discount_idx = text_content.index(discount) if discount else -1

            rating = next((float(text) for text in text_content
                           if text and text[0].isdigit() and len(text) <= 3), None)
            rating_idx = text_content.index(
                str(rating)) if rating else len(text_content)

            name = None
            if discount_idx != -1 and discount_idx + 1 < rating_idx:
                name = text_content[discount_idx + 1]
            elif rating_idx > 0:  # No discount, take line before rating
                name = text_content[rating_idx - 1]
            else:  # Fallback: first line without excluded keywords
                name = next((text for text in text_content if text and not any(
                    x in text for x in ['OFF', 'min', '₹', 'Promoted', 'Open'])), None)

            # Extract other details
            price = next(
                (text for text in text_content if '₹' in text and 'for' in text), None)

            # Improved delivery time extraction
            delivery_time = next(
                (text for text in text_content if re.search(r'^\d+\s*min$', text)), None)
            if not delivery_time:  # Fallback if exact match fails
                delivery_time = next(
                    (text for text in text_content if 'min' in text), None)
            distance = next(
                (text for text in text_content if re.search(r'\d+\.?\d*\s*km', text.strip())), None)

            # Extract opens_at time if it exists after price
            opens_at = None
            if price:
                price_idx = text_content.index(price)
                for idx in range(price_idx + 1, len(text_content)):
                    if 'Opens' in text_content[idx]:
                        opens_at = text_content[idx]
                        break

            # Extract cuisines - Get text between rating and price
            cuisines = None
            if rating is not None and price is not None:
                rating_idx = text_content.index(str(rating))
                price_idx = text_content.index(price)
                if rating_idx + 1 < price_idx:
                    cuisines = text_content[rating_idx + 1]

            # Extract location
            location = None
            if price:
                price_idx = text_content.index(price)
                for idx in range(price_idx + 1, len(text_content)):
                    # Skip distance entries
                    if 'km' in text_content[idx]:
                        continue
                    # Look for location text that's not delivery time or opens_at
                    if not any(x in text_content[idx] for x in ['min', 'Opens']):
                        location = text_content[idx].strip()
                        break

            # Extract images
            images = [img.get_attribute('src') for img in element.find_elements(
                By.TAG_NAME, 'img') if img.get_attribute('src')]

            # Extract links
            links = list(set([a.get_attribute('href') for a in element.find_elements(
                By.TAG_NAME, 'a') if a.get_attribute('href')]))

            return {
                "name": name,
                "discount": discount,
                "rating": rating,
                "cuisines": cuisines,
                "price": price,
                "delivery_time": delivery_time,
                "distance": distance,
                "opens_at": opens_at,
                "location": location,
                "images": images,
                "links": links,
            }
        except Exception as e:
            print(f"Error extracting restaurant details: {str(e)}")
            return None

    def get_restaurant_images(self, element):
        """Extract all image URLs from a restaurant element"""
        images = []

        if element.tag_name == "img":
            src = element.get_attribute("src")
            if src and "data:image" not in src:
                images.append(src)

        nested_images = element.find_elements(By.TAG_NAME, "img")
        for img in nested_images:
            src = img.get_attribute("src")
            if src and "data:image" not in src:
                images.append(src)

        bg_images = element.find_elements(
            By.CSS_SELECTOR, "[style*='background-image']")
        for bg in bg_images:
            style = bg.get_attribute("style")
            url_match = re.search(r'url\(["\']?(.*?)["\']?\)', style)
            if url_match and "data:image" not in url_match.group(1):
                images.append(url_match.group(1))

        return list(set(images))

    def get_restaurant_links(self, element):
        """Extract all link URLs from a restaurant element"""
        links = []

        if element.tag_name == "a":
            href = element.get_attribute("href")
            if href and "zomato.com" in href:
                links.append(href)

        nested_links = element.find_elements(By.TAG_NAME, "a")
        for link in nested_links:
            href = link.get_attribute("href")
            if href and "zomato.com" in href:
                links.append(href)

        return list(set(links))

    def process_restaurant_element(self, element):
        """Process a single restaurant element and return complete details"""
        details = self.extract_restaurant_details(element)

        if details:
            if details["links"] and details["name"] == "Unknown":
                for link in details["links"]:
                    if "/info" in link:
                        name_from_url = link.split(
                            "/")[-2].replace("-", " ").title()
                        details["name"] = name_from_url
                        break

            if details["name"] == "Unknown" and not details["rating"] and not details["discount"] and not details["price"]:
                return None

            return details
        return None

    def print_restaurants_json(self):
        """Print the restaurants data and jumbo tracker details as pretty-printed JSON"""
        print("\nRestaurants Data:")
        print(json.dumps(self.restaurants, indent=2, ensure_ascii=False))

    def cleanup(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

    def scrape(self):
        """Main scraping method with error handling"""
        try:
            self.setup_driver()
            self.navigate_to_page("https://www.zomato.com/vizianagaram")

            try:
                best_food_element = self.find_best_food_element()
                print("Successfully found the 'Best Food' element")

                jumbo_trackers = self.find_jb_trackers()
                if jumbo_trackers:
                    print(
                        f"\nFound {len(jumbo_trackers)} restaurant elements:")
                    for tracker in jumbo_trackers:
                        restaurant_data = self.process_restaurant_element(
                            tracker)
                        if restaurant_data:
                            self.restaurants["restaurants"].append(
                                restaurant_data)

                    print(
                        f"Successfully processed {len(self.restaurants['restaurants'])} restaurants")
                else:
                    print("\nNo restaurants found after 'Best Food' section")

                self.print_restaurants_json()

            except TimeoutException:
                print("Timeout while waiting for 'Best Food' element to load")
            except NoSuchElementException as e:
                print(f"Could not find 'Best Food' element: {str(e)}")

        except Exception as e:
            print(f"Critical error occurred: {str(e)}")
        finally:
            self.cleanup()


if __name__ == "__main__":
    try:
        scraper = ScrapeAgent()
        scraper.scrape()
    except KeyboardInterrupt:
        print("Process terminated - Keyboard interrupt detected")
