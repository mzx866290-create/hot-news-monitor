import requests, sys, time
sys.stdout.reconfigure(encoding='utf-8')

queries = [
    'zhaopin scraper python',
    '51job scraper github',
    'boss直聘 python 爬虫', 
    'lagou lagupython scraper',
    'liepin scraper python',
    'zhilianzhaopin python',
    'zhipin python scraper',
]

all_results = []
for q in queries:
    try:
        r = requests.get(
            f'https://api.github.com/search/repositories?q={requests.utils.quote(q)}&sort=stars&per_page=5',
            timeout=10,
            headers={'Accept': 'application/vnd.github.v3+json'}
        )
        if r.status_code == 200:
            data = r.json()
            total = data.get('total_count', 0)
            print(f'{q}: {total} results')
            for item in data.get('items', [])[:3]:
                stars = item.get('stargazers_count', 0)
                if stars > 0:
                    print(f'  {item["full_name"]} stars:{stars} {item["html_url"]}')
                    all_results.append((stars, item['full_name'], item['html_url'], q))
        elif r.status_code == 403:
            print(f'{q}: Rate limited')
            break
        else:
            print(f'{q}: HTTP {r.status_code}')
        time.sleep(1)  # avoid rate limit
    except Exception as e:
        print(f'{q}: ERROR {e}')

print('\n=== Top Results ===')
all_results.sort(reverse=True)
for stars, name, url, q in all_results[:10]:
    print(f'{name} (stars:{stars}) - {url}')
