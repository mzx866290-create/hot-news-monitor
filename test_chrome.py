from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_chrome():
    with sync_playwright() as p:
        # Try to connect to existing Chrome
        print("Trying to connect to Chrome...")
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            print("Connected via CDP!")
            page = browser.new_page()
            page.goto("https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1", timeout=15000)
            content = page.content()
            print(f"Content length: {len(content)}")
            print(content[:500])
            browser.close()
        except Exception as e:
            print(f"CDP connect failed: {e}")
            
            # Try launching new browser
            print("\nTrying to launch new Chromium...")
            try:
                browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
                print("Launched new browser!")
                page = browser.new_page()
                page.goto("https://we.51job.com", timeout=15000)
                content = page.content()
                print(f"Content length: {len(content)}")
                browser.close()
            except Exception as e2:
                print(f"Launch failed: {e2}")

if __name__ == '__main__':
    test_chrome()
