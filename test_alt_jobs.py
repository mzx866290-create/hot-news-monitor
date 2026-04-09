import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}

# Try other Chinese job sites that might not be blocked
alt_sites = [
    ('中国人才热线', 'https://r.jina.ai/https://www.jobcn.com/search/result.cfm?keyword=AI&location=zhuhai'),
    ('中国就业网', 'https://r.jina.ai/https://www.chinahr.com/sitehtml/1026/html/sou.html?keyWord=AI&cityCategory=province&cityCode=44&page=1'),
    ('卓博', 'https://r.jina.ai/https://www.zhaobiao.cn/zt/AI-jobs/'),
    ('百才', 'https://r.jina.ai/https://www.baicai.com/'),
    ('英才网', 'https://r.jina.ai/https://www.chinahr.com/sitehtml/1026/html/sou.html?keyWord=AI'),
]

for name, url in alt_sites:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{name}: {r.status_code} len={len(r.text)}')
        if r.status_code == 200 and len(r.text) > 100:
            if '验证' not in r.text[:200] and '登录' not in r.text[:200]:
                print(f'  OK')
            else:
                print(f'  Blocked')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()
