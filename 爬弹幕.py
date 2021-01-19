from bs4 import BeautifulSoup
import requests
import os
import json
import pandas as pd
# from wordcloud import WordCloud, ImageColorGenerator
import imageio
import seaborn as sns
import matplotlib.pyplot as plt
import jieba
import collections # 词频统计库

#提取某一期的弹幕
def get_danmu(num1,num2,page):
    url='https://bullet-ws.hitv.com/bullet/2021/01/17/{}/{}/{}.json'
    # url='https://bullet-ali.hitv.com/bullet/2021/01/3/010001/4692790/0.json'
    danmuurl = url.format(num1,num2,page)
    res=requests.get(danmuurl)
    res.encoding = 'utf-8'
    jd=json.loads(res.text)
    details=[]
    for i in range(len(jd['data']['items'])):
        result={}
        # result['stype']=num2
        # 0 分钟：0-1 分钟
        result['time(分钟)']=page
        result['time(秒)']=int(jd['data']['items'][i]['time'])%60000/1000//60
        result['time(精确秒)']=int(jd['data']['items'][i]['time'])%60000/1000
        # result['id']=jd['data']['items'][i]['id']
        # try:
        #     result['uname']=jd['data']['items'][i]['uname']
        # except:
        #     result['uname']=''
        result['content']=jd['data']['items'][i]['content']
        # 弹幕点赞数
        # try:
        #     result['v2_up_count']=jd['data']['items'][i]['v2_up_count']
        # except:
        #     result['v2_up_count']=''
        details.append(result) 
    return details

def count_danmu(num1,num2,page):
    danmu_total=[]
    for i in range(page):
        danmu_total.extend(get_danmu(num1,num2,i))
    return danmu_total

def main():
    # 第一季
    # all_12 = [[153606,4689939,84,'第一期'],[182843,4712794,91,'第二期'],['000000',4736228,83,'第三期'],\
    #             ['003934',4757455,84,'第四期'],['003733',4777585,88,'第五期'],[110832,4797719,98,'第六期'],\
    #             [181918,4819935,94,'第七期'],['010000',4844469,102,'第八期'],['011809',4892601,94,'第九期'],\
    #             ['003733',4930225,95,'第十期'],[175543,4976693,94,'第十一期'],['013700',5014495,92,'第十二期']]
    # 第二季
    all_12 = [['012720',6003037,7,'先导片'],['014936',6048031,100,'第一期'],['010503',6086355,96,'第二期'],['004307',6127793,96,'第三期'],\
                ['012916',6168251,89,'第四期'],['010534',6209042,89,'第五期'],['012729',6256538,88,'第六期'],\
                ['132233',6295564,89,'第七期'],['010503',6335411,94,'第八期'],['010930',6380854,91,'第九期'],\
                ['010528',6424343,96,'第十期'],['004427',6484461,92,'第十一期'],['050119',6562903,107,'第十二期']]
    writer = pd.ExcelWriter('/Users/krystalgong/Desktop/声入人心/声入人心第二季弹幕.xlsx')
    for n in all_12:
        danmu_end=[]
        num1=str(n[0])
        num2=str(n[1])
        page=n[2]
        danmu_end.extend(count_danmu(num1,num2,page))
        df=pd.DataFrame(danmu_end)
        df.to_excel(writer,n[3])
    writer.save()

if __name__ == '__main__':
    main()