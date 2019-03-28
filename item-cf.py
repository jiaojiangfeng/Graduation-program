#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-26 17:05:58
# @Author  : Jiang Feng (jaychou19961107@gmail.com)
# @Link    : http://www.jiaojfeng.com
# @Version : $Id$
from surprise import Reader, Dataset,evaluate,print_perf,KNNBaseline
import os


def start(goods='951'):
	
	file_path = os.path.expanduser('SampleData')
	# 指定文件格式
	reader = Reader(line_format='user item rating timestamp', sep=',')
	# 从文件读取数据
	data = Dataset.load_from_file(file_path, reader=reader)

	trainset = data.build_full_trainset()
	sim_options = {'name':'pearson_baseline','user_based': False}
	    ##使用KNNBaseline算法
	algo = KNNBaseline(sim_options=sim_options)
	algo.train(trainset)

	iid_innerid = algo.trainset.to_inner_iid(goods)

	
	iid_neighbors = algo.get_neighbors(iid_innerid,k=10)

	
	iid_neighbors = (algo.trainset.to_raw_iid(inner_id)
	                       for inner_id in iid_neighbors)



	print('The 10 nearest neighbors of %s:' %goods)
	for iid in iid_neighbors:
	    print(iid)



start()
