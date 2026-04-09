import requests, json

headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}
url = 'https://sou.zhaopin.com/?jl=763&kw=AI'
r = requests.get(f'https://r.jina.ai/{url}', headers=headers, timeout=15)

print(f'Status: {r.status_code}')
print(f'Encoding: {r.encoding}')
print(f'Content-Type: {r.headers.get("content-type", "")}')
print(f'Raw bytes[:30]: {r.content[:30]}')

text = r.text
print(f'Text length: {len(text)}')
print(f'Text[:100]: {repr(text[:100])}')

# Try to fix encoding
# Check if it's double-encoded
try:
    # Try UTF-8 first
    t1 = text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
    print(f'UTF-8 decode OK, chars: {len(t1)}')
    print(f'Sample: {t1[50:150]}')
except Exception as e:
    print(f'UTF-8 failed: {e}')

# Save raw response
with open('D:/Apps/hot-news-monitor/jina_debug.txt', 'w', encoding='utf-8') as f:
    f.write(f'Status: {r.status_code}\n')
    f.write(f'Encoding: {r.encoding}\n')
    f.write(f'Content-Type: {r.headers.get("content-type", "")}\n')
    f.write(f'Raw bytes:\n{r.content[:200]}\n\n')
    f.write(f'Text:\n{text[:3000]}\n')
print('Saved to jina_debug.txt')
