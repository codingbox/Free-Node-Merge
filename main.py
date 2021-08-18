import requests
import json
import base64
import re
import time

# 配置
sub_url = [
    "https://raw.fastgit.org/freefq/free/master/v2",
    "https://raw.fastgit.org/v2ray-links/v2ray-free/master/v2ray",
    "https://jiang.netlify.app"
]

# 下载订阅链接将其合并
sub_link = []
for i in range(len(sub_url)):
    url = sub_url[i]
    try:
        rq = requests.get(url)
        if (rq.status_code != 200):
            print("[GET Code {}] Download sub error on link: ".format(rq.status_code) + url)
            continue
        print("Get node link on sub " + url)
        sub_link.append(base64.b64decode(rq.content).decode("utf-8"))
    except:
        print("[Unknown Error] Download sub error on link: " + url)

# 逐条读取链接，并进行测试
country_count = {}
merged_link = []
for i in sub_link:
    for j in i.split():
        try:
            if (j.find("vmess://") == -1):
                print(j)
                continue
            node = json.loads(base64.b64decode(j[8:]).decode("utf-8"))
            rq = requests.get("http://ip-api.com/json/{}?lang=zh-CN".format(node['add']))
            ip_info = json.loads(rq.content)
            if (ip_info['status'] != 'success'):
                continue
            ip_country = ip_info['country']
            if (country_count.__contains__(ip_country)): 
                country_count[ip_country] += 1
            else:
                country_count[ip_country] = 1
            newname = "{} {} {}".format(ip_country, (str)(country_count[ip_country]), re.split(',| ', ip_info['org'])[0])
            print("Rename node {} to {}".format(node['ps'], newname))
            node['ps'] = newname
            merged_link.append(node)
        except:
            print("[Unknown Error]")
    print("Sub Merged successfully\n".format(i))

print(merged_link)

# 合并整理完成的节点
tmp = ""
for i in merged_link:
    bs = "vmess://" + base64.b64encode(json.dumps(i).encode("utf-8")).decode("utf-8")
    tmp = tmp + bs + '\n'
res = base64.b64encode(tmp.encode("utf-8"))
print(res.decode("utf-8"))
_file = open('node.txt', 'w', encoding='utf-8')
_file.write(res.decode("utf-8"))
_file.close()