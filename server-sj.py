from playwright.sync_api import sync_playwright
import random
import time
import threading

# Pages and referrers
PAGES = [
    'https://sjr.pages.dev/',
    'https://sjr.pages.dev/order',
    'https://sjr.pages.dev/company',
    'https://sjr.pages.dev/faq',
    'https://sjr.pages.dev/contact'
]

REFERRERS = [
            "https://www.google.com",
            "https://www.bing.com",
            "https://www.instagram.com",
            "https://www.youtube.com", 
            "https://www.linkedin.com", 
]

DEVICES = [
    "iPhone 12", "Galaxy S9+", "iPad Pro 11", "iPhone XR",
    "Kindle Fire HDX", "Moto G4 landscape", "Desktop Chrome HiDPI",
    "Desktop Edge HiDPI", "Desktop Firefox HiDPI", "Desktop Safari",
    "Desktop Chrome", "Desktop Edge", "Desktop Firefox", None
]

def scroll_to_bottom(page):
    """
    Scroll to the bottom of the page by continuously scrolling until no more height is available.
    """
    try:
        while True:
            # Get the current scroll height
            previous_height = page.evaluate("document.documentElement.scrollTop + window.innerHeight")
            
            # Scroll by one screen height
            page.evaluate("window.scrollBy(0, window.innerHeight);")
            
            # Wait for the page to load more content if applicable
            time.sleep(random.uniform(2, 3))
            
            # Get the new scroll height
            current_height = page.evaluate("document.documentElement.scrollTop + window.innerHeight")
            
            # Break the loop if the bottom is reached
            if current_height == previous_height:
                break
    except Exception as e:
        print(f"Error while scrolling: {e}")

def simulate_single_visitor(visitor_id):
    """
    Simulate a single visitor with random navigation and user interaction.
    """
    with sync_playwright() as p:
        try:
            # Launch the browser in headless mode
            browser = p.chromium.launch(headless=True)

            # Select a random device
            device_name = random.choice(DEVICES)
            device = p.devices[device_name] if device_name else None
            context = browser.new_context(**device) if device else browser.new_context()

            # Open a new page
            page = context.new_page()

            # Set a random referrer
            referrer = random.choice(REFERRERS)
            page.set_extra_http_headers({"Referer": referrer})

            # Select random pages to visit
            num_pages_to_visit = random.randint(1, len(PAGES))
            selected_pages = random.sample(PAGES, num_pages_to_visit)

            for page_url in selected_pages:
                # Navigate to the page
                page.goto(page_url)

                # Simulate scrolling to the bottom
                scroll_to_bottom(page)

                # Mimic a short pause between actions
                time.sleep(random.uniform(5, 9))

            print(f"Visitor {visitor_id} navigated successfully to {num_pages_to_visit} pages.")
            page.close()
            context.close()

        except Exception as e:
            print(f"Error for Visitor {visitor_id}: {e}")

        finally:
            browser.close()

def simulate_visitors(number_of_visitors, threads=10):
    """
    Simulate visitors in parallel using threads.
    """
    def worker(start, end):
        for visitor_id in range(start, end):
            simulate_single_visitor(visitor_id)

    batch_size = number_of_visitors // threads
    threads_list = []

    for i in range(threads):
        start = i * batch_size
        end = start + batch_size if i < threads - 1 else number_of_visitors
        thread = threading.Thread(target=worker, args=(start, end))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

if __name__ == "__main__":
    simulate_visitors(number_of_visitors=1100, threads=10)
