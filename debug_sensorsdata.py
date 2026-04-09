from playwright.sync_api import sync_playwright
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

def debug():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.new_page()
        
        url = "https://we.51job.com/pc/search?jobarea=760000&curr_page=1&keyword=AI&searchType=2&sortType=0"
        page.goto(url, timeout=20000, wait_until="networkidle")
        page.wait_for_selector('.joblist', timeout=10000)
        
        items = page.query_selector_all('.joblist-item')
        print(f"Found {len(items)} job items")
        
        # Check first item
        item = items[0]
        attrs = item.evaluate('el => Object.keys(el.attributes).map(k => ({key: k, value: el.attributes[k]?.value || el.attributes[k]?.nodeValue}))')
        print(f"\nFirst item attributes:")
        for a in attrs[:10]:
            print(f"  {a}")
        
        # Try to get sensorsdata
        sensorsdata = item.get_attribute('sensorsdata')
        print(f"\nSensorsdata type: {type(sensorsdata)}")
        print(f"Sensorsdata length: {len(sensorsdata) if sensorsdata else 0}")
        print(f"Sensorsdata preview: {sensorsdata[:200] if sensorsdata else 'None'}")
        
        # Try data-v-* attributes
        data_attrs = item.evaluate('el => { const attrs = {}; for(const attr of el.attributes) attrs[attr.name] = attr.value; return attrs; }')
        print(f"\nAll attributes: {json.dumps(data_attrs, ensure_ascii=False)[:500]}")
        
        browser.close()

if __name__ == '__main__':
    debug()
