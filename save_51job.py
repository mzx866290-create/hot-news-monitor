import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# Save 51job RSS v2
r = requests.get('https://we.51job.com/rss/760000%2C000000%2C0000%2C00%2C9%2C99%2CAI%2C2%2C1.html', timeout=10)
with open('51job_rss_v2.xml', 'w', encoding='utf-8') as f:
    f.write(r.text)
print('51job RSS v2 saved:', len(r.text), 'chars')
print('First 500 chars:')
print(r.text[:500])
