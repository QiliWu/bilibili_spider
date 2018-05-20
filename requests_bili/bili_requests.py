import requests
import datetime
import json
import re
from urllib.parse import urlencode

#使用fake_useragent包随机生成useragent
from fake_useragent import UserAgent
ua = UserAgent()

#获取代理ip的接口
from get_ip import GetIP
getip = GetIP()

#创建一个Insertitem对象实例，来向数据库中插入数据
from requests_bili.mysql_table import Insertitem, Users
insertitem = Insertitem()

#通过post请求post_url, 获取包含用户注册信息的json数据
post_url = 'https://space.bilibili.com/ajax/member/GetInfo'
for i in range(0, 326480090):
    form_data = {
        'mid':str(i),
        'csrf':'c4a9f764ab52dd8eacc20b6947c58f35'
    }
    headers = {
        'Accept':'application/json, text/plain, */*',
        'Content-Type':'application/x-www-form-urlencoded',
        'Referer':'https://space.bilibili.com',
        'User-Agent': ua['random']
    }
    #从数据库中提取有效的代理ip
    proxy_dict, proxy= getip.get_random_valid_ip()
    try:
        response = requests.post(url=post_url, headers=headers, proxies=proxy_dict, data=urlencode(form_data), timeout=10)
        result = json.loads(response.text, encoding='utf-8')
        data = result['data']
        home_url = 'https://space.bilibili.com/{0}/#/'.format(i)
        face_img = data['face']
        name = data['name']
        curr_level = int(data['level_info']['current_level']) if data['level_info']['current_level'] else 0
        regtime = datetime.datetime.fromtimestamp(int(data['regtime'])) if data.get('regtime', '') else None
        sex = data['sex']
        mid = i

        #获取关注数和粉丝数
        follow_url = 'https://api.bilibili.com/x/relation/stat?vmid={0}&jsonp=jsonp&callback=__jp4'.format(i)
        follow_r = requests.get(url=follow_url, headers=headers, proxies=proxy_dict)
        text = follow_r.text
        match = re.match(r'.*"following":(\d+).*"follower":(\d+).*', text)
        #粉丝数
        follower = int(match.group(1))
        #关注数
        following = int(match.group(2))

        new_item = Users(home_url=home_url,
                         face_img=face_img,
                         name=name,
                         curr_level=curr_level,
                         regtime=regtime,
                         sex=sex,
                         mid=mid,
                         follower=follower,
                         following=following)
        insertitem.add_item(new_item)
        print('成功插入第 {0} 条用户信息'.format(i))

    except Exception as e:
        print(e)

#在所有数据插入完成后，调用getip.close_conn方法关闭数据数据库连接
#如果在中途关闭了conn, 则会报错：_mysql_exceptions.InterfaceError: (0, '')
getip.close_conn()

print('finished')









