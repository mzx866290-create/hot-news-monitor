import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

queries = ['zhaopin', '51job', 'zhilian', 'bosszhipin', 'liepin', 'lagou']
for q in queries:
    r = requests.get(
        f'https://api.github.com/search/repositories?q={q}+jobs+scraper+language:python&per_page=3',
        timeout=10
    )
    if r.status_code == 200:
        data = r.json()
        count = data.get('total_count', 0)
        if count > 0:
            print(f'\n{q}: {count} repos')
            for item in data['items'][:2]:
                stars = item.get('stargazers_count', 0)
                if stars > 0:
                    desc = item.get('description', '') or ''
                    print(f'  {item["full_name"]} stars:{stars}')
                    print(f'    {desc[:100]}')
                    print(f'    {item.get("html_url","")}')
