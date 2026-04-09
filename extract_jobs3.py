from playwright.sync_api import sync_playwright
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

def extract_51job_jobs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        jobs = []
        seen = set()
        
        # Method: Find all <a> tags with job links (they have /job/ in href)
        all_links = page.query_selector_all('a[href*="/job/"]')
        print(f"Found {len(all_links)} job links")
        
        for link in all_links:
            try:
                href = link.get_attribute('href') or ''
                title = link.inner_text().strip()
                
                # Skip short titles (badges, tags)
                if len(title) < 6:
                    continue
                    
                # Skip if already seen
                if title in seen:
                    continue
                seen.add(title)
                
                # Get parent element for more info
                parent = link.evaluate('el => el.closest(".job") || el.parentElement.parentElement')
                
                # Try to get salary from nearby elements
                salary = ''
                try:
                    salary_elem = page.query_selector(f'xpath=//a[@href="{href}"]/../../../td[3]')
                    if salary_elem:
                        salary = salary_elem.inner_text().strip()
                except:
                    pass
                
                # Clean up
                title = re.sub(r'\s+', ' ', title)
                
                jobs.append({
                    'title': title[:100],
                    'url': href,
                    'source': '51job',
                    'salary': salary,
                    'category': 'job_news',
                    'time': '',
                    'summary': title
                })
                print(f"  {title[:50]} | {salary}")
                
                if len(jobs) >= 30:
                    break
                    
            except Exception as e:
                pass
        
        print(f"\nExtracted {len(jobs)} unique jobs")
        
        with open('jobs_51job.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print("Saved to jobs_51job.json")
        
        browser.close()
        return jobs

if __name__ == '__main__':
    extract_51job_jobs()
