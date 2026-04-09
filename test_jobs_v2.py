import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/plain',
    'X-Return-Format': 'text'
}

sources = [
    ('拉勾网', 'https://r.jina.ai/https://www.lagou.com/jobs/list_AI?px=new&city=%E7%8F%9E%E5%90%88'),
    ('智联招聘', 'https://r.jina.ai/https://sou.zhaopin.com/?jl=763&kw=AI'),
    ('Boss直聘', 'https://r.jina.ai/https://www.zhipin.com/web/geek/job?query=AI&city=101280900'),
    ('猎聘', 'https://r.jina.ai/https://www.liepin.com/so/?key=AI&city=030200'),
]

for name, url in sources:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if len(r.text) > 20:
            print(f'  Sample: {r.text[:100]}')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()
