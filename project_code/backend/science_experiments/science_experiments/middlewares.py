# Author: Marco Biasion <marco.biasion@usi.ch>

import ipaddress
from typing import Optional
import scrapy
import scrapy.signals
import scrapy.http
from urllib.parse import urlparse
import os
import os.path


class CacheMiddleware:
    _local_cache_path = 'cache'
    _local_host = ipaddress.IPv4Address('127.0.0.1')

    @classmethod
    def local_path(cls, url) -> str:
        url = urlparse(url)

        site_path = '/'.join(url.netloc.split('.')[::-1])
        insite_path = url.path.strip('/')
        query = f'?{url.query}' if url.query else ''
        return f'{cls._local_cache_path}/{site_path}/-/{insite_path}{query}'

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=scrapy.signals.spider_opened)
        return s

    def process_request(self,
                        request: scrapy.http.Request,
                        spider: scrapy.Spider) -> Optional[scrapy.http.TextResponse]:
        """Load the response locally if it was cached.

        Args:
            request (Request): The original request.
            spider (Spider): The spider managing the crawling.

        Returns:
            Optional(TextResponse): The response if the page response was cached.
        """

        file_path = self.local_path(request.url)

        # check if response is cached
        if not os.path.isfile(file_path):
            return None

        # read file
        with open(file_path, 'r') as f:
            body = f.read()

        # return cached response
        return scrapy.http.TextResponse(
            url=request.url,
            status=200,
            headers=None,
            body=body,
            encoding='utf-8',
            flags=None,
            request=request,
            certificate=None,
            ip_address=self._local_host,
            protocol=None
        )

    def process_response(self,
                         request: scrapy.http.Request,
                         response: scrapy.http.TextResponse,
                         spider: scrapy.Spider) -> scrapy.http.TextResponse:
        """Save the response body if it came from a server.

        Args:
            request (Request): The original request.
            response (Response): The response to possibly save.
            spider (Spider): The spider managing the crawling.

        Returns:
            TextResponse: The response as it was given to the function.
        """

        # response is coming from the cache, skip
        if response.ip_address == self._local_host:
            return response

        file_path = self.local_path(request.url)

        # create folder/s (if missing)
        folder_path, file_name = file_path.rsplit('/', 1)
        os.makedirs(folder_path, exist_ok=True)

        # write file
        with open(file_path, 'w') as f:
            f.write(response.text)

        return response

    def spider_opened(self, spider):
        spider.logger.info(f'Spider opened: {spider.name}')