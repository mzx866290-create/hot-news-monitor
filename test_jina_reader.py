import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# Try jina.ai reader (newer API)
headers = {
    'Accept': 'text/plain',
    'X-Return-Format': 'text'
}

urls = [
    ('51job via jina.ai/reader', 'https://r.jina.ai/https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1'),
    ('Jina reader 51job', 'https://jina.ai/reader/https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1'),
]

for name, url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if len(r.text) > 20:
            print(f'  Sample: {r.text[:150]}')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()

# Try alternative job sites that might not be blocked
alt_sources = [
    ('Indeed China', 'https://r.jina.ai/https://cn.indeed.com/jobs?q=AI&l=Zhuhai'),
    ('Glassdoor China', 'https://r.jina.ai/https://www.glassdoor.com/Job/zhuhai-ai-jobs-SRCH_IL.0,6_IC2728232.htm'),
]

for name, url in alt_sources:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if len(r.text) > 20:
            print(f'  Sample: {r.text[:150]}')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()
