#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-29 11:13:48
# @Author  : Jiang Feng (jaychou19961107@gmail.com)
# @Link    : http://www.jiaojfeng.com
# @Version : $Id$
import os
from surprise import SVD
from surprise import Dataset
from surprise import accuracy,Reader
from surprise.model_selection import train_test_split

file_path = os.path.expanduser('SampleData')
# 指定文件格式
reader = Reader(line_format='user item rating timestamp', sep=',')
# 从文件读取数据
data = Dataset.load_from_file(file_path, reader=reader)

# 0.25分割数据
trainset, testset = train_test_split(data, test_size=.25)

# 创建实例开始训练
algo = SVD()

algo.fit(trainset)

predictions = algo.test(testset)

# RMSE 评价指标
accuracy.rmse(predictions)
