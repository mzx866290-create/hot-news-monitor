import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}

# Try RSS feeds for jobs
rss_urls = [
    ('LinkedIn RSS alternative', 'https://r.jina.ai/https://www.linkedin.com/jobs/search/?keywords=AI&location=Zhuhai%2C%20China'),
    ('Indeed RSS', 'https://r.jina.ai/https://cn.indeed.com/rss?q=AI&l=Zhuhai'),
    ('SimplyHired', 'https://r.jina.ai/https://www.simplyhired.com/search?q=AI&l=Zhuhai'),
    ('GitHub Jobs alternative', 'https://r.jina.ai/https://github.com/settings/stored?type=jobs'),
]

for name, url in rss_urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if len(r.text) > 30:
            print(f'  OK')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()

# Try Jina with different approach - raw content extraction
raw_urls = [
    ('招聘导航', 'https://r.jina.ai/https://www.zhaopin.com/'),
    ('中国人才热线', 'https://r.jina.ai/https://www.jobcn.com/search/result.cfm?keyword=AI&location=zhuhai'),
]

for name, url in raw_urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if len(r.text) > 30:
            print(f'  OK')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()
