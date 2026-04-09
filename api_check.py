import requests, json

r = requests.get('http://127.0.0.1:5000/api/news', timeout=10)
data = r.json()

with open('D:/Apps/hot-news-monitor/flask_api_check.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Saved {len(data["ai_news"])} AI news and {len(data["job_news"])} jobs')
if data['job_news']:
    print('First 3 jobs:')
    for item in data['job_news'][:3]:
        # Save raw bytes to verify encoding
        title_bytes = item['title'].encode('utf-8')
        print(f'  Title bytes: {title_bytes[:30]}')
        print(f'  Title chars: {item["title"]}')
