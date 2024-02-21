import scrapy
import re
from scrapy.http import Response

# scrapy crawl experiment_archive -o experiment_archive.json

class experimentArchiveSpider(scrapy.Spider):
    name = "experiment_archive"

    start_urls = ["https://www.experimentarchive.com/"]

    def parse(self, response: Response):

        base_url = "https://www.experimentarchive.com"

        for experiment in response.xpath("//div[@class='polaroidcontainer']"):
            title = experiment.xpath(".//h2[@class='polaroidrubrik']/text()").get()
            subject = experiment.xpath(".//div[@class='polaroidkategori']/text()").get()
            description = experiment.xpath(".//div[@class='polaroidingress']/text()").get()
            link = experiment.xpath(".//div[@class='polaroidcontainer_inre']/a/@href").get()

            if link:
                yield scrapy.Request(url=base_url + link, callback=self.parse_explanation, cb_kwargs=dict(title=title, subject=subject, description=description))

    def parse_explanation(self, response: Response, title, subject, description):

        explanation = None

        class_names = ['lang_forklaring', 'forklaring', 'kort_forklaring']

        for class_name in class_names:
            target_h2 = response.xpath(f"//h2[@class='{class_name}']")
            if target_h2:
                explanation = target_h2.xpath("following-sibling::node()[following-sibling::h2]").extract()
                break

        clean_explanation = ""
        if explanation:
            for content in explanation:
                clean_text = re.sub('<[^<]+?>', '', content)
                clean_text = clean_text.replace('\r', ' ').replace('\n', ' ')
                clean_explanation += clean_text


        yield {
            "title": title,
            "subject": subject,
            "description": description,
            "link": response.url,
            "explanation": clean_explanation,
        }