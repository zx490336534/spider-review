# coding=utf-8
# Auth:zx
# Time:2018/12/2 0002 9:45
import scrapy


class Renrenspider(scrapy.Spider):
    name = "renren2"
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/576586461']
    cookies = {
        'anonymid': 'jp6749qw-ighn5j',
        'depovince': 'GW',
        '_r01_': '1',
        'JSESSIONID': 'abc2VpHTONFGg6oIzFSDw',
        'ick_login': 'dfe2ded8-e8f4-4f34-88bf-57ac97677f6e',
        'first_login_flag': '1',
        'ln_uact': '15168230644',
        'ln_hurl': 'http://hdn.xnimg.cn/photos/hdn321/20131229/1845/h_main_008K_52920001c7f1113e.jpg',
        'ch_id': '10016',
        'wp': '1',
        'wp_fold': '0',
        'jebecookies': '5dfce250-1d58-46af-ba71-6a8f203efbf2|||||',
        '_de': '9D0F4C3FC3E49879570A84C70CA844DE',
        'p': '6785500e0e1d5fa406f0ae744d27c6d01',
        't': 'b38c548637a445992b76ce998a010aa01',
        'societyguester': 'b38c548637a445992b76ce998a010aa01',
        'id': '576586461',
        'xnsid': '936711af',
        'ver': '7.0',
        'loginfrom': 'null'
    }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url=url,cookies=self.cookies,callback=self.parse)

    def parse(self, response):
        print(response.body)
        name = response.xpath('//p[@class="status"]/text()').extract_first()
        friend = response.xpath('//div[@class="userhead"]/span/text()').extract_first()
        print(name)
        print(friend)
