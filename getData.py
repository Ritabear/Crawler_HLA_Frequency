import pandas as pd
import re
from collections import OrderedDict


df = pd.read_csv('clinicalVariants.tsv', sep='\t')
# print(df.shape)  # (4920, 6)
listHLA = []
# HLA = df.loc[df['gene'].str.contains('HLA', na=False)]
HLA = df.loc[df['variant'].str.contains('HLA', na=False)]

# print(HLA.shape)
# print(HLA['variant']) # 180
HLA_List = HLA['variant'].tolist()
# print(HLA_List)
# print(len(HLA_List))
OnlyAllele = []
characters = "HLA-"
for i in range(0, len(HLA_List)):
    HLA_Split = HLA_List[i].split(', ')
    for j in range(0, len(HLA_Split)):
        OnlyAllele.append(HLA_Split[j].replace(characters, ''))
        # print(HLA_Split[j].replace(characters, ''))

# print(OnlyAllele)  # 175 #'B*59:01:01:01', 'B*59:01:01:01'
# print(len(OnlyAllele))

OnlyAllele = list(OrderedDict.fromkeys(OnlyAllele))
# print(OnlyAllele)
# print(len(OnlyAllele))
"""
# 不同方式驗證重複
final_list = list(OrderedDict.fromkeys(OnlyAllele))

print(final_list)
print(len(final_list))

print('--------------------------')
resultantList = []

for element in OnlyAllele:
    if element not in resultantList:
        resultantList.append(element)

print(resultantList)
print(len(resultantList))
"""
