import json
import requests
import datetime
import random


class Huge(object):
    def __init__(self):
        #self.QmsgKey = '',
        # 抓包获取
        self.appid = '',
        self.apsid = '',
        self.couseid = '',
        self.session = requests.session()
        self.headers = {
            'Host': 'apiopen.jingdaka.com',
            'Connection': 'keep-alive',
            'filter': 'test1',
            'charset': 'utf-8',
            "appid": "%s" % self.appid,
            "apsid": "%s" % self.apsid,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Mi 10 Pro Build/SKQ1.220119.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3185 MMWEBSDK/20210902 Mobile Safari/537.36 MMWEBID/4024 MicroMessenger/8.0.15.2001(0x28000F41) Process/appbrand0 WeChat/arm64 Weixin GPVersion/1 NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'version': '8.5.14',
            'Referer': 'https://servicewechat.com/%s/36/page-frame.html' % self.appid,
        }

    def getTimes():
        return str(datetime.date.today())

    def getCalendarId(self):
        url = 'https://apiopen.jingdaka.com/user/get_theme'
        params = (
            ('course_id', self.couseid),
            ('record_at', Huge.getTimes()),
        )

        request = self.session.get(url, headers=self.headers, params=params)
        data = json.loads(request.content.decode('utf8'))
        return data['data']['calendar_id']

    def isCheckin(self):
        url = 'https://apiopen.jingdaka.com/user/get_theme'
        params = (
            ('calendar_id', Huge.getCalendarId(self)),
        )

        request = self.session.get(url, headers=self.headers, params=params)
        data = json.loads(request.content.decode('utf8'))
        return data['data']['is_submited'],data['data']['pc_content']

    def getPic(self):
        url = 'https://apiopen.jingdaka.com/user/submitlist'
        params = (
            ('order_type', '3'),
            ('limit', '100'),
            ('offset', '0'),
            ('search_user_name', '电信'),
            ('course_id', self.couseid),
            ('record_at', Huge.getTimes()),
        )

        request = self.session.get(url, headers=self.headers, params=params)
        data = json.loads(request.content.decode('utf8'))
        rand = random.randint(0,99)
        pic = data['data']['submit_list'][rand]['picture_list'][0]
        voc = data['data']['submit_list'][rand]['voice_list'][0]
        return pic, voc

    def checkin(self):
        flag = Huge.isCheckin(self)
        if flag[0] == 1:
            print('已经打卡了')
            return
        elif flag[1] == '':
            print('没有打卡内容')
            return
        else:
            url = 'https://apiopen.jingdaka.com/user/submit'
            data = {
                "content": "", "word_count": 0, "form_id": "", "document_list": [],
                "picture_list": [Huge.getPic(self)[0]],
                "voice_list": [{
                    "voice": Huge.getPic(self)[1]['voice_url'],
                    "voice_duration": Huge.getPic(self)[1]['voice_duration']
                }],
                "video_list": [],
                "web_title": "",
                "website": "",
                "show_range": 0,
                "course_calendar_id": Huge.getCalendarId(self),
                "course_id": self.couseid,
                "record_at": "%sT00:00:00+08:00" % Huge.getTimes()
            }
            request = self.session.post(url, headers=self.headers, data=json.dumps(data))
            d = json.loads(request.content.decode('utf8'))
            sub = d['err_msg']
            if sub == 'SUCCESS':
                print('今日英语虎哥未打卡,已为您自动打卡')
            else:
                print('今日英语虎哥未打卡,请尽快打卡')


if __name__ == '__main__':
    run = Huge()
    run.checkin()
