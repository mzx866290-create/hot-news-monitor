from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def debug():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        items = page.query_selector_all('.joblist-item')
        print(f"Found {len(items)} job items")
        
        # Get first item HTML
        item = items[0]
        html = item.inner_html()
        print(f"\nFirst item HTML ({len(html)} chars):")
        print(html[:1500])
        
        # Get first item text
        text = item.inner_text()
        print(f"\nFirst item text:")
        print(text[:500])
        
        browser.close()

if __name__ == '__main__':
    debug()
