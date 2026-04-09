import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')

headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}

# Try Indeed RSS (they have a working RSS)
indeed_urls = [
    ('Indeed Zhuhai AI', 'https://r.jina.ai/https://cn.indeed.com/rss?q=AI&l=Zhuhai&sort=date'),
    ('Indeed Guangzhou AI', 'https://r.jina.ai/https://cn.indeed.com/rss?q=AI&l=Guangzhou&sort=date'),
    ('Indeed Shenzhen AI', 'https://r.jina.ai/https://cn.indeed.com/rss?q=AI&l=Shenzhen&sort=date'),
    # Direct Indeed RSS (without Jina)
    ('Indeed Direct RSS', 'https://cn.indeed.com/rss?q=AI&l=Zhuhai&sort=date'),
]

for name, url in indeed_urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if r.status_code == 200 and len(r.text) > 50:
            print(f'  Content preview: {r.text[:200]}')
        print()
        time.sleep(0.3)
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()

# Try Jina's newer API
print('\n=== Jina AI Reader API ===')
jina_reader_urls = [
    'https://r.jina.ai/https://www.zhaopin.com/',
    'https://r.jina.ai/https://we.51job.com/',
    'https://r.jina.ai/https://sou.zhaopin.com/',
]
for url in jina_reader_urls:
    site = url.split('/')[-1]
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{site}: {r.status_code} len={len(r.text)}')
        if len(r.text) > 30:
            print(f'  Preview: {r.text[:150]}')
        print()
        time.sleep(0.3)
    except Exception as e:
        print(f'{site}: ERROR {e}')
        print()
