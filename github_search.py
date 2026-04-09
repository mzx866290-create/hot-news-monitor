import requests

queries = [
    '51job python scraper',
    'zhaopin python api',
    'boss直聘 python',
    'lagou python scraper',
    'liepin python scraper',
    'job51 python scraper',
    'zhilian zhaopin crawler',
]

for q in queries:
    r = requests.get(f'https://api.github.com/search/repositories?q={q.replace(" ", "+")}+language:python&sort=stars&per_page=3', timeout=10)
    if r.status_code == 200:
        data = r.json()
        if data.get('total_count', 0) > 0:
            print(f'\n=== {q} ({data["total_count"]} results) ===')
            for item in data.get('items', [])[:3]:
                name = item.get('full_name', '')
                stars = item.get('stargazers_count', 0)
                url = item.get('html_url', '')
                print(f'  {name} (stars:{stars}) - {url}')
