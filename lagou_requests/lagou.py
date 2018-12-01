# coding=utf-8
# Auth:zx
# Time:2018/12/1 0001 19:45
import requests


class LagouSpider(object):
    def __init__(self):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '43',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=ABAAABAAAFCAAEG9304352BED7368D2569B54649176FFC7; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543664790; _ga=GA1.2.1745748303.1543664791; _gat=1; user_trace_token=20181201194630-be8f3c26-f55e-11e8-8869-525400f775ce; LGSID=20181201194630-be8f3dd1-f55e-11e8-8869-525400f775ce; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DAXim_5bnpwAzTOHZyBDQD_fxpFjqpIyP4IjYd7BAb17%26ck%3D3669.2.113.183.153.168.142.129%26shh%3Dwww.baidu.com%26wd%3D%26eqid%3Dcdc9c79600044814000000065c027491; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20181201194630-be8f409b-f55e-11e8-8869-525400f775ce; _gid=GA1.2.793890544.1543664791; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=index_search; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543664795; LGRID=20181201194634-c101868f-f55e-11e8-8ca7-5254005c3644; SEARCH_ID=8fe186bd16d0405086ba515bbc78fc49',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.offset = 1
        self.data = {'first': 'true',
                     'pn': str(self.offset),
                     'kd': 'python爬虫'}

    def start_requests(self):
        response = requests.post(url=self.url, headers=self.headers, data=self.data)
        html = response.content.decode()
        print(html)
        self.offset += 1
        self.start_requests()
        if self.offset == 30:
            return


if __name__ == '__main__':
    spider = LagouSpider()
    spider.start_requests()
