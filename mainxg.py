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
from solve_utils import find_max
from solve_utils import find_min
import os

def doTheJob():
	# 读取测试图片
	testImage = ImageGrab.grab((1, 46, 690, 1288))
	size = testImage.size #size[0] 宽 750  size[1] 高
	scaleSize = size[0] / 750.0

	questionBox = [55,165,645,255]
	questionSubImage = testImage.crop(Box2Rect(questionBox, scaleSize))

	answerABox = [105,440,545,100] # x,y,w,h
	answerASubImage = testImage.crop(Box2Rect(answerABox, scaleSize))

	answerBBox = [105,answerABox[1] + 32 + answerABox[3],answerABox[2],answerABox[3]]
	answerBSubImage = testImage.crop(Box2Rect(answerBBox, scaleSize))

	answerCBox = [105,answerABox[1] + (32 + answerABox[3]) * 2,answerABox[2],answerABox[3]]
	answerCSubImage = testImage.crop(Box2Rect(answerCBox, scaleSize))

	# 百度OCR
	questionText = baidu_OCR(questionSubImage).encode('utf-8')
	webbrowser.open('https://baidu.com/s?' + urlencode({"wd":questionText}))

	answers = []
	answerAText = baidu_OCR(answerASubImage)
	answers.append(answerAText)

	answerBText = baidu_OCR(answerBSubImage)
	answers.append(answerBText)

	answerCText = baidu_OCR(answerCSubImage)
	answers.append(answerCText)

	sc = words_count(questionText,answers)
	print "|"
	print answers[find_min(sc)].encode('utf-8') + " 在答案中出现的最少"
	print answers[find_max(sc)].encode('utf-8') + " 在答案中出现的最多"
	print "\n"

	sc = search_count(questionText,answers)
	print "|"
	print answers[find_min(sc)].encode('utf-8') + " 的结果最少"
	print answers[find_max(sc)].encode('utf-8') + " 的结果最多"
	print "\n"


def go():
    goOn = True
    while goOn:
    	print "回车识别下一题，输入q可退出程序"
    	inputValue = raw_input(": ")
    	os.system('clear')
    	if inputValue == "q":
    		exit()
    	else:
    		doTheJob()
go()


