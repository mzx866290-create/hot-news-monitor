from playwright.sync_api import sync_playwright
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

def test_51job():
    with sync_playwright() as p:
        # Launch headless browser (won't affect your Chrome)
        browser = p.chromium.launch(headless=True)
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
                # Extract text content
                text = item.inner_text()
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                
                # First non-empty line is usually the job title
                title = lines[0] if lines else ''
                if not title or len(title) < 5 or title in seen:
                    continue
                seen.add(title)
                
                # Try to find salary, area from lines
                salary = ''
                area = ''
                for line in lines:
                    if '万' in line or '千' in line or '元' in line:
                        salary = line
                    elif any(city in line for city in ['中山', '珠海', '广州', '深圳', '东莞', '佛山', '武汉', '杭州', '上海', '北京']):
                        area = line
                
                jobs.append({
                    'title': title[:100],
                    'url': 'https://we.51job.com',
                    'source': '51job',
                    'category': 'job_news',
                    'time': '',
                    'summary': f"{area} | {salary}" if area or salary else title
                })
                print(f"  {title[:50]} | {area} | {salary}")
                
            except Exception as e:
                pass
        
        print(f"\nExtracted {len(jobs)} jobs")
        
        with open('jobs_51job.json', 'w', encoding='utf-8') as f:
            json.dump(jobs, f, ensure_ascii=False, indent=2)
        
        browser.close()

if __name__ == '__main__':
    test_51job()
