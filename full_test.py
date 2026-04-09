import requests

# 1. Check API
r = requests.get('http://127.0.0.1:5000/api/news', timeout=5)
data = r.json()
print("API AI:", len(data['ai_news']), "Jobs:", len(data['job_news']))
print("Update:", data['last_update'])

# 2. Simulate JS logic
allNews = (data.get('ai_news') or []) + (data.get('job_news') or [])
ai_filtered = [n for n in allNews if n.get('category') == 'ai_news']
print("Combined:", len(allNews), "AI filtered:", len(ai_filtered))

# 3. Check HTML
html_r = requests.get('http://127.0.0.1:5000/', timeout=5)
html = html_r.text
print("HTML size:", len(html))

old_success = 'result.success' in html
has_url_link = 'news.url' in html and '<a href=' in html
has_ai_filter = "category === 'ai_news'" in html
print("OLD result.success:", old_success)
print("Has news.url link:", has_url_link)
print("Has ai_news filter:", has_ai_filter)

# 4. First item link
first = allNews[0] if allNews else None
if first:
    print("First URL:", first.get('url'))
    print("First title:", first.get('title')[:40])
