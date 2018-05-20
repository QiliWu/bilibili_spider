from ScrapyRedisBili.scrapy_redis.spiders import RedisSpider
from scrapy import Request, FormRequest
import json, re
import datetime
from ScrapyRedisBili.ScrapyRedisBili.items import ScrapyredisbiliItem


class ScrapyredisbiliSpider(RedisSpider):
    name = 'scrapyredis_bili'
    redis_key = 'biliuser:start_urls'
    allowed_domains = ['space.bilibili.com', 'api.bilibili.com']
    post_url = 'https://space.bilibili.com/ajax/member/GetInfo'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://space.bilibili.com'}

    def start_requests(self):
        for i in range(0, 326480090):
            form_data = {
                'mid': str(i),
                'csrf': ''
            }
            yield FormRequest(url=self.post_url,
                              method='POST',
                              headers=self.headers,
                              formdata=form_data,
                              callback=self.parse,
                              meta={'i':i})

    def parse(self, response):
        result = json.loads(response.text, encoding='utf-8')
        data = result['data']
        i = response.meta['i']
        follow_url = 'https://api.bilibili.com/x/relation/stat?vmid={0}&jsonp=jsonp&callback=__jp4'.format(i)
        yield Request(url=follow_url, callback=self.parse_detail, meta={'data':data})

    def parse_detail(self, response):
        item = ScrapyredisbiliItem()
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

