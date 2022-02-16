# %% [markdown]
# # Load Library

# %%
import xml.etree.ElementTree as ET
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from scipy.stats import pearsonr
from sklearn import preprocessing

import zipfile
from glob import glob

import seaborn as sns
from sympy import subsets
sns.set()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

#import japanize_matplotlib
import unicodedata

class NIKKEIHokenClass(object):

    def __init__(self,data_dir = u"L:\\Miyuki"):

        #self.data_dir = u"L:\\Miyuki"
        self.data_dir = data_dir
        self.output_dir = u"L:\\epson_pxm840f\\Shikakku"

        self.filename = os.path.join(self.data_dir,"NIKKEI.TXT")

    def readShikaku(self):

        self.df = pd.read_csv(self.filename,encoding='cp932')
        targetCols = ['調剤日',
        '患者No',
        '患者名',
        '生年月日',
        '保険種類',
        '保険者番号',
        '被保険者記号',
        '被保険者番号',
        '公費負担者番号１',
        '公費受給番号１',
        '公費負担者番号２',
        '公費受給番号２',
        '給付割合',
        '医療機関',
        '受付回数',
        '処方箋枚数',
        '保険合計(点)',
        '患者負担金(円)']

        df= self.df[targetCols].copy()

        newcolname=['chozai','id','name','birth','hokenShu','hoken','kigo','bango','kouhi1','kouhi_jyu1','kouhi2','kouhi_jyu2',
            'kyufu','institution','accept_counts','prescript_counts','total','paid']

        df.columns = newcolname
        df['kouhi1'] = df['kouhi1'].fillna(0).apply(int).apply(str).replace(['0'],' ')
        df['kouhi_jyu1'] = df['kouhi_jyu2'].fillna(0).apply(int).apply(str).replace(['0'],' ')
        df['kouhi2'] = df['kouhi2'].fillna(0).apply(int).apply(str).replace(['0'],' ')
        df['kouhi_jyu2'] = df['kouhi_jyu2'].fillna(0).apply(int).apply(str).replace(['0'],' ')
        df['hoken'] = df['hoken'].fillna(0).apply(int).apply(str).replace(['0'],' ')
        df['kigo'] = [unicodedata.normalize("NFKC",str(z)) for z in df['kigo'].fillna("").apply(str)]
        # special purpose to change hyfun chord of Japanese
        df['kigo'] = [ s.replace('\u2010','-') for s in df['kigo'].tolist() ]

        df['bango'] = [unicodedata.normalize("NFKC",str(z)) for z in df['bango'].fillna("").apply(str)]

        df.reset_index(drop=True,inplace=True)

        print(df.dtypes)


        return df

    def toCsv(self,df, filename="NIKKEI_hoken.csv"):

        NIKKEI = os.path.join(self.output_dir,filename)
        df.to_csv(NIKKEI, encoding='cp932', errors='replace', index=False)

