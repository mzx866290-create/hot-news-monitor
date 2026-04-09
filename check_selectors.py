from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def check_page():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        print(f"Going to: {url}")
        page.goto(url, timeout=20000, wait_until="networkidle")
        
        # Get page HTML structure
        content = page.content()
        with open('51job_search.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved {len(content)} chars to 51job_search.html")
        
        # Find job-related elements
        print("\nLooking for job elements...")
        
        # Try various selectors
        selectors = [
            '.job', '.joblist', '.j_joblist', '.jobs',
            '[class*="job"]', '[class*="item"]',
            'div.job', 'div.item', 'li.job'
        ]
        
        for sel in selectors:
            try:
                count = len(page.query_selector_all(sel))
                if count > 0:
                    print(f"  {sel}: {count} elements")
            except:
                pass
        
        # Get page text preview
        text = page.inner_text('body')
        print(f"\nPage text (first 500 chars):\n{text[:500]}")
        
        browser.close()

if __name__ == '__main__':
    check_page()
