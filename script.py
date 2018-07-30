import json
import pymongo



def response(flow):
    client = pymongo.MongoClient('localhost')
    db = client['jd']
    comments_collection = db['comments']
    url = 'http://.*?/client.action' #匹配规则
    if url in flow.request.url:
        # print('asdfggh' + url)
        text = flow.response.text
        data = json.loads(text)
        comments = data.get('commentInfoList') or []
        for comment in comments:
            if comment.get('commentInfo') and comment.get('commentInfo').get('commentData'):
                print('qwertyu')
                print('qwertyu')
                print('qwertyu')
                info = comment.get('commentInfo')
                nickname = info.get('userNickName')
                content = info.get('commentData')
                pub_date = info.get('commentDate')
                wareAttribute = info.get('wareAttribute')
                buy_date = info.get('orderDate')
                pictures = info.get('pictureInfoList')
                print(nickname, text, pub_date)
                comments_collection.insert({
                    '用户昵称': nickname,
                    '评论内容': content,
                    '评论日期': pub_date,
                    '商品属性': wareAttribute,
                    '购买日期': buy_date,
                    'pictures': pictures
                })
















