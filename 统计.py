import pandas as pd
import numpy as np
import codecs
import jieba
import jieba.posseg as pseg
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
# from scipy.misc import imread
import matplotlib.pyplot as plt
import collections
from bs4 import BeautifulSoup
import requests
import os
import json
# import imageio
# import seaborn as sns

def jieba_frequency(txt):
    # 自定义词汇+停用词 e.g. 合并 金色+男高音=金色男高音，合并过后词性变为x
    jieba.load_userdict('combined_words.txt')
    stopwords = [line.strip() for line in open("stopword.txt").readlines()]
    # 词汇切割
    cixing = pseg.lcut(txt)
    # 精确模式
    count  = jieba.lcut(txt)
    # 搜索引擎模式：
    # count = jieba.cut_for_search(txt)

    word_count = {}
    word_flag = {}
    all=[]
    word_count_cixing = pd.DataFrame(columns=["word","count","flag"])

    # 词性统计
    for w in cixing:
        word_flag[w.word] = w.flag
    # 词频统计
    for word in count:
        if word not in stopwords:
        # 不统计字数为一的词
            if len(word) == 1:
                continue
            else:
                word_count[word] = word_count.get(word, 0) + 1
    items = list(word_count.items())
    # 按词频排序
    items.sort(key=lambda x: x[1], reverse=True)
    # 查询词频字典里关键字的词性
    for i in range(len(items)):
        word=[]
        word.append(items[i][0])
        word.append(items[i][1])
        # 若词频字典里，该关键字有分辨出词性，则记录，否则为空
        if items[i][0] in word_flag.keys():
            word.append(word_flag[items[i][0]])
        else:
            word.append("")
        # 通过词性筛选关键词
        if word[2] in ['m','c','d','f']:
            pass
        all.append(word)
    word = []
    count = []
    flag = []
    new_txt = ''
    for res in all:
        new_txt += res[0] + ','
        word.append(res[0])
        count.append(res[1])
        flag.append(res[2])
    word_count_cixing['word'] = word
    word_count_cixing['count'] = count
    word_count_cixing['flag'] = flag
    return word_count_cixing, new_txt, word_count

def img_grearte(txt,word_count,people):
    path = people+'.jpg'
    mask = np.array(Image.open('wordcloud.jpeg'))
    word=WordCloud(background_color="white",
                    width=800,
                    height=800,
                    scale=32, # 图片清晰度？还没试过
                    font_path='/Library/Fonts/Arial Unicode.ttf',
                    mask=mask
                    ).generate(txt)
    word.generate_from_frequencies(word_count)
    word.to_file(path)
    # plt.imshow(word)    #使用plt库显示图片
    # plt.axis("off")
    # plt.show()

def main():
    writer = pd.ExcelWriter('/Users/krystalgong/Desktop/声入人心/声入人心第一季多人词频4.xlsx')
    sheet_names = ['第一期','第二期','第三期','第四期','第五期','第六期',\
                    '第七期','第八期','第九期','第十期','第十一期','第十二期']
    keywords = [['阿云嘎','嘎子|嘎子哥|阿云嘎|双云|嘎嘎|云次方|老云家'],['简弘亦','简弘亦|简老师'],\
        ['陆宇鹏','陆宇鹏|鹏鹏'],['王晰','王晰|晰哥|深呼吸|深呼晰'],['仝卓','仝卓|人工卓']]
    # keywords = [['蔡程昱','蔡程昱|蔡蔡|菜菜|嫡长子'],['郑云龙','大龙|郑云龙|双云']]
    for keyword in keywords:
        people = keyword[0]
        criteria = keyword[1]
        txt = ''
        for name in sheet_names:
            sheet = pd.read_excel('/Users/krystalgong/Desktop/声入人心/声入人心第一季弹幕.xlsx',sheet_name = name)
            sheet['content'] = sheet['content'].apply(str)
            text = sheet.loc[sheet['content'].str.contains(criteria)]
            for i in text['content']:
                txt+=i
        word_count_cixing, new_txt, word_count = jieba_frequency(txt)
        # generate Word Cloud!!!
        img_grearte(new_txt,word_count,people)
        word_count_cixing.to_excel(writer,people)
        print(people+' finished!')
    writer.save()

if __name__ == '__main__':
    main()