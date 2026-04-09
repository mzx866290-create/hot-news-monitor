from playwright.sync_api import sync_playwright
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

def extract_jobs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        # This URL worked - search for AI jobs
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        print(f"Going to: {url}")
        response = page.goto(url, timeout=20000, wait_until="networkidle")
        print(f"Status: {response.status}")
        
        # Wait for job list to load
        page.wait_for_selector('.j_joblist', timeout=10000)
        
        # Get all job items
        job_items = page.query_selector_all('.j_joblist .job')
        print(f"Found {len(job_items)} job items")
        
        jobs = []
        for item in job_items[:20]:  # First 20
            try:
                # Try different selectors
                title_elem = item.query_selector('.j_title')
                if not title_elem:
                    title_elem = item.query_selector('.title')
                if not title_elem:
                    title_elem = item.query_selector('a')
                
                title = title_elem.inner_text().strip() if title_elem else ''
                link = title_elem.get_attribute('href') if title_elem else ''
                
                company_elem = item.query_selector('.j_name')
                if not company_elem:
                    company_elem = item.query_selector('.company')
                company = company_elem.inner_text().strip() if company_elem else ''
                
                salary_elem = item.query_selector('.j_salary')
                if not salary_elem:
                    salary_elem = item.query_selector('.salary')
                salary = salary_elem.inner_text().strip() if salary_elem else ''
                
                area_elem = item.query_selector('.j_place')
                if not area_elem:
                    area_elem = item.query_selector('.place')
                area = area_elem.inner_text().strip() if area_elem else ''
                
                if title:
                    jobs.append({
                        'title': re.sub(r'\s+', ' ', title),
                        'company': re.sub(r'\s+', ' ', company),
                        'salary': salary,
                        'area': area,
                        'url': link
                    })
                    print(f"  {title[:50]} | {company[:20]} | {salary}")
            except Exception as e:
                print(f"  Error: {e}")
        
        print(f"\nTotal extracted: {len(jobs)} jobs")
        
        # Save to file
        import json
        with open('extracted_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print("Saved to extracted_jobs.json")
        
        browser.close()

if __name__ == '__main__':
    extract_jobs()
