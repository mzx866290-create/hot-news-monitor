from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_51job_search():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        # Try different search URLs
        urls = [
            "https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1&sort=0",
            "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0",
        ]
        
        for url in urls:
            print(f"\n=== Testing {url[:60]}... ===")
            try:
                response = page.goto(url, timeout=20000, wait_until="networkidle")
                content = page.content()
                print(f"Status: {response.status}, Length: {len(content)}")
                
                if '验证' not in content[:2000] and '滑动' not in content[:2000]:
                    print("OK - no captcha")
                    # Try to find job items
                    # Look for common 51job selectors
                    job_items = page.query_selector_all('.j_joblist .job')
                    if not job_items:
                        job_items = page.query_selector_all('.joblist .item')
                    if not job_items:
                        job_items = page.query_selector_all('[class*="job"]')
                    print(f"Found {len(job_items)} job items")
                    
                    # Get page text
                    text = page.inner_text('body')
                    if 'AI' in text or '职位' in text:
                        print(f"Page has job content, preview: {text[:300]}")
                else:
                    print("BLOCKED by verification")
                    page.screenshot(path='captcha.png')
                    
            except Exception as e:
                print(f"ERROR: {e}")
        
        browser.close()

if __name__ == '__main__':
    test_51job_search()
