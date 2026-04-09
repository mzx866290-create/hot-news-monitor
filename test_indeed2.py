import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}

# Just test Indeed with Jina
r = requests.get('https://r.jina.ai/https://cn.indeed.com/rss?q=AI&l=Zhuhai&sort=date', headers=headers, timeout=10)
print('Indeed Jina:', r.status_code, len(r.text))
print(r.text[:300] if r.status_code == 200 else 'FAILED')
