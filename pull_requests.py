# -*- coding: utf-8 -*-

import requests
from pprint import pprint
import slackweb
from pytz import timezone
from dateutil import parser

def create_label_list(labels):
    label_list = []
    for lab in labels:
        label_list.append(lab['name'])
    return ','.join(label_list)

url = '' # issueを取得
headers = {"content-type": "application/json"}
issue_data = requests.get(url, headers=headers).json() # 型をlistで取得

pull_request_count = 0
attachments = []

for data in issue_data:
    for label in data['labels']:
        pull_request_count += 1 # プルリク総件数

        # プルリクに紐付いているラベルを全て取得する
        footer_label = create_label_list(data['labels'])

        # 文字列UTCからJSTのdatetime型へ
        jst_time = parser.parse(data['created_at']).astimezone(timezone('Asia/Tokyo'))

        attachment = {
            'title': data['title'],
            'title_link': data['html_url'],
            'color': 'good',
            'author_icon': data['user']['avatar_url'],
            'author_name': data['user']['login'],
            'footer': footer_label,
            'ts': jst_time.timestamp(), # UNIX_TIMEを送る
        }
        attachments.append(attachment) # リストを入れてく

bot_title = {
    'pretext': 'プルリク総件数は{0}件です'.format(pull_request_count)
}
attachments.insert(0, bot_title) # リストの頭に入れる

pprint(attachments)

# slack設定
webhook_url = '' # 送信先のチャンネルのURLをここに書く
slack = slackweb.Slack(url=webhook_url)

# slackに投げる
slack.notify(attachments=attachments)
