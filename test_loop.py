"""
循环测试脚本 - 每5分钟检测一次服务状态
"""
import requests
import time
import json
from datetime import datetime

FLASK_URL = "http://127.0.0.1:5000/api/news"
TEST_INTERVAL = 300  # 5分钟


def check_flask():
    """检查 Flask 服务"""
    try:
        r = requests.get(FLASK_URL, timeout=10)
        data = r.json()
        return {
            'ok': True,
            'ai_news': len(data.get('ai_news', [])),
            'job_news': len(data.get('job_news', [])),
            'last_update': data.get('last_update', 'N/A')
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def check_jina():
    """检查 Jina 招聘提取"""
    import requests
    try:
        headers = {'Accept': 'text/plain', 'X-Return-Format': 'text'}
        url = 'https://sou.zhaopin.com/?jl=763&kw=AI'
        r = requests.get(f'https://r.jina.ai/{url}', headers=headers, timeout=15)
        if r.status_code == 200:
            text = r.text
            lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 4]
            job_lines = [l for l in lines if any(kw in l for kw in ['AI', '人工智能', '工程师', '开发', '实习', '元/月', 'K·'])]
            return {'ok': True, 'total_lines': len(lines), 'job_lines': len(job_lines), 'sample': text[50:150]}
        else:
            return {'ok': False, 'status': r.status_code}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def main():
    print(f"循环测试开始 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 立即测试一次
    print("\n[Flask API]")
    result = check_flask()
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n[Jina 提取]")
    result2 = check_jina()
    print(json.dumps(result2, ensure_ascii=False, indent=2))

    print("\n" + "=" * 60)
    print(f"下次测试: {TEST_INTERVAL//60} 分钟后")
    print("按 Ctrl+C 停止")


if __name__ == '__main__':
    main()
