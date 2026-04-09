from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def check_links():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        # Get all links on page
        links = page.query_selector_all('a')
        print(f"Total links: {len(links)}")
        
        # Find links with "job" in href or text
        job_links = []
        for link in links:
            try:
                href = link.get_attribute('href') or ''
                text = link.inner_text().strip()
                if 'job' in href.lower() or ('AI' in text and len(text) > 10):
                    job_links.append((href[:80], text[:50]))
            except:
                pass
        
        print(f"\nJob-related links ({len(job_links)}):")
        for href, text in job_links[:20]:
            print(f"  {href}")
            print(f"    Text: {text}")
        
        # Also check links with jQuery-style or onclick
        onclick_links = page.query_selector_all('[onclick*="job"]')
        print(f"\nElements with job onclick: {len(onclick_links)}")
        
        browser.close()

if __name__ == '__main__':
    check_links()
