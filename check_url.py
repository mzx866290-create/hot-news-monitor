import requests
r = requests.get('http://127.0.0.1:5000/api/news', timeout=5)
data = r.json()
print('=== AI News URLs ===')
for n in data['ai_news'][:3]:
    print('title:', n['title'][:50])
    print('url:', n['url'])
    print()
print('=== Job News URLs ===')
for n in data['job_news'][:3]:
    print('title:', n['title'][:50])
    print('url:', n['url'])
