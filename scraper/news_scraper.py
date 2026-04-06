import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from datetime import datetime, timezone, date
from storage import save_to_json
from deduplicator import filter_new

load_dotenv()

async def scrape_finviz_news() -> list[dict]:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = True)
        page = await browser.new_page()

        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        print("[scraper] Navigating to Finviz...")
        await page.goto("https://finviz.com/news.ashx", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        rows = await page.query_selector_all("tr.news_table-row")
        for row in rows:
            time_cell = await row.query_selector("td.news_date-cell")
            link_cell = await row.query_selector("td.news_link-cell a")

            if time_cell and link_cell:
                time_text = await time_cell.inner_text()
                headline = await link_cell.inner_text()
                url = await link_cell.get_attribute("href")

                results.append({
                    "headline": headline.strip(),
                    "url" : url,
                    "time_raw" : time_text.strip(),
                    "published_at" : f"{date.today().isoformat()} {time_text.strip()}",
                    "scraped_at" : datetime.now(timezone.utc).isoformat()
                    #"scraped_at" : datetime.now(datetime.UTC).isoformat()
                })
        await browser.close()
    return results

async def main():
    news = await scrape_finviz_news()
    if not news:
        print("[scraper] No results found. Site structure may have changed.")
        return
    print(f"[scraper] Fetched {len(news)} headlines\n")
    new_news = filter_new(news)
    if not new_news:
        print("[scraper] No new headlines to save.")
        return
    
    for item in news[:5]:
        print(f"   [{item['published_at']}]  {item['headline']}")
        print(f"   -> {item['url']}\n")
    save_to_json(news)

# if __name__ == "__main__":
#     asyncio.run(main())

async def debug_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        await page.goto("https://finviz.com/news.ashx", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        # Dump the raw HTML so we can see the actual structure
        html = await page.content()
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("[debug] Saved page HTML to debug_page.html")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())