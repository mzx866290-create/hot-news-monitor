# -*- coding: utf-8 -*-
"""
Standalone 51job scraper - runs as separate process
Saves results to jobs.json, Flask reads from there
"""
import json
import logging
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def scrape_51job():
    news = []
    seen = set()

    for attempt in range(3):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-setuid-sandbox']
                )
                page = browser.new_page()
                page.set_default_timeout(30000)

                url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
                logger.info(f'51job: navigating to {url}')
                page.goto(url, timeout=30000, wait_until="networkidle")

                # Wait for job list
                try:
                    page.wait_for_selector('.joblist', timeout=15000)
                except:
                    page.wait_for_selector('.j_joblist', timeout=15000)

                import time
                time.sleep(2)

                # Try different selectors
                items = page.query_selector_all('.joblist-item')
                if not items:
                    items = page.query_selector_all('.j_joblist > div')

                logger.info(f'51job: found {len(items)} items (attempt {attempt+1})')

                for item in items:
                    try:
                        text = item.inner_text()
                        lines = [l.strip() for l in text.split('\n') if l.strip()]
                        title = lines[0] if lines else ''
                        if not title or len(title) < 5 or title in seen:
                            continue
                        seen.add(title)

                        salary = ''
                        area = ''
                        for line in lines:
                            if '万' in line or '千' in line or '元' in line:
                                salary = line
                            elif any(city in line for city in ['中山', '珠海', '广州', '深圳', '东莞', '佛山']):
                                area = line

                        news.append({
                            'title': title[:100],
                            'url': 'https://we.51job.com',
                            'source': '51job',
                            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'category': 'job_news',
                            'summary': f"{area} | {salary}" if area or salary else title
                        })
                    except Exception as e:
                        pass

                browser.close()

                if news:
                    logger.info(f'51job: SUCCESS extracted {len(news)} jobs')
                    break
                else:
                    logger.warning(f'51job: 0 jobs, retrying...')
        except Exception as e:
            logger.error(f'51job attempt {attempt+1} failed: {e}')

    # Save to file
    with open('jobs.json', 'w', encoding='utf-8') as f:
        json.dump({'jobs': news, 'updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'count': len(news)}, f, ensure_ascii=False)
    logger.info(f'Saved {len(news)} jobs to jobs.json')
    return news

if __name__ == '__main__':
    scrape_51job()
