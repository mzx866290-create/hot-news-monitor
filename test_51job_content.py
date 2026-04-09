from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_51job_content():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1"
        print(f"Testing {url}")
        page.goto(url, timeout=20000, wait_until="networkidle")
        content = page.content()
        print(f"Content length: {len(content)}")
        
        # Check if verification
        if '验证' in content[:2000] or '滑动' in content[:2000]:
            print("BLOCKED by verification")
        else:
            print("OK - got content")
            # Save to file
            with open('51job_page.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("Saved to 51job_page.html")
            
            # Try to find job data in JSON
            if 'job' in content.lower() or '职位' in content:
                print("Found job-related content")
                
            # Get page text
            text = page.inner_text('body')
            print(f"\nPage text preview:\n{text[:1000]}")
        
        browser.close()

if __name__ == '__main__':
    test_51job_content()
