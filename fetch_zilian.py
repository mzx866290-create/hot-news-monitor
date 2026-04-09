import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# Get the Zhilian_Scraper repo
r = requests.get('https://api.github.com/repos/Aruomeng/Zhilian_Scraper', timeout=10)
if r.status_code == 200:
    data = r.json()
    print('Zhilian_Scraper:')
    print(f'  Stars: {data.get("stargazers_count")}')
    print(f'  Language: {data.get("language")}')
    print(f'  URL: {data.get("html_url")}')
    print(f'  Description: {data.get("description")}')
    
    # Get contents
    r2 = requests.get('https://api.github.com/repos/Aruomeng/Zhilian_Scraper/contents', timeout=10)
    if r2.status_code == 200:
        contents = r2.json()
        print('\n  Files:')
        for item in contents:
            print(f'    {item["name"]} ({item["type"]})')
