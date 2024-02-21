import scrapy
import re
from scrapy.http import Response

# scrapy crawl steve_spangler -o steve_spangler.json

class steveSpanglerSpider(scrapy.Spider):
    name = "steve_spangler"

    start_urls = ["https://stevespangler.com/experiments/"]

    def parse(self, response: Response):

        base_url = "https://stevespangler.com"

        for experiment in response.xpath("//article[@class='post']"):

            title = experiment.xpath(".//div[@class='text']/h3/text()").get()
            description = experiment.xpath(".//div[@class='text']/p/text()").get()
            link = experiment.xpath(".//div[@class='text']/div/a[@class='wp-block-button__link']/@href").get()

            if link:
                yield scrapy.Request(url=base_url + link, callback=self.parse_explanation, cb_kwargs=dict(title=title, description=description))

            next_page = response.xpath("//a[@class='nextpostslink']/@href").get()

            if next_page:
                yield response.follow(url=next_page, callback=self.parse)

    def parse_explanation(self, response: Response, title, description):

        explanation = None

        target_strong = response.xpath('//strong[contains(text(), "How Does It Work")]')
        p_tags = response.xpath('//p[@class="p1"]//text()').extract()
        h1_tag = response.xpath('//h1[contains(text(), "How Does It Work?")]')

        if target_strong:
            closest_div = target_strong.xpath("ancestor::div[@class='text']")
            if closest_div:
                extracted_content = closest_div.xpath('.//text()').extract()
                explanation = ''.join(extracted_content)
        
        elif p_tags:
            # If <strong> is not present, extract text from <p> tags with class "p1"
            p_tags = response.xpath('//p[@class="p1"]//text()').extract()
            
            if p_tags:
                explanation = ''.join(p_tags)

        elif h1_tag:
            following_p = h1_tag.xpath('following-sibling::p[1]//text()').extract()
                
            if following_p:
                # Join the extracted content to form a string
                explanation = ''.join(following_p)

        clean_explanation = ""
        if explanation:
        # Clean the extracted content
            clean_explanation = re.sub(r'<.*?>', '', explanation)  # Remove HTML tags
            clean_explanation = clean_explanation.replace('\r', ' ').replace('\n', ' ')  # Remove \r and \n

        yield {
            "title": title,
            "description": description,
            "link": response.url,
            "explanation": explanation,
        }