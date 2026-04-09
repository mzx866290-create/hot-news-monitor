import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get('https://we.51job.com/api/job/search-pc?api_key=5Fz&search_keys=AI&search_area=7600000&page=1&sort=0', headers=headers, timeout=10)
print('Status:', r.status_code, 'Size:', len(r.text))

# Check if HTML or JSON
if r.text.strip().startswith('{'):
    data = r.json()
    print('Is JSON: True')
    print('Keys:', list(data.keys())[:10])
    if 'resultbody' in data:
        body = data['resultbody']
        print('resultbody keys:', list(body.keys()) if isinstance(body, dict) else 'list')
else:
    print('Response is HTML, not JSON')
    with open('51job_response.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    print('Saved to 51job_response.html')
