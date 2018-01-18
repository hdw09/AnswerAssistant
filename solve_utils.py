#!/usr/bin/python
# -*- coding: utf-8 -*-
import webbrowser
import requests

#直接用浏览器打开问题
def open_wabpage(question):
    webbrowser.open('https://baidu.com/s?wd=' + question)

#根据问题搜索结果计算每个选项出现的次数
def words_count(question,answers):
    print "搜索问题得到的答案中各个选项匹配的次数:"
    try:
        req = requests.get(url='http://www.baidu.com/s', params={'wd': question})
        body = req.text
        counts = []
        for answer in answers:
            if len(answer) == 0:
                answer = "OCR can not read"
            num = body.count(answer)
            par = {'answer':answer, 'num':num}
            counts.append(par)
            print answer + " ---> " + str(num)
        return counts;
    except:
        print "search_count error"
        return counts;

#计算问题＋每个选项搜索的结果数
def search_count(question,answers):
    print "问题和答案一起搜各个选择得到的结果："
    counts = []
    for answer in answers:
        if len(answer) == 0:
            answer = "OCR can not read"
        try:
            req = requests.get(url='http://www.baidu.com/s', params={'wd': question +"%20"+answer.encode('utf-8')})
            body = req.text
            start = body.find(u'百度为您找到相关结果约') + 11
            body = body[start:]
            end = body.find(u"个")
            num = body[:end]
            num = num.replace(',', '')
            par = {'answer':answer, 'num':num}
    
            counts.append(par)
            print answer + " ---> " + str(num)
        except:
            print "search_count error"

    return counts


#判断结果是否重复
def has_repeat(counts,num):
    sum = 0;
    for count in counts:
        if count == counts[num] or count == 0:
            sum = sum + 1;
    return sum
