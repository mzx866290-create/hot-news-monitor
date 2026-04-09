# -*- coding: utf-8 -*-
"""
Hot News Monitor - Flask Backend
Reads AI/编程 news via Jina AI
Reads job data from jobs.json (written by scrape_51job.py)
"""
import json, logging, os, re, subprocess, time, requests
from datetime import datetime
from flask import Flask, render_template, jsonify, make_response
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
news_cache = {'ai_news': [], 'job_news': [], 'last_update': None}
refresh_thread = None


def load_jobs():
    """Load 51job data from scrape_51job.py output file"""
    fpath = os.path.join(SCRIPT_DIR, 'jobs.json')
    if os.path.exists(fpath):
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
            age = (datetime.now() - mtime).total_seconds()
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            jobs = data.get('jobs', [])
            updated = data.get('updated', '')
            logger.info(f'Loaded {len(jobs)} jobs from jobs.json (updated {updated}, age {age:.0f}s)')
            return jobs
        except Exception as e:
            logger.warning(f'Failed to load jobs.json: {e}')
    return []


def fetch_ai_news():
    """Fetch AI/编程 news via Jina AI content extraction"""
    AI_SOURCES = [
        ('机器之心', 'https://jiqizhixin.com'),
        ('36氪', 'https://36kr.com'),
        ('虎嗅', 'https://www.huxiu.com'),
        ('品玩', 'https://www.pingwest.com'),
        ('Solidot', 'https://www.solidot.org'),
        ('新智元', 'https://yuanzibo.com'),
        ('Hacker News', 'https://news.ycombinator.com'),
        ('DEV Community', 'https://dev.to'),
        ('Product Hunt', 'https://producthunt.com'),
    ]

    AI_KEYWORDS = [
        'AI', '大模型', 'GPT', 'Claude', 'Gemini', 'Llama', '开源', '发布', '训练', '模型',
        '算法', 'ChatGPT', 'Copilot', 'LangChain', 'RAG', 'GPU', '英伟达', 'AMD', '芯片',
        '深度学习', '神经网络', '推理', 'AGI', 'Sora', '文生', '多模态', 'Agent',
        'embedding', '微调', 'SOTA', '评测', '超越', '全球', '中国', '阿里', '百度',
        '华为', '字节', '腾讯', 'OpenAI', 'Anthropic', 'Google', 'Meta', 'Mistral', 'DeepSeek',
        'Kimi', '豆包', '通义', '文心', '智谱', 'Gemini', 'ChatGPT', 'o1', 'o3', 'Grok'
    ]
    SKIP_WORDS = ['首页', '最新', '热门', '关于', '联系', '登录', '注册', '收藏', '分享',
                  '评论', '关闭', '打开', '更多', '导航', '菜单', '相关', '推荐',
                  'AI新闻', '科技资讯', '实时要闻', '查看详情', '点击查看', '阅读更多']

    seen = set()
    source_items = {}

    def fetch_single_source(name, url):
        """Fetch and parse a single news source - runs in parallel"""
        try:
            headers = {
                'Accept': 'text/plain',
                'X-Return-Format': 'text',
                'User-Agent': 'Mozilla/5.0 (compatible; NewsMonitor/1.0)'
            }
            resp = requests.get(f'https://r.jina.ai/{url}', headers=headers, timeout=20)
            if resp.status_code == 200:
                text = resp.text
                if isinstance(text, bytes):
                    text = text.decode('utf-8', errors='replace')
                lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]
                items = []
                for line in lines:
                    if any(kw in line for kw in AI_KEYWORDS):
                        clean = re.sub(r'[#*🎯💼🔥🎓💰🔍🚀\d+年\d+月\d+日\d+:\d+]+', '', line)
                        clean = re.sub(r'\s+', ' ', clean).strip()
                        if (clean and clean not in seen and 6 < len(clean) < 250
                                and not any(sw in clean for sw in SKIP_WORDS)):
                            seen.add(clean)
                            item = {'title': clean[:150], 'url': url, 'source': name,
                                    'time': datetime.now().strftime('%Y-%m-%d %H:%M'), 'category': 'ai_news'}
                            items.append(item)
                logger.info(f'{name}: extracted {len(items)} items via Jina')
                return name, items
        except requests.Timeout:
            logger.warning(f'Jina AI news {name} timeout')
        except requests.RequestException as e:
            logger.warning(f'Jina AI news {name} request failed: {e}')
        except Exception as e:
            logger.warning(f'Jina AI news {name} failed: {e}')
        return name, []

    # Parallel fetch all sources
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_single_source, name, url): name for name, url in AI_SOURCES}
        for future in as_completed(futures):
            name, items = future.result()
            if items:
                source_items[name] = items

    # Interleave from all sources: take up to 3 from each source, then fill remaining
    MAX_PER_SOURCE = 2
    result = []
    for name, _ in AI_SOURCES:
        if name in source_items:
            result.extend(source_items[name][:MAX_PER_SOURCE])

    for name, _ in AI_SOURCES:
        if name in source_items:
            for item in source_items[name][MAX_PER_SOURCE:]:
                if len(result) >= 15:
                    break
                if item not in result:
                    result.append(item)

    logger.info(f'Total AI news extracted: {len(result)}')
    return result[:15]


def refresh():
    """Background: load jobs.json every 5 min, fetch AI news every 5 min"""
    global news_cache
    last_job_refresh = 0
    last_ai_refresh = 0
    consecutive_failures = 0
    max_failures = 3

    while True:
        now = time.time()
        jobs = news_cache.get('job_news', [])

        # Refresh jobs every 5 min
        if now - last_job_refresh > 300:
            jobs = load_jobs()
            last_job_refresh = now
            logger.info(f'Jobs refreshed: {len(jobs)}')

        # Refresh AI news every 5 min
        if now - last_ai_refresh > 300:
            try:
                ai_news = fetch_ai_news()
                consecutive_failures = 0
                last_ai_refresh = now
                news_cache = {
                    'ai_news': ai_news,
                    'job_news': jobs,
                    'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                logger.info(f'Refreshed: {len(ai_news)} AI news, {len(jobs)} jobs')
            except Exception as e:
                consecutive_failures += 1
                logger.error(f'AI news refresh failed ({consecutive_failures}/{max_failures}): {e}')
                if consecutive_failures >= max_failures:
                    logger.warning('Max consecutive failures reached, will keep retrying')
                    consecutive_failures = 0  # Reset to allow continued retries

        time.sleep(30)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/news')
def get_news():
    response = make_response(jsonify(news_cache))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/api/news', methods=['OPTIONS'])
def preflight():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response


@app.route('/api/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'ai_news_count': len(news_cache.get('ai_news', [])),
        'job_news_count': len(news_cache.get('job_news', [])),
        'last_update': news_cache.get('last_update'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


@app.route('/api/refresh', methods=['POST'])
def force_refresh():
    """Force an immediate refresh of news data"""
    global news_cache
    try:
        jobs = load_jobs()
        ai_news = fetch_ai_news()
        news_cache = {
            'ai_news': ai_news,
            'job_news': jobs,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify({'status': 'success', 'message': 'Refreshed', 'counts': {'ai': len(ai_news), 'jobs': len(jobs)}})
    except Exception as e:
        logger.error(f'Force refresh failed: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # Load initial jobs
    initial_jobs = load_jobs()

    # Start background refresh thread
    refresh_thread = Thread(target=refresh, daemon=True, name='news-refresh')
    refresh_thread.start()
    logger.info('Background refresh thread started')

    time.sleep(2)

    # Fetch AI news for the first time in main thread
    try:
        ai_news = fetch_ai_news()
        news_cache = {
            'ai_news': ai_news,
            'job_news': initial_jobs,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        logger.info(f'Initial load: {len(ai_news)} AI news, {len(initial_jobs)} jobs')
    except Exception as e:
        logger.error(f'Initial AI news fetch failed: {e}')
        news_cache = {
            'ai_news': [],
            'job_news': initial_jobs,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    logger.info('Starting Flask server on port 5003...')
    app.run(host='0.0.0.0', port=5003, debug=False, threaded=True)
