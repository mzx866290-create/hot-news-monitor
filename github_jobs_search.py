import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# Search for specific known repos related to Chinese job sites
repos = [
    ('BossZP', 'PandyGithub/BossZP'),
    ('spider_reverse', '0xAllenChen/spider_reverse'),
    ('zhaopin-spider', 'w392807148/zhaopin-spider'),
    ('zhilian-spider', 'python-s上游/zhiilian-spider'),
    ('51job-spider', 'Chy監督者/51jobSpider'),
]

for name, repo in repos:
    try:
        # Get repo info
        r = requests.get(f'https://api.github.com/repos/{repo}', timeout=10)
        if r.status_code == 200:
            data = r.json()
            desc = data.get('description', '') or ''
            stars = data.get('stargazers_count', 0)
            lang = data.get('language', '') or ''
            print(f'{name}: {stars} stars, {lang}')
            print(f'  {data.get("html_url")}')
            if desc:
                print(f'  {desc[:150]}')
            
            # Get README
            for readme in ['README.md', 'README_CN.md', 'readme.md']:
                r2 = requests.get(f'https://raw.githubusercontent.com/{repo}/main/{readme}', timeout=10)
                if r2.status_code == 200:
                    print(f'  README ({readme}):')
                    print(f'  {r2.text[:500]}')
                    break
        else:
            print(f'{name}: HTTP {r.status_code}')
        print()
    except Exception as e:
        print(f'{name}: ERROR {e}')
        print()
