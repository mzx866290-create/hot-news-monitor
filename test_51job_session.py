from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_51job_session():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0] if browser.contexts else browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.pages[0] if context.pages else context.new_page()
        
        print("1. Going to 51job homepage first...")
        page.goto("https://www.51job.com", timeout=20000, wait_until="domcontentloaded")
        print(f"   Homepage loaded: {len(page.content())} chars")
        
        print("\n2. Now going to search page...")
        page.goto("https://search.51job.com/list/760000,000000,0000,00,9,99,AI,2,1.html", timeout=20000, wait_until="networkidle")
        content = page.content()
        print(f"   Search page loaded: {len(content)} chars")
        
        if '验证' not in content[:2000] and '滑动' not in content[:2000]:
            print("   SUCCESS - got search results!")
            # Extract some job titles
            titles = page.query_selector_all('.job_title')
            print(f"   Found {len(titles)} job titles")
            for t in titles[:5]:
                print(f"   - {t.inner_text()}")
        else:
            print("   BLOCKED - still verification")
            
            # Try to take screenshot
            page.screenshot(path='51job_captcha.png')
            print("   Screenshot saved to 51job_captcha.png")
        
        browser.close()

if __name__ == '__main__':
    test_51job_session()
