"""Debug test for hot news frontend"""
import requests

# Test API
r = requests.get('http://127.0.0.1:5000/api/news', timeout=5)
data = r.json()
allNews = data.get('ai_news', []) + data.get('job_news', [])
ai_count = len([n for n in allNews if n.get('category') == 'ai_news'])
job_count = len([n for n in allNews if n.get('category') == 'job_news'])
last_update = data.get('last_update')

print(f"API: Total={len(allNews)}, AI={ai_count}, Jobs={job_count}")
print(f"Update: {last_update}")
print()

# Check HTML
html_r = requests.get('http://127.0.0.1:5000/', timeout=5)
html = html_r.text

checks = {
    'allNews = [...(result.ai_news': 'Spread operator fix (result.ai_news)',
    "category === 'ai_news'": 'Category filter uses ai_news',
    'result.last_update': 'Uses result.last_update (not timestamp)',
}
for pattern, desc in checks.items():
    found = pattern in html
    print(f"{desc}: {'OK' if found else 'MISSING'}")

# Check OLD bad patterns
if 'result.success' in html:
    print("result.success: STILL PRESENT (should be removed)")
if '/api/refresh' in html:
    print("/api/refresh: STILL REFERENCED (should be removed)")
