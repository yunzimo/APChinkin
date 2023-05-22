"""
cron: 0 8,13,22 * * *
new Env('机场签到')
"""


import json
import requests
import time
import sys
from QLApi import *
import http.cookies
from notify import *



#下面填入机场应用的ID和secret
address = "http://127.0.0.1:5700"
client_id = "9QO7c7RE_wfK"
client_secret = "mPlXkDn1_-FV87BE6HVWPNl0"
ql = QL(address, client_id, client_secret)

def get_cookies():
    envs = ql.getEnvs()
    result = getEnvValueByName(envs,'JC_COOKIE')
    CookieJCs = []
    if result:
        print("已获取并使用Env环境 Cookie")
        if '&' in result:
            CookieJCs = result.split('&')
        elif '\n' in result:
            CookieJCs = result.split('\n')
        else:
            CookieJCs = [result]
    else:
        print("未获取到正确✅格式的机场账号Cookie")
        return

    print(f"====================共{len(CookieJCs)}个机场账号Cookie=========\n")
    print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
    return CookieJCs

def login_in(email,passwd):
    url = 'https://www.cutecloud.net/auth/login'
    payload = {'email': email, 'passwd': passwd}
    response = requests.post(url, data=payload)
    print(response.text)
    cookie = response.headers.get('Set-Cookie')
    print(cookie)
    cookie_dict = http.cookies.SimpleCookie(cookie)
    # 获取cookie所需要的值
    key = cookie_dict['key'].value
    expire_in = cookie_dict['expire_in'].value
    uid = cookie_dict['uid'].value
    email = cookie_dict['email'].value
    print('key:', key)
    print('expire_in:', expire_in)
    str = 'uid='+uid+';'+'email='+email+';'+'key='+key+';'+'expire_in='+expire_in+';'
    return str

    
        
def check_in(cookie):
    content = ''
    print('cookie:'+cookie+'\n')
    try:
        header = {
        'cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 '
                        'Safari/537.36 '
        }
        response = requests.post("https://www.cutecloud.net/user/checkin", headers=header)
        print(response.status_code)
        if response.status_code != 200:
            print('机场签到失败，错误码：'+str(response.status_code))
            send('机场签到','机场签到失败，错误码：'+str(response.status_code))
        else:
            #print(response.text)
            resp_str=response.text
            if resp_str.find('立即注册')!=-1:
                print('cookie重新获取------------------------')
                # 登录
                envs = ql.getEnvs()
                result = getEnvValueByName(envs,'JC_Passwd')
                email = result.split(';')[0].split('=')[1]
                passwd = result.split(';')[1].split('=')[1]
                print(email+'-----------------------'+passwd)
                CookieValue = login_in(email,passwd)
                print(CookieValue)
                envs = {"name":"JC_COOKIE","value":CookieValue,"id":getIdByName(envs,'JC_COOKIE')}
                #更新环境变量
                ql.updateEnv(envs)
                #重新签到
                check_in(CookieValue)
            else:
                result = json.loads(response.text)
                if result['ret']==1:
                    print("result中trafficInfo的类型: {}".format(type(result['trafficInfo'])))
                    trafficInfo = result['trafficInfo']
                    print(trafficInfo['todayUsedTraffic'])
                    content = content + result['msg'] + '\n' +'今日使用：'+ trafficInfo['todayUsedTraffic']+'\n'+'总共使用：'+trafficInfo['lastUsedTraffic']+'\n'+'流量剩余：'+trafficInfo['unUsedTraffic']+'\n'
                    send('机场签到','签到成功' + content)            
                else:
                    content = content + result['msg']
                    print(content)
                    send('机场签到',content)
    except Exception as e:
        print('机场签到失败\n',e)
        
        send('机场签到','机场签到失败')

if __name__ == '__main__':
    try:
        cks = get_cookies()
        if not cks:
            sys.exit()
    except:
        print("未获取到有效COOKIE,退出程序！")
        sys.exit()
    for cookie in cks[:]:
        check_in(cookie)