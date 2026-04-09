"""Quick test of the hot news frontend"""
from app import app

with app.test_client() as client:
    # Test frontend HTML
    html_resp = client.get('/')
    html = html_resp.data.decode('utf-8')

    checks = [
        ("category === 'ai_news'", "JS filter: ai_news"),
        ("category === 'job_news'", "JS filter: job_news"),
        ("categoryLabel", "JS categoryLabel var"),
    ]

    all_ok = True
    for pattern, desc in checks:
        if pattern in html:
            print(f'OK: {desc}')
        else:
            print(f'FAIL: {desc}')
            all_ok = False

    # Test API endpoint (cache might be empty but endpoint should work)
    api_resp = client.get('/api/news')
    import json
    data = json.loads(api_resp.data)
    print(f'\nAPI: {len(data["ai_news"])} AI news, {len(data["job_news"])} jobs (cache may be empty in test mode)')

    if all_ok:
        print('\n✅ Frontend HTML contains correct JS filters!')
    else:
        print('\n❌ Frontend has issues')
