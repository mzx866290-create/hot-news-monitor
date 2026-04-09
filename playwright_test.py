from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_job_sites():
    with sync_playwright() as p:
        # Launch chromium
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-blink-features=AutomationControlled'])
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        )
        
        sites = [
            ('51job', 'https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1'),
            ('智联', 'https://sou.zhaopin.com/?jl=763&kw=AI&kt=3'),
            ('Boss', 'https://www.zhipin.com/web/geek/job?query=AI&city=101280900'),
        ]
        
        for name, url in sites:
            print(f'\n=== Testing {name} ===')
            page = context.new_page()
            try:
                response = page.goto(url, timeout=15000, wait_until='domcontentloaded')
                print(f'Status: {response.status if response else "No response"}')
                content = page.content()
                print(f'Content length: {len(content)}')
                
                # Check for verification
                if '验证' in content[:1000] or '滑动' in content[:1000]:
                    print('BLOCKED by verification')
                else:
                    print('GOT content!')
                    # Try to find job listings
                    if 'job' in content.lower() or '职位' in content:
                        print('Found job-related content')
                        
            except PlaywrightTimeout:
                print(f'{name}: TIMEOUT')
            except Exception as e:
                print(f'{name}: ERROR {e}')
            finally:
                page.close()
        
        browser.close()

if __name__ == '__main__':
    test_job_sites()
