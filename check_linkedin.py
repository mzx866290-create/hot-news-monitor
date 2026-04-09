import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}

# Check LinkedIn content
r = requests.get('https://r.jina.ai/https://www.linkedin.com/jobs/search/?keywords=AI&location=Zhuhai%2C%20China', headers=headers, timeout=10)
print('LinkedIn content:')
print(r.text[:1000])
print('---')

# Check 招聘导航 content
r2 = requests.get('https://r.jina.ai/https://www.zhaopin.com/', headers=headers, timeout=10)
print('Zhaopin content:')
print(r2.text[:500])
