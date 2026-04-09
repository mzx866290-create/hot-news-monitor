import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

# Try different approaches for job sites
tests = [
    # Direct pages
    ('51job search', 'https://search.51job.com/list/760000,000000,0000,00,9,99,AI,2,1.html'),
    ('智联 search', 'https://sou.zhaopin.com/?jl=763&kw=AI&kt=3'),
    ('Boss search', 'https://www.zhipin.com/web/geek/job?query=AI&city=101280900'),
    # RSS feeds
    ('51job RSS', 'https://search.51job.com/rss/760000.txt'),
    # Alternative job aggregators
    ('Jooble', 'https://cn.jooble.org RSS'),
]

for name, url in tests:
    try:
        if 'RSS' in name and 'jooble' in url:
            r = requests.get('https://cn.jooble.org/rss/?l=Zhuhai&q=AI', headers=headers, timeout=10)
        else:
            r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if r.status_code == 200 and len(r.text) > 100:
            # Check if it's not a verification page
            if '验证' not in r.text[:500] and '请滑动' not in r.text[:500]:
                print(f'  OK - got content')
            else:
                print(f'  Blocked by verification')
        print()
        time.sleep(0.5)
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()
