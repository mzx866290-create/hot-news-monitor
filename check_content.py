import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
}

# Check 智联
print('=== 智联 ===')
r = requests.get('https://sou.zhaopin.com/?jl=763&kw=AI&kt=3', headers=headers, timeout=10)
print(f'Status: {r.status_code}, Length: {len(r.text)}')
with open('zhaopin_content.txt', 'w', encoding='utf-8') as f:
    f.write(r.text)
print('Saved to zhaopin_content.txt')

# Check Boss
print('\n=== Boss ===')
r2 = requests.get('https://www.zhipin.com/web/geek/job?query=AI&city=101280900', headers=headers, timeout=10)
print(f'Status: {r2.status_code}, Length: {len(r2.text)}')
with open('boss_content.txt', 'w', encoding='utf-8') as f:
    f.write(r2.text)
print('Saved to boss_content.txt')

# Check 51job RSS
print('\n=== 51job RSS ===')
r3 = requests.get('https://search.51job.com/rss/760000.txt', headers=headers, timeout=10)
print(f'Status: {r3.status_code}, Length: {len(r3.text)}')
with open('51job_rss.txt', 'w', encoding='utf-8') as f:
    f.write(r3.text)
print('Saved to 51job_rss.txt')
