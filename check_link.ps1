with open(r'D:\Apps\hot-news-monitor\templates\index.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('Has clickable link:', '<a href=' in c and 'target="_blank"' in c)
print('news.url used:', 'news.url' in c)
