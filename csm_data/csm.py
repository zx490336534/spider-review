# coding=utf-8
# Auth:zx
# Time:2018/12/2 0002 21:28
import requests
import json
import time
def work():
    url_index = 'http://www.csm-huan.com/index'
    data1 = {
        'query': '{"channel_codes":["antv","5dfcaefe6e7203df9fbe61ffd64ed1c4","bingtuanweishi","fjtv","5ace8ddc54a4151bbcf76e56c8aa582a","c8bf387b1824053bdb0423ef806a2227","5cbb108dbf59f2ae1849ec8d1126d1a5","5a7d01661b5d9c64293860531374312b","ef1fce69a9e1b3a587ca734302400107","1ce026a774dba0d13dc0cef453248fb7","2c854868563485135dd486801057dd6e","55fc65ef82e92d0e1ccb2b3f200a7529","c39a7a374d888bce3912df71bcb0d580","322fa7b66243b8d0edef9d761a42f263","535765a19ab55a12bbf64a1e98ae97dd","45392a8be644f5b8903838436870c75d","9291c40ec1cec1281638720c74c7245f","0d7b5dfe999fc5fd0140863f6e8910a5","03295de404257fa9653b89bf2d0e47ac","a09ab19928a6b2bd616f7e2eba1056ee","4ec095f1d2564f82341275fff64edb5a","28502a1b6bf5fbe7c6da9241db596237","dragontv","eb7330e363ceec8c6895eacc44a1a804","2aeb585ccaca9fa893b0bdfdbc098c7f","20831bb807a45638cfaf81df1122024d","b82fa4086c9a2c9442279efbb80cce31","5927c7a6dd31f38686fafa073e2e13bc","ad291a233f1fd3f24332e41461798a25","feccf21eb7e50753355efdab2d54d9e8","c786da29f0f5cc5973444e3ad49413a6","590e187a8799b1890175d25ec85ea352","5731a167d79c432575056c4963dc8049","cctv_kids","cctv_news","cctv_music","cctv1","cctv8","cctv2","cctv9","cctv6","cctv7","cctv3","cctv12","cctv10","cctv11","cctv4_asia","cctv5"],"begin_time":"2018-12-02 20:28:00","end_time":"2018-12-02 21:28:00"}',
        'queryType': 'all'}
    url_history = 'http://www.csm-huan.com/history_compare'
    response_index = requests.post(url_index, data=data1)
    channel_dict = {}
    index_info = json.loads(response_index.text)
    for i in index_info['data']['rows_sort_by_program']:
        print(i)
        channel_dict[i.get('channelName')] = []
        channel_dict[i.get('channelName')].append(i.get('channelCode'))
        channel_dict[i.get('channelName')].append(i.get('timePoint').get('programName'))
        channel_dict[i.get('channelName')].append(i.get('timePoint').get('audienceRating'))
    for key,value in channel_dict.items():
        history_data = {}
        history_data['channel_codes']= channel_dict[key][0]
        history_data['flag']= 'hour'
        history_data['queryType']= 'all'
        history_json = requests.post(url_history, data=history_data).json()
        time_xAxis = history_json.get('option').get('xAxis')[0].get('data')
        series = history_json.get('option').get('series')[0].get('data')
        channel_dict[key].append(time_xAxis)
        channel_dict[key].append(series)

    with open(str(int(time.time()*1000))+'csm.json', 'w') as f:
        content = json.dumps(channel_dict, ensure_ascii=False)
        f.write(content)

if __name__ == '__main__':
    while True:
        work()
        time.sleep(3600)
