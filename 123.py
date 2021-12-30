import os
import functools
from numpy.core.fromnumeric import size
from numpy.core.numeric import NaN
from numpy.lib.shape_base import column_stack
from pandas.core.frame import DataFrame
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
import random
from iteration_utilities import duplicates

# # 顯示所有列
# pd.set_option('display.max_columns', None)
# # #顯示所有行
# pd.set_option('display.max_rows', None)


columns = ['Allele', 'Population.1', 'Frequency', 'sampleSize']
TotalChina = [[['A*31:01:02', 'China Zhejiang Han', 0.0283, 1734]], [['B*15:02:01', 'China Zhejiang Han', 0.0355, 1734]], [['B*57:01:01', 'China Zhejiang Han', 0.0061, 1734]], [['B*58:01', 'China Hubei Han', 0.0616, 3732]], [['B*15:11:01', 'China Zhejiang Han', 0.015, 1734]], [['B*13:01:01', 'China Zhejiang Han', 0.0438, 1734]], [], [['B*40:01:01', 'China Jingpo Minority', 0.068, 105]], [['C*01:02:01', 'China Zhejiang Han', 0.1765, 1734]], [['C*03:02', 'China Hubei Han', 0.0611, 3732]], [['A*33:03', 'China Hubei Han', 0.0742, 3732]], [['DRB1*01:01:01', 'China Zhejiang Han', 0.0141, 1734]], [['C*04:01:01:01', 'China North Han', 0.076, 105]], [['DPB1*03:01:01', 'China Inner Mongolia Autonomous Region Northeast', 0.057, 496]], [['A*02:07:01', 'China Zhejiang Han', 0.0975, 1734]], [['DRB1*14:01:01', 'China Inner Mongolia Autonomous Region Northeast', 0.031, 496]], [['DRB1*09:01:02', 'China Zhejiang Han', 0.1796, 1734]], [['DRB1*03:01', 'China Hubei Han', 0.0437, 3732]], [['DRB1*15:02:01', 'China Zhejiang Han', 0.0182, 1734]], [['DRB1*13:02:01', 'China Zhejiang Han', 0.03, 1734]], [['A*02:01', 'China Hubei Han', 0.1016, 3732]], [['B*48:01', 'China Hubei Han', 0.017, 3732]], [['C*08:01', 'China Hubei Han', 0.0785, 3732]], [['DRB1*07:01:01:01', 'China Inner Mongolia Autonomous Region Northeast', 0.124, 496]], [['DQA1*02:01', 'China Zhejiang Han pop 2', 0.0576, 833]], [['B*13:02:01', 'China Zhejiang Han', 0.047, 1734]], [['B*15:18:01', 'China Zhejiang Han', 0.0112, 1734]], [['B*15:19', 'China Hubei Han', 0.0001, 3732]], [['B*15:27:01', 'China Zhejiang Han', 0.0127, 1734]], [['B*27:09', 'China Tibet Region Tibetan', 0, 158]], [['B*38:02:01', 'China Zhejiang Han', 0.0311, 1734]], [['B*38:01:01', 'China Zhejiang Han', 0.0014, 1734]], [['B*48:04', 'China Zhejiang Han', 0.0003, 1734]], [['B*18:01:01', 'China Zhejiang Han', 0.0014, 1734]], [], [['B*15:05:01', 'China Zhejiang Han', 0.0003, 1734]], [], [], [['DRB1*11:01:01', 'China Zhejiang Han', 0.0681, 1734]], [['DRB1*03:01:01:01', 'China Inner Mongolia Autonomous Region Northeast', 0.059, 496]], [], [['A*02:01:01:01', 'China Yunnan Province Wa', 0.008, 119]], [['B*51:01:01', 'China Zhejiang Han', 0.0484, 1734]], [['B*46:01:01', 'China Zhejiang Han', 0.1148, 1734]], [['DQB1*06:02:01', 'China Zhejiang Han', 0.0559, 1734]], [], [['B*44:03:01', 'China Zhejiang Han', 0.0104, 1734]], [['C*14:03', 'China Hubei Han', 0.0067, 3732]], [['B*15:13:01', 'China Zhejiang Han', 0.0006, 1734]], [['DRB1*16:01:01', 'China Zhejiang Han', 0.0003, 1734]], [['DQB1*05:02:01', 'China Zhejiang Han', 0.0669, 1734]], [['B*44:02:01:01', 'China North Han', 0.01, 105]], [['B*40:02:01', 'China Zhejiang Han', 0.0245, 1734]], [['B*15:01:01:01', 'China Yunnan Province Wa', 0.042, 119]], [['DRB1*04:03:01', 'China Zhejiang Han', 0.015, 1734]], [['DRB1*04:01:01', 'China Zhejiang Han', 0.0087,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            1734]], [['A*24:02:01:01', 'China South Han', 0.172, 284]], [['A*11:01:01', 'China Zhejiang Han', 0.2581, 1734]], [['B*35:05:01', 'China Zhejiang Han', 0.0003, 1734]], [['DRB1*04:06:01', 'China Zhejiang Han', 0.0294, 1734]], [], [['C*02:02:01', 'China North Han', 0, 105]], [], [['C*07:01:01', 'China Zhejiang Han', 0.0017, 1734]], [['C*12:02:01', 'China Yunnan Province Lisu', 0.021, 111]], [['C*14:02:01', 'China Zhejiang Han', 0.0421, 1734]], [['C*15:02:01', 'China Zhejiang Han', 0.0297, 1734]], [], [], [['B*08:01:01', 'China Zhejiang Han', 0.0032, 1734]], [['B*27:05:02', 'China Zhejiang Han', 0.0046, 1734]], [], [['B*51:02:01', 'China Zhejiang Han', 0.0127, 1734]], [['B*54:01:01', 'China Zhejiang Han', 0.0317, 1734]], [['B*55:01:01', 'China Zhejiang Han', 0.0006, 1734]], [['B*55:02:01', 'China Zhejiang Han', 0.036, 1734]], [['B*56:01:01', 'China Zhejiang Han', 0.0032, 1734]], [['B*56:06', 'China Tibet Region Tibetan', 0.0, 158]], [], [['B*39:05:01', 'China Zhejiang Han', 0.0023, 1734]], [['B*39:06:01', 'China North Han', 0, 105]], [['B*39:09', 'China Hubei Han', 0.0005, 3732]], [['B*15:12', 'China Hubei Han', 0.0024, 3732]], [['B*15:24', 'China Beijing Shijiazhuang Tianjian Han', 0.001, 618]], [['B*15:25:01', 'China Zhejiang Han', 0.004, 1734]], [['B*15:32', 'China Hubei Han', 0.0008, 3732]], [['B*15:35', 'China Hubei Han', 0.0005, 3732]], [], [['B*35:10', 'China Tibet Region Tibetan', 0.0, 158]], [['C*04:03', 'China Hubei Han', 0.0086, 3732]], [['DRB1*01:02:01', 'China Zhejiang Han', 0.0006, 1734]], [['DRB1*10:01:01', 'China Zhejiang Han', 0.0124, 1734]], [['DRB1*08:01:01', 'China Inner Mongolia Autonomous Region Northeast', 0.002, 496]], [['DRB1*04:04:01', 'China Zhejiang Han', 0.0156, 1734]], [['DRB1*01:03', 'China Beijing Shijiazhuang Tianjian Han', 0.001, 618]], [['C*04:06', 'China South Han pop 2', 0.0005, 1098]], [['C*04:07', 'China Tibet Region Tibetan', 0.0, 158]], [], [['C*18:01', 'China Tibet Region Tibetan', 0.0, 158]], [['DRB1*15:01:01:01', 'China Inner Mongolia Autonomous Region Northeast', 0.098, 496]], [['DRB1*16:02:01', 'China Zhejiang Han', 0.0343, 1734]], [['A*32:01:01', 'China Zhejiang Han', 0.0081, 1734]], [], [], [['DQB1*02:01:01', 'China Zhejiang Han', 0.06, 1734]], [['DPB1*10:01', 'China Zhejiang Han pop 2', 0.0012, 833]], [['DRB1*08:03:02', 'China Zhejiang Han', 0.0954, 1734]], [['DQB1*06:01:01', 'China Yunnan Province Lisu', 0.136, 111]], [], [['B*15:21', 'China Hubei Han', 0.0001, 3732]], [['B*56:02', 'China Tibet Region Tibetan', 0.0, 158]], [['DQB1*02:02', 'China Hubei Han', 0.0557, 3732]], [['B*67:01:01', 'China Zhejiang Han', 0.0043, 1734]]]


TotalTaiwan = [[['A*31:01:02', 'Taiwan Atayal', 0.0, 106]], [], [], [['B*58:01', 'Taiwan Tzu Chi Cord Blood Bank', 0.098, 710]], [], [], [], [], [], [['C*03:02', 'Taiwan Han Chinese', 0.105, 504]], [['A*33:03', 'Taiwan Tzu Chi Cord Blood Bank', 0.104, 710]], [['DRB1*01:01:01', 'Taiwan Minnan and Hakka', 0.008, 190]], [], [['DPB1*03:01:01', 'Taiwan Ami pop 2', 0.01, 50]], [], [['DRB1*14:01:01', 'Taiwan Minnan and Hakka', 0.04, 190]], [['DRB1*09:01:02', 'Taiwan Minnan and Hakka', 0.155, 190]], [['DRB1*03:01', 'Taiwan Tzu Chi Cord Blood Bank', 0.088, 710]], [['DRB1*15:02:01', 'Taiwan Minnan and Hakka', 0.013, 190]], [['DRB1*13:02:01', 'Taiwan Minnan and Hakka', 0.037, 190]], [['A*02:01', 'Taiwan Tzu Chi Cord Blood Bank', 0.104, 710]], [['B*48:01', 'Taiwan Tzu Chi Cord Blood Bank', 0.017, 710]], [['C*08:01', 'Taiwan Han Chinese', 0.081, 504]], [], [['DQA1*02:01', 'Taiwan', 0.0, 65]], [], [], [], [], [['B*27:09', 'Taiwan Atayal', 0, 106]], [], [], [['B*48:04', 'Taiwan Atayal', 0.0, 106]], [], [], [], [], [], [['DRB1*11:01:01', 'Taiwan Minnan and Hakka', 0.058, 190]], [], [], [], [['B*51:01:01', 'Taiwan Atayal', 0.0, 106]], [], [], [], [], [['C*14:03', 'Taiwan pop 2', 0.001, 364]], [], [], [], [], [], [], [['DRB1*04:03:01',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     'Taiwan Minnan and Hakka', 0.04, 190]], [['DRB1*04:01:01', 'Taiwan Minnan and Hakka', 0.003, 190]], [], [], [], [['DRB1*04:06:01', 'Taiwan Minnan and Hakka', 0.013, 190]], [], [['C*02:02:01', 'Taiwan Atayal', 0, 106]], [], [], [], [], [], [], [], [], [], [], [['B*51:02:01', 'Taiwan Atayal', 0.0, 106]], [], [], [], [], [], [], [], [], [['B*39:09', 'Taiwan Atayal', 0.0, 106]], [['B*15:12', 'Taiwan Tzu Chi Cord Blood Bank', 0.003, 710]], [['B*15:24', 'Taiwan Atayal', 0.0, 106]], [], [['B*15:32', 'Taiwan Han Chinese', 0.002, 504]], [], [], [['B*35:10', 'Taiwan Atayal', 0.0, 106]], [['C*04:03', 'Taiwan Han Chinese', 0.019, 504]], [], [['DRB1*10:01:01', 'Taiwan Minnan and Hakka', 0.011, 190]], [], [['DRB1*04:04:01', 'Taiwan Minnan and Hakka', 0.011, 190]], [], [['C*04:06', 'Taiwan Han Chinese', 0.0, 504]], [['C*04:07', 'Taiwan Atayal', 0.0, 106]], [], [['C*18:01', 'Taiwan Atayal', 0.0, 106]], [], [['DRB1*16:02:01', 'Taiwan Minnan and Hakka', 0.071, 190]], [], [], [], [], [], [['DRB1*08:03:02', 'Taiwan Minnan and Hakka', 0.09, 190]], [], [], [['B*15:21', 'Taiwan Tzu Chi Cord Blood Bank', 0.001, 710]], [['B*56:02', 'Taiwan Tzu Chi Cord Blood Bank', 0.001, 710]], [['DQB1*02:02', 'Taiwan Han Chinese', 0.024, 504]], []]


def list_unpack(l):
    """拆開一層嵌套列表元組"""
    return functools.reduce(lambda x, y: x + y, l)


# unpack_TotalData = pd.DataFrame(list_unpack(TotalData), columns=columns)
# print(unpack_TotalData)
# df = unpack_TotalData.sort_values(by=['Frequency', 'Allele'], ascending=False)
# path_CSV = os.getcwd()
# print(df.to_csv('Result.csv'))
# print(unpack_TotalData.to_csv('1.csv'))
# print(df)


dfChina = pd.DataFrame(list_unpack(TotalChina), columns=columns)
dfTaiwan = pd.DataFrame(list_unpack(TotalTaiwan), columns=columns)
print(dfChina)
print(dfTaiwan)

SetChina = set(dfChina.Allele)
SetTaiwan = set(dfTaiwan.Allele)
print(SetChina)
print(SetTaiwan)
print('-----------------------')
OnlyChina = dfChina[dfChina.Allele.isin(list(SetChina-SetTaiwan))]
OnlyTaiwan = dfTaiwan[dfTaiwan.Allele.isin(list(SetTaiwan-SetChina))]
print(OnlyChina)
print(OnlyTaiwan)  # 空
print('-----------------------')

BothList = list(SetChina & SetTaiwan)
print(BothList)
print('-----------------------')

BothChina = dfChina[dfChina.Allele.isin(BothList)]
print(BothChina)
BothTaiwan = dfTaiwan[dfTaiwan.Allele.isin(BothList)]
print(BothTaiwan)
print('-----------------------')
print('-----------------------')
print('-----------------------')
print('-----------------------')

# 排China 與 台灣
OnlyChina = OnlyChina.sort_values(by=['Frequency'], ascending=False)
OnlyTaiwan = OnlyTaiwan.sort_values(by=['Frequency'], ascending=False)

# 排Both:Pair Allele
# Both = pd.merge(BothChina, BothTaiwan, on='Allele').drop(columns=['Population.1_y']).sort_values(by=['Frequency_x'], ascending=False)
Both = pd.merge(BothChina, BothTaiwan, on='Allele').sort_values(
    by=['Frequency_x'], ascending=False)
Both.columns = ['Allele', 'Population.C', 'FrequencyChina',
                'sampleSizeChina', 'Population.T', 'FrequencyTaiwan', 'sampleSizeTaiwan']
# print(Both)


"""
12123
"""
# Pair
# labels = Both['Allele'].tolist()
# dataC = Both['FrequencyChina'].tolist()
# dataT = Both['FrequencyTaiwan'].tolist()

# NotPair
# labels = OnlyChina['Allele'].tolist()
# dataC = OnlyChina['Frequency'].tolist()
# dataT =
labels = OnlyTaiwan['Allele'].tolist()
dataC = OnlyTaiwan['Frequency'].tolist()

width = 0.4
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', 'r', 'b']
xpos = np.arange(0, len(labels), 1)

# 生成柱状图
fig, ax = plt.subplots(figsize=(10, 8))
bars1 = plt.bar(xpos-width/2, dataC, align='center', width=width,
                alpha=0.9, color='#1f77b4', label='China')
# bars2 = plt.bar(xpos+width/2, dataT, align='center', width=width,
#                 alpha=0.9, color='#ff7f0e', label='Taiwan')
# 設定每個柱子下面的記號
fig.autofmt_xdate(rotation=45)
ax.set_xticks(xpos)  # 確定每個記號的位置
ax.set_xticklabels(labels)  # 確定每個記號的內容

# 給每個柱子上面新增標註


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",  # 相對於被註釋點xy的偏移量（單位是點）
                    ha='center', va='bottom', size=5
                    )


autolabel(bars1)
# autolabel(bars2)

# 展示結果
plt.legend()
plt.show()
