from playwright.sync_api import sync_playwright
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

def extract_jobs():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        jobs = []
        
        # Get all elements with 'job' in class
        job_elements = page.query_selector_all('[class*="job"]')
        
        for elem in job_elements[:30]:
            try:
                text = elem.inner_text()
                html = elem.inner_html()
                
                # Skip small elements (badges, tags, etc)
                if len(text) < 20:
                    continue
                
                # Try to find link (job title is usually in an <a> tag)
                link_elem = elem.query_selector('a')
                if link_elem:
                    title = link_elem.inner_text().strip()
                    href = link_elem.get_attribute('href') or ''
                else:
                    # Try first text-heavy element
                    title = text.split('\n')[0].strip()
                    href = ''
                
                # Clean up title
                title = re.sub(r'\s+', ' ', title).strip()
                
                # Skip if too short or looks like a tag
                if len(title) < 5 or title in ['AI', '职位', '招聘']:
                    continue
                
                # Extract salary if present
                salary_match = re.search(r'([\d\.]+-[❯\d\.]+[万/kK·]*|[\d]+-[❯\d]+[kK]*)', text)
                salary = salary_match.group(0) if salary_match else ''
                
                # Extract area
                area_match = re.search(r'(上海|北京|广州|深圳|中山|珠海|东莞|佛山|武汉|杭州|南京|成都|重庆|[^\\s]{2,6})\s*$', text.split('\n')[0])
                area = area_match.group(1) if area_match else ''
                
                jobs.append({
                    'title': title[:100],
                    'salary': salary,
                    'area': area,
                    'url': href,
                    'source': '51job',
                    'category': 'job_news',
                    'time': '',
                    'summary': text[:150]
                })
                print(f"[{len(jobs):2d}] {title[:50]} | {salary}")
                
            except Exception as e:
                pass
        
        print(f"\nTotal extracted: {len(jobs)} jobs")
        
        import json
        with open('extracted_jobs.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        print("Saved to extracted_jobs.json")
        
        browser.close()

if __name__ == '__main__':
    extract_jobs()
