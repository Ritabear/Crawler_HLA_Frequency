import pandas as pd
import re
from collections import OrderedDict


df = pd.read_csv('clinicalVariants.tsv', sep='\t')
listHLA = []
HLA = df.loc[df['variant'].str.contains('HLA', na=False)]
HLA_List = HLA['variant'].tolist()

OnlyAllele = []
characters = "HLA-"
for i in range(0, len(HLA_List)):
    HLA_Split = HLA_List[i].split(', ')
    for j in range(0, len(HLA_Split)):
        OnlyAllele.append(HLA_Split[j].replace(characters, ''))

# print(len(OnlyAllele)) #175

OnlyAllele = list(OrderedDict.fromkeys(OnlyAllele))
