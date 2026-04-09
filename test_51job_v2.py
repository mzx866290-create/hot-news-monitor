import requests, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get('https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1&sort=0', headers=headers, timeout=10)
print('Status:', r.status_code, 'Size:', len(r.text))
print('Is JSON:', r.text.strip().startswith('{'))

# Save response
filepath = r'D:\Apps\hot-news-monitor\51job_response.html'
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(r.text)
print('Saved to', filepath)
