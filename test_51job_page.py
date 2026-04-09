from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_51job():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        # Try search results page
        urls = [
            "https://search.51job.com/list/760000,000000,0000,00,9,99,AI,2,1.html",
            "https://we.51job.com",
            "https://www.51job.com",
        ]
        
        for url in urls:
            print(f"\n=== Testing {url} ===")
            try:
                page.goto(url, timeout=20000, wait_until="domcontentloaded")
                content = page.content()
                print(f"Content length: {len(content)}")
                
                # Check if blocked
                if '验证' in content[:1000] or '滑动' in content[:1000]:
                    print("BLOCKED by verification")
                else:
                    print("OK - got content")
                    # Try to find job listings
                    jobs = page.query_selector_all('.job')
                    print(f"Found {len(jobs)} job elements")
                    
            except Exception as e:
                print(f"ERROR: {e}")
        
        browser.close()

if __name__ == '__main__':
    test_51job()
