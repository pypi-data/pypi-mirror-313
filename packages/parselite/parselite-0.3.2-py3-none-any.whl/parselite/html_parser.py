import asyncio
import re
from functools import lru_cache

import aiohttp
import trafilatura
from bs4 import BeautifulSoup


class FastHTMLParserV3:
    @lru_cache
    async def _fetch_url(self, session, url, url_fetch_timeout=10):
        if self._is_avoid_urls(url):
            return ""
        try:
            async with session.get(url, timeout=url_fetch_timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._process_trafili_html(html)
                else:
                    # print(f"Error fetching {url}: HTTP status {response.status}")
                    return ""
        except aiohttp.ClientConnectorError as e:
            print(f"Connection error for {url}: {str(e)}")
            return ""
        except asyncio.TimeoutError:
            print(f"Timeout error for {url}")
            return ""
        except Exception as e:
            print(f"Unexpected error fetching {url}: {str(e)}")
            return ""


    async def fetch_content(self,urls,url_fetch_timeout=10):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch_url(session, url,url_fetch_timeout) for url in urls]
            return await asyncio.gather(*tasks)
                # return [result for result in await asyncio.gather(*tasks) if result]


    def _is_avoid_urls(self,url):
        if "https://arxiv.org/pdf" in url.lower() or url.endswith(".pdf") or "youtube.com/watch" in url.lower():
            return True
        return False

    def _process_trafili_html(self, html):
        text = trafilatura.extract(html, include_formatting=True)
        return text