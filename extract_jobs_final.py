from playwright.sync_api import sync_playwright
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

def extract_jobs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        jobs = []
        seen = set()
        
        # Get all joblist-item elements
        items = page.query_selector_all('.joblist-item')
        print(f"Found {len(items)} job items")
        
        for item in items:
            try:
                # Extract sensorsdata JSON
                sensorsdata = item.get_attribute('sensorsdata')
                if not sensorsdata:
                    continue
                
                # Parse JSON
                data = json.loads(sensorsdata)
                title = data.get('jobTitle', '')
                salary = data.get('jobSalary', '')
                area = data.get('jobArea', '')
                company = data.get('companyName', '')  # might not exist
                job_id = data.get('jobId', '')
                
                if not title or title in seen:
                    continue
                seen.add(title)
                
                # Construct URL
                job_url = f"https://jobs.51job.com/pc/search?jobArea=&amp;keyword=AI&amp;ord_field=0&amp;searchType=2&amp;appid=0&amp;functionDomain=&amp;workPlace={area}&amp;jobArea={area}"
                
                jobs.append({
                    'title': title[:100],
                    'url': job_url,
                    'source': '51job',
                    'category': 'job_news',
                    'time': '',
                    'summary': f"{area} | {salary}" if salary else area
                })
                print(f"  {title[:50]} | {area} | {salary}")
                
            except Exception as e:
                pass
        
        print(f"\nExtracted {len(jobs)} jobs")
        
        with open('jobs_51job.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        
        browser.close()
        return jobs

if __name__ == '__main__':
    extract_jobs()
