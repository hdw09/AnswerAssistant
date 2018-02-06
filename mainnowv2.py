#!/usr/bin/python2.7
# coding=utf-8

# 导入所需要的包
from matplotlib import pyplot as plt
from PIL import Image
from plotImg import markRect
from plotImg import Box2Rect
from plotImg import baidu_OCR
import numpy as np
from PIL import ImageGrab
import webbrowser
from urllib import urlencode
import argparse
from solve_utils import words_count
from solve_utils import search_count
import os

from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("http://www.baidu.com")

def serchInChrome(question):
	driver.get('https://baidu.com/s?' + urlencode({"wd":question}))

def highlightAnswers(answers):
	jsText = "function keyLight(keyword,mycolor){var body=document.getElementById('wrapper');var bodyText=body.innerHTML;var keywordSpan='<span style=\\'background-color:'+ mycolor +';\\'>'+keyword+'</span>';var regStr=new RegExp(keyword,'g');bodyText=bodyText.replace(regStr,keywordSpan);body.innerHTML=bodyText};";
	for answer in answers:
		answer = answer.encode('utf-8')
		if len(answer) > 0:
			jsText = jsText + "keyLight('"+ answer +"', 'orange');"
	jsText = jsText + "keyLight('最佳答案', 'pink');"
	jsText = jsText + "keyLight('答案:', 'pink');"
	try: driver.execute_script(jsText)
	except:
		print "highlightAnswers error!!!"
        return 1
	return 0
def showAnswersCheck(words_sc, search_sc):
	jsText = "var contentRight = document.getElementById('content_right');"
	words_sc.sort(lambda x,y: cmp(y['num'], x['num']))
	search_sc.sort(lambda x,y: cmp(y['num'], x['num']))

	htmlText = "<h3>"+ "搜索问题得到的答案中各个选项匹配的次数:" +"</h3><ul>"
	count = 1
	for par in words_sc:
		htmlText = htmlText + "<li>" + str(count) + ".  " + par['answer'].encode('utf-8') + ":" + str(par['num']) +"</li>"
		count = count + 1
	htmlText = htmlText + "</ul><br/><br/>"
	htmlText = htmlText + "<h3>"+ "问题和答案一起搜各个选择得到的结果：" +"</h3><ul>"
	count = 1
	for par in search_sc:
		htmlText = htmlText + "<li>" + str(count) + ".  " + par['answer'].encode('utf-8') + "</li>"
		count = count + 1
	htmlText = htmlText + "</ul><br/><br/>"
	jsText = jsText + "contentRight.innerHTML = " + "'"+ htmlText +"';"
	try: driver.execute_script(jsText)
	except:
		print "showAnswersCheck error!!!"
        return 1
	return 0

def doTheJob():
	# 读取测试图片
	testImage = ImageGrab.grab((1, 46, 690, 1288))
	size = testImage.size #size[0] 宽 750  size[1] 高
	scaleSize = size[0] / 750.0

	questionBox = [50,330,655,190]
	questionSubImage = testImage.crop(Box2Rect(questionBox, scaleSize))

	answerABox = [120,545,500,98] # x,y,w,h
	answerASubImage = testImage.crop(Box2Rect(answerABox, scaleSize))

	answerBBox = [120,answerABox[1] + 20 + answerABox[3],answerABox[2],answerABox[3]]
	answerBSubImage = testImage.crop(Box2Rect(answerBBox, scaleSize))

	answerCBox = [120,answerABox[1] + (20 + answerABox[3]) * 2,answerABox[2],answerABox[3]]
	answerCSubImage = testImage.crop(Box2Rect(answerCBox, scaleSize))

	# 百度OCR
	questionText = baidu_OCR(questionSubImage).encode('utf-8')
	#webbrowser.open('https://baidu.com/s?' + urlencode({"wd":questionText}))
	serchInChrome(questionText)

	answers = []
	answerAText = baidu_OCR(answerASubImage)
	answers.append(answerAText)

	answerBText = baidu_OCR(answerBSubImage)
	answers.append(answerBText)

	answerCText = baidu_OCR(answerCSubImage)
	answers.append(answerCText)

	highlightAnswers(answers)

	#words_sc = words_count(questionText,answers)
	#search_sc = search_count(questionText,answers)
	#showAnswersCheck(words_sc, search_sc)

def go():
    goOn = True
    while goOn:
    	print "回车识别下一题，输入q可退出程序"
    	inputValue = raw_input(": ")
    	os.system('clear')
    	if inputValue == "q":
    		driver.close()
    		exit()
    	else:
    		doTheJob()
go()


