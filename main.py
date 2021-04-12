# 服务器版本
import json
import re
import requests
import time

class Huge(object):
    def __init__(self):
        self.QmsgKey = '                            ',
        self.appid = '                              ',
        self.apsid = '                              ',
        # 自动打卡开关，1表示开
        self.auto = 1,

    def checkin(self):
        auto = self.auto[0]
        # 提取id
        f = open('id.csv', encoding='utf-8')
        data = f.readline()
        id = re.sub("\D", "", data)
        base_url = 'https://apiopen.jingdaka.com/user/get_theme?calendar_id=%s' % (id)
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Linux; Android 11; Mi 10 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2767 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/4024 MicroMessenger/8.0.1.1841(0x28000151) Process/appbrand0 WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
            "content-type": "application/json",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "version": "7.3.16",
            "appid": "%s" % self.appid,
            "apsid": "%s" % self.apsid,
            "charset": "utf-8",
            "filter": "test1",
            "Connection": "keep-alive",
            "Host": "apiopen.jingdaka.com",
            "Referer": "https://servicewechat.com/wx5a6e75651505714e/29/page-frame.html"
        }
        session = requests.session()
        request = session.get(base_url, headers=headers)
        d = json.loads(request.content.decode('utf8'))
        sub = d['data']['is_submited']
        # 正则匹配时间
        time = d['data']['record_at']
        real_time = re.match(r'\w{4}-(\w{2}-\w{2})', time)
        times = real_time.group(1)
        if sub == 1:
            text = '今日虎哥打卡任务已完成'
            print(text)
        else:
            if d['data']['pc_content'] == '':
                text = '今日没有任务'
                print(text)
            else:
                text = '今日英语虎哥未打卡'
                print(text)
                if auto == 1:
                    print(id)
                    url = 'https://apiopen.jingdaka.com/user/submit'
                    id = int(id)
                    data2 = {
                        "content": "", "word_count": 0, "form_id": "", "document_list": [],
                        "picture_list": ["                                             "],
                        "voice_list": [
                            {"voice": "                                          ", "voice_duration": 33}],
                        "video_list": [], "web_title": "", "website": "", "show_range": 0,
                        "course_calendar_id": id,
                        "course_id": 972440, "record_at": "2021-%sT00:00:00+08:00" % (times)
                    }
                    session = requests.session()
                    request = session.get(url, headers=headers,data=json.dumps(data2))
                    d = json.loads(request.content.decode('utf8'))
                    sub = d['err_msg']
                    if sub == 'SUCCESS':
                        text = '今日英语虎哥未打卡,已为您自动打卡'
                    else:
                        text = '今日英语虎哥未打卡,请尽快打卡'
                QmsgKey = "%s" % self.QmsgKey
#                 print(QmsgKey)
#                 print(times)
#                 print(text)
                content = f"""{times}{text}"""
                data = {
                    "msg": content
                }
                url_send = "https://qmsg.zendee.cn/send/%s" % (QmsgKey)
                print(url_send)
                try:
                    res = requests.post(url_send, data=data)
                    sucmsg = res.json()['success']
                    if sucmsg == True:
                        print("qq推送服务成功")
                    else:
                        print("qq推送服务失败")
                except:
                    print("qq推送参数错误")
        # 存入id
        ids = int(id)
        ids += 1
        with open('id.csv', 'w', encoding='utf-8') as idFile:
            idFile.write('%d' % ids)
        # 日志记录
        with open('日志.txt', 'a', encoding='utf-8') as idFile:
            idFile.write('%s,' % times)
            idFile.write('今日的任务id为%s，' % id)
            idFile.write('%s\n' % text)
    
if __name__ == '__main__':
    run = Huge()
    run.checkin()
