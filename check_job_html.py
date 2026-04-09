from playwright.sync_api import sync_playwright
import sys
sys.stdout.reconfigure(encoding='utf-8')

def check_job_html():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        # Get the joblist element HTML
        joblist = page.query_selector('.joblist')
        if joblist:
            html = joblist.inner_html()
            with open('joblist.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Saved joblist HTML ({len(html)} chars)")
            print(f"\nFirst 2000 chars of joblist HTML:\n{html[:2000]}")
        else:
            print("No .joblist found")
        
        # Check page inner text for job titles
        text = page.inner_text('body')
        # Look for lines with common job title keywords
        lines = text.split('\n')
        job_lines = []
        for line in lines:
            line = line.strip()
            if line and any(kw in line for kw in ['工程师', '算法', '开发', '数据', 'AI', '机器学习', '分析师', '研究员', '架构']):
                if len(line) > 4 and len(line) < 60:
                    job_lines.append(line)
        
        print(f"\nJob title lines ({len(job_lines)}):")
        for l in job_lines[:15]:
            print(f"  {l}")
        
        browser.close()

if __name__ == '__main__':
    check_job_html()
