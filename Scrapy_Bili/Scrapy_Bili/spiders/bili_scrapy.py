# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
import json, re, datetime
from Scrapy_Bili.Scrapy_Bili.items import ScrapybiliItem



class ScrapybiliSpider(scrapy.Spider):
    name = 'scrapy_bili'
    allowed_domains = ['space.bilibili.com', 'api.bilibili.com']

    headers = {
        'Accept':'application/json, text/plain, */*',
        'Content-Type':'application/x-www-form-urlencoded',
        'Referer':'https://space.bilibili.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

#一定需要在headers中传入上述信息，不能只传入user-agent.否则会报400错误。

    def start_requests(self):
        post_url = 'https://space.bilibili.com/ajax/member/GetInfo'
        for i in range(0, 326480090):
            form_data = {
                'mid': str(i),
                'csrf': 'c4a9f764ab52dd8eacc20b6947c58f35'
            }
            yield FormRequest(url=post_url, method='POST', headers=self.headers, formdata=form_data, callback=self.parse, meta={'i':i})

    def parse(self, response):
        result = json.loads(response.text, encoding='utf-8')
        data = result['data']
        i = response.meta['i']
        follow_url = 'https://api.bilibili.com/x/relation/stat?vmid={0}&jsonp=jsonp&callback=__jp4'.format(i)
        yield Request(url=follow_url, callback=self.parse_detail, meta={'data':data})

    def parse_detail(self, response):
        item = ScrapybiliItem()

        data = response.meta['data']
        item['face_img'] = data['face']
        item['name'] = data['name']
        item['curr_level'] = int(data['level_info']['current_level']) if data['level_info']['current_level'] else 0
        item['regtime'] = datetime.datetime.fromtimestamp(int(data['regtime'])) if data.get('regtime', '') else None
        item['sex'] = data['sex']
        item['mid'] = int(data['mid'])
        item['home_url'] = 'https://space.bilibili.com/{0}/#/'.format(data['mid'])

        text = response.text
        match = re.match(r'.*"following":(\d+).*"follower":(\d+).*', text)
        # 粉丝数
        item['follower'] = int(match.group(1))
        # 关注数
        item['following'] = int(match.group(2))

        yield item
