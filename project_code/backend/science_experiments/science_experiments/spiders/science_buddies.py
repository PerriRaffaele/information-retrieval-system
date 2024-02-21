from typing import Any
import scrapy
import re
from scrapy.http import Response


# eval "$(/home/gianluca/anaconda3/bin/conda shell.bash hook)"
# conda activate scrapy_env
# scrapy crawl science_buddies -o science_experiments.json

class ScienceBuddiesSpider(scrapy.Spider):

    name = 'science_buddies'

    start_urls = ["https://www.sciencebuddies.org/science-experiments?p=1"]

    def parse(self, response: Response):

        base_url = "https://www.sciencebuddies.org"

        experiment = response.xpath("//div[@class='search-result search-result-grid page-break-avoid']")
        
        links = experiment.xpath(".//div[@class='search-title']/a/@href").extract()
        for link in links:
            if link:
                yield scrapy.Request(url=base_url + link, callback=self.parse_experiment)

        next_page = response.xpath(".//div[@class='pager only-screen']/a[@class='pager-button'][contains(., '>')]")
        if next_page:
            next_page_url = next_page.xpath('@href').extract_first()
            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parse)


    def parse_experiment(self, response: Response):
        title = response.xpath('.//div[@class="main-title"]/div[@class="main-title-left"]/h1/span[@class="title-name"]/text()').get()
        if not title:
            title = response.xpath('.//div[@class="main-title"]/div[@class="main-title-left"]/h1/text()').get()

        subject = response.xpath('.//div[@class="page-break-avoid"]/div[@class="summary"]/div[@class="summary-left"]/div[@class="pi-summary-content"]/a/span[@class="title-name"]/text()').get()
        if not subject:
            subject = ""
        
        target_explanation = response.xpath("//h2[@id='introduction']")
        explanation = ""
        if target_explanation:
            next_h3 = target_explanation.xpath('following::h3[1][contains(.,"Terms and Concepts")]')
            if next_h3:
                explanation = target_explanation.xpath('following-sibling::*[following::h3[1][contains(.,"Terms and Concepts")]]').extract()
            else:
                explanation = target_explanation.xpath('following-sibling::*[following::h2[1][contains(.,"Materials")]]').extract()
             

        clean_explanation = ""
        if explanation:
            for content in explanation:
                clean_text = re.sub('<[^<]+?>', '', content)
                clean_text = clean_text.replace('\r', '').replace('\n', '')
                clean_explanation += clean_text


        target_description = response.xpath("//h2[@id='abstract']")
        description = ""
        if target_description:
            # Select the div with a specific class name
            next_div = target_description.xpath('following::div[@class="page-break-avoid"][1]')
            
            if next_div:
                description = target_description.xpath('following-sibling::node()[following::div[1][@class="page-break-avoid"]]').extract()
            else:
                description = target_description.xpath('following-sibling::node()[following::h2[1][@id="summary"]]').extract()

        clean_description = ""
        if description:
            for content in description:
                clean_text = re.sub('<[^<]+?>', '', content)
                clean_text = clean_text.replace('\r', '').replace('\n', '')
                clean_description += clean_text

        yield {
            "title": title, 
            "subject": subject,
            "link": response.url,
            "description": clean_description,
            "explanation": clean_explanation, 
        }