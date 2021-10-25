import requests
import json


class Collection:
    def __init__(self):
        self.session = requests.Session()

    def search_book(self, params):
        url = 'https://xxxxx/'
        post_data = {
            "searchFieldContent": params.get('book_title'),
            "searchField": "keyWord",
            "sortClause": "asc",
            "page": params.get('page'),
            "rows": 10
        }
        try:
            res = self.session.post(url=url, data=json.dumps(post_data)).text
        except TimeoutError as e:
            raise Exception('服务响应超时')
        data = json.loads(res)['data']
        book_list = []
        for item in data['searchResult']:
            book_list.append({
                'book_recordId': item['recordId'],
                'book_title': item['title'],
                'book_author': item['author'],
                'book_publisher': item['publisher'],
                'book_isbn': item['isbn'],
                'book_personalAuthor': item['personalAuthor'],
                'book_onShelfCountI': item['onShelfCountI']
            })
        return {'count': (data['numFound'] + 9) // 10,
                'results': book_list,
                'page': int(params.get('page')), }

    def book_detail(self, params):
        url = 'https://xxxxx/'
        post_data = {
            "page": 1,
            "rows": 20,
            "recordId": params.get('book_id'),
            "isUnify": 'true'
        }
        try:
            response = self.session.post(url, data=json.dumps(post_data)).json()['data']['list']
        except TimeoutError as e:
            raise Exception('服务响应超时')
        detail_list = []
        for item in response:
            detail_list.append({
                'callNo': item['callNo'],
                'locationName': item['locationName'],
                'processType': item['processType'],
            })
        return {
            'results': detail_list,
        }
