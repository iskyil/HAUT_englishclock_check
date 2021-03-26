import requests
import json
import re

# 读取csv中id的值
f = open('id.csv')
data = f.readline()
# print(data)
# 我们仅仅需要数字，用正则取出数字id
id = re.sub("\D", "", data)
print(id)
base_url = 'https://apiopen.jingdaka.com/user/get_theme?calendar_id=%s'%(id)
headers = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 11; Mi 10 Pro Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2767 MMWEBSDK/201201 Mobile Safari/537.36 MMWEBID/4024 MicroMessenger/8.0.1.1841(0x28000151) Process/appbrand0 WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android",
    "content-type": "application/json",
    "Accept-Encoding": "gzip,compress,br,deflate",
    "version": "7.3.16",
    "appid": "                           ",
    "apsid": "                           ",
    "charset": "utf-8",
    "filter": "test1",
    "Connection": "keep-alive",
    "Host": "apiopen.jingdaka.com",
    "Referer": "https://servicewechat.com/wx5a6e75651505714e/29/page-frame.html"
}
# 仅appid、apsid与User-Agent必需

if __name__ == '__main__':
    request = requests.get(base_url, headers=headers)
    d = json.loads(request.content.decode('utf8'))
    # print(d)
    # print(d['data']['is_submited'])
    sub = d['data']['is_submited']
    # print(sub)
    if sub == 1:
        test = 'yes'
        print(test)
        # 必须将id强制转换成整数类型，才能进行递增操作
        id = int(id)
        id += 1
        # 最后，将递增后的id写入csv文件，供下次使用
        with open('id.csv', 'w') as idFile:
            idFile.write('%d' % id)
        print(id)
    else:
        test = '今日英语虎哥未打卡，尽快打卡'
        print(test)
        id = int(id)
        id += 1
        with open('id.csv', 'w') as idFile:
            idFile.write('%d' % id)
        QmsgKey = "                         "
        content = f"""{test}"""
        data = {
            "msg": content
        }
        url_send = "https://qmsg.zendee.cn/send/%s" % (QmsgKey)
        try:
            res = requests.post(url_send, data=data)
            sucmsg = res.json()['success']
            if sucmsg == True:
                print("qq推送服务成功")
            else:
                print("qq推送服务失败")
        except:
            print("qq推送参数错误")