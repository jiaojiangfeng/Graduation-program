#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-26 16:12:56
# @Author  : Jiang Feng (jaychou19961107@gmail.com)
# @Link    : http://www.jiaojfeng.com
# @Version : $Id$

import os

import pandas as pd

import numpy as np

from datetime import datetime

class DataProcessing():
	"""数据检查及统计"""

	def __init__(self, path=r'data\train.csv'):
		"""初始化属性"""
		self.path = path
		self.df = pd.read_csv(self.path)
		print('\rData import succeeded !!')

	def load_data(self):
		"""检查数据"""
		print(self.df.head(5))
		print(np.where(np.isnan(self.df)))
		self.df.info()
		nou = np.size(self.df.uid.unique())
		nop = np.size(self.df.iid.unique())
		print('用户数:%s' %nou)
		print('产品数:%s' %nop)
		# 查看每个用户对每个商品的评价次数
		group = self.df.groupby([self.df.uid,self.df.iid])
		group_max =group.score.count().max()
		group_min = group.score.count().min()
		group_mean = group.mean().reset_index()
		if group_max and group_min == 1:
			print('Each user only evaluated each product once.')
		else:
			group_mean.to_csv('grou_mean',header=0)
		
	def sample_df(self,n=0.1):
		"""数据抽取"""
		df_train = self.df.sample(frac=n,random_state=1)
		df_train.to_csv('SampleData',index=False,header=False)

	def create_uid_info(self):
		"""构建用户详情表"""
		uid_df = self.df.loc[:,['uid','score','time']]
		# 对data分组
		first_time = uid_df['time'].groupby(uid_df['uid']).min()
		last_time = uid_df['time'].groupby(uid_df['uid']).max()
		buy  = uid_df['score'].groupby(uid_df['uid']).count()
		# 将分组后的series对象转为字典
		first_time = {'uid':first_time.index,'f_time':first_time.values}
		last_time = {'uid':last_time.index,'l_time':last_time.values}
		buy = {'uid':buy.index,'b_count':buy.values}
		# 再转为pandas的DataFrame对象
		first_time_df = pd.DataFrame(first_time)
		last_time_df = pd.DataFrame(last_time)
		buy_df = pd.DataFrame(buy)
		# 对三个df对象根据uid合并
		mg = pd.merge(buy_df,first_time_df,on='uid')
		mg = pd.merge(mg,last_time_df,on='uid')
		# 计算第一次和最后一次的时间差
		user = mg.eval('timedifference=l_time-f_time')
		# 转为时间戳
		user['l_time'] = user['l_time'].apply(lambda x: pd.to_datetime(x, unit='s'))
		user['f_time'] = user['f_time'].apply(lambda x:pd.to_datetime(x, unit='s'))
		user['timedifference'] = user['timedifference'].apply(lambda x:pd.to_datetime(x, unit='s'))
		user.to_csv('user_info',index=False)
		print('Completed!!!')

	def create_iid_info(self):
		"""构建物品详情表"""	
		iid_df = self.df.loc[:,['iid','score']]
		# 对data分组
		i_score_mean = iid_df['score'].groupby(iid_df['iid']).mean()
		i_score_count = iid_df['score'].groupby(iid_df['iid']).count()
		# 将分组后的series对象转为字典
		i_score_mean = {'iid':i_score_mean.index,'score_mean':i_score_mean.values}
		i_score_count = {'iid':i_score_count.index,'score_count':i_score_count.values}
		# 再转为pandas的DataFrame对象
		i_score_mean = pd.DataFrame(i_score_mean)
		i_score_count = pd.DataFrame(i_score_count)
		# 对两个个df对象根据iid合并
		articles = pd.merge(i_score_mean,i_score_count,on='iid')
		# 商品评分分箱
		articles['labe'] = pd.cut(articles['score_mean'],[1,1.5,2.5,3.5,4.5,5],labels=['一星','二星','三星','四星','五星'])
		articles.to_csv('articles_info',index=False)
		print('Completed!!!')


df = DataProcessing()
df.load_data()
df.create_iid_info()
df.create_uid_info()
df.sample_df()

