from numpy.core.numeric import NaN
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import random
import functools
import os


from getData import OnlyAllele
from DrawBarClass import DrawBar

# # 顯示所有列
# pd.set_option('display.max_columns', None)
# # #顯示所有行
# pd.set_option('display.max_rows', None)


HLA_Url = OnlyAllele
page = '1'


def main():
    baseurl = "http://www.allelefrequencies.net/hla6006a.asp?page=" + \
        page+"&hla_region=South-East+Asia&hla_selection="
    # 1.爬取網页
    TotalChina, TotalTaiwan = getData(baseurl)
    # 3.處理數據
    Both, OnlyChina, OnlyTaiwan = dealData(TotalChina, TotalTaiwan)

    # 4.畫圖
    # draw = DrawBar()
    # Pair
    labels = Both['Allele'].tolist()
    dataC = Both['FrequencyChina'].tolist()
    dataT = Both['FrequencyTaiwan'].tolist()
    DrawBar.drawDoubleBar(labels, dataC, dataT)

    # NotPair
    labels = OnlyChina['Allele'].tolist()
    data1 = OnlyChina['Frequency'].tolist()
    DrawBar.drawDoubleBar(labels, data1)


# 爬取網页
def getData(baseurl):
    TotalData = []
    TotalChina = []
    TotalTaiwan = []
    num = 0
    for i in range(0, len(HLA_Url)):
        url = baseurl+HLA_Url[i]
        print(url)
        num += 1
        print(num)
        html = askURL(url)
        # 2.逐一解析數據
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find('table', class_='tblNormal')
        if table != None:
            df = pd.read_html(str(table))[0]
            df.columns = ['Line', 'Allele', 'Population', 'Population.1',  'individual', 'Frequency',
                          'img', 'sampleSize', 'Database', 'Distribution', 'Association', 'Notes']

            # China
            if df['Population.1'].str.contains('China').any():
                China = df.loc[df['Population.1'].str.contains(
                    'China'), ['Allele', 'Population.1', 'Frequency', 'sampleSize']]
                ChinaMax_Index = China['sampleSize'].idxmax(
                    skipna=True)
                ChinaMax = China.loc[ChinaMax_Index:ChinaMax_Index]

            else:
                ChinaMax = pd.DataFrame()

            # Taiwan
            if df['Population.1'].str.contains('Taiwan').any():
                Taiwan = df.loc[df['Population.1'].str.contains(
                    'Taiwan'), ['Allele', 'Population.1', 'Frequency', 'sampleSize']]
                TaiwanMax_Index = Taiwan['sampleSize'].idxmax(skipna=True)
                TaiwanMax = Taiwan.loc[TaiwanMax_Index:TaiwanMax_Index]
            else:
                TaiwanMax = pd.DataFrame()

            res = pd.concat([ChinaMax, TaiwanMax])

            TotalData.append(res.values.tolist())
            TotalChina.append(ChinaMax.values.tolist())
            TotalTaiwan.append(TaiwanMax.values.tolist())
        else:
            TotalData.append([])
            TotalChina.append([])
            TotalTaiwan.append([])

    return TotalChina, TotalTaiwan


# 得到指定一个URL的網頁内容
def askURL(url):
    head = {  # 模擬瀏覽器信息，向伺服器發送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    time.sleep(random.uniform(1, 5))
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def list_unpack(l):
    """拆開一層嵌套列表元組"""
    return functools.reduce(lambda x, y: x + y, l)


def dealData(TotalChina, TotalTaiwan):
    columns = ['Allele', 'Population.1', 'Frequency', 'sampleSize']

    dfChina = pd.DataFrame(list_unpack(TotalChina), columns=columns)
    dfTaiwan = pd.DataFrame(list_unpack(TotalTaiwan), columns=columns)

    SetChina = set(dfChina.Allele)
    SetTaiwan = set(dfTaiwan.Allele)

    OnlyChina = dfChina[dfChina.Allele.isin(list(SetChina-SetTaiwan))]
    OnlyTaiwan = dfTaiwan[dfTaiwan.Allele.isin(list(SetTaiwan-SetChina))]
    # print(OnlyTaiwan)  # 空

    BothList = list(SetChina & SetTaiwan)
    BothChina = dfChina[dfChina.Allele.isin(BothList)]
    BothTaiwan = dfTaiwan[dfTaiwan.Allele.isin(BothList)]

    # 排China 與 台灣
    OnlyChina = OnlyChina.sort_values(by=['Frequency'], ascending=False)
    OnlyTaiwan = OnlyTaiwan.sort_values(by=['Frequency'], ascending=False)

    # 排Both:Pair Allele
    Both = pd.merge(BothChina, BothTaiwan, on='Allele').sort_values(
        by=['Frequency_x'], ascending=False)
    Both.columns = ['Allele', 'Population.C', 'FrequencyChina',
                    'sampleSizeChina', 'Population.T', 'FrequencyTaiwan', 'sampleSizeTaiwan']
    # print(Both)

    return Both, OnlyChina, OnlyTaiwan


if __name__ == "__main__":
    start = time.time()
    # 調用函数
    main()
    end = time.time()
    print("爬取完畢！:"+str(end - start))
