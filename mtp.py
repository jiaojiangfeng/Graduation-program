#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-28 13:28:43
# @Author  : Jiang Feng (jaychou19961107@gmail.com)
# @Link    : http://www.jiaojfeng.com
# @Version : $Id$

import pandas as pd

import matplotlib.pyplot as plt

import numpy as np


def iid_head(path=r'data\train.csv'):
	plt.rcParams['font.sans-serif']=['SimHei']
	plt.rcParams['axes.unicode_minus'] = False
	df = pd.read_csv(path)
	df_count = df.iid.value_counts().head(10)
	print(df_count)
	labels = df_count.index
	sizes = df_count.values
	plt.pie(sizes,labels=labels,autopct='%1.3f%%',labeldistance=1.1,startangle=90,shadow=False,pctdistance=0.7)

	# plt.legend(loc='upper right')
	plt.show()

def score_info(path=r'articles_info'):

	plt.rcParams['font.sans-serif']=['SimHei']
	plt.rcParams['axes.unicode_minus'] = False

	df = pd.read_csv(path)
	score_count = df['labe'].value_counts()
	print(score_count)
	labels = score_count.index
	sizes = score_count.values
	plt.pie(sizes,labels=labels,autopct='%1.1f%%',labeldistance=1.1,startangle=90,shadow=False,pctdistance=0.7)

	# plt.legend(loc='upper right')
	plt.show()

iid_head()
score_info()