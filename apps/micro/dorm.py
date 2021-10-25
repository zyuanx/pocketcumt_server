import requests


class Dorm:
    def __init__(self):
        self.session = requests.Session()
        self.url = {
            'urlTry': 'https://xxxxx/',
            'urlQuery': 'https://xxxxx/'
        }

    def get_ele(self, params):
        dormid = [
            ['13579_173_288_948', '13579_173_288_949', '13579_173_288_950'],
            ['13579_173_289_951', '13579_173_289_952',
             '13579_173_289_953', '13579_173_289_954'],
            ['13579_173_290_955', '13579_173_290_956',
             '13579_173_290_957', '13579_173_290_958'],
            ['13579_173_291_959', '13579_173_291_960', '13579_173_291_961',
             '13579_173_291_962', '13579_173_291_963'],
            ['13579_173_292_964', '13579_173_292_965', '13579_173_292_966'],
            ['13579_173_293_967', '13579_173_293_968', '13579_173_293_969']
        ]
        dormname = [
            ['杏1楼', '杏2楼', '杏3楼'],
            ['竹1楼', '竹2楼', '竹3楼', '竹4楼'],
            ['松1楼', '松2楼', '松3楼', '松4楼'],
            ['桃1楼', '桃2楼', '桃3楼', '桃4楼', '桃5楼'],
            ['梅1楼', '梅2楼', '梅3楼'],
            ['研1', '研2', '研3']
        ]
        res1 = self.session.post(self.url['urlTry'], data={
            'openid': 'oUiRowQuQrWYQISmJBkJ7FMHzDuc',
            'flatid': dormid[int(params.get('row'))][int(params.get('column'))],
            'roomname': params.get('dorm')
        }, timeout=3).json()
        if res1['code'] == 400003:
            raise Exception("宿舍不存在")
        else:
            try:
                res2 = self.session.post(self.url['urlQuery'], data={
                    'flatname': dormname[int(params.get('row'))][int(params.get('column'))],
                    'roomname': params.get('dorm')
                }, headers={
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'www.houqinbao.com',
                    'Origin': 'http://www.houqinbao.com',
                    'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.3578.98 Safari / 537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }, timeout=3).json()
                return {'dushu': res2['data']['dushu']}
            except TimeoutError as e:
                raise Exception("暂不可用")
