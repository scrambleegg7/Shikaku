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
import mojimoji

from MyZipClass import MyZipClass
from NIKKEIHokenClass import NIKKEIHokenClass

class HokenCheckClass(object):

    def __init__(self):

        self.data_dir = u"S:\\"
        self.output_dir = u"L:\\epson_pxm840f\\Shikakku"

        self.shikaku_tag = {}        
        self.shikaku = []

        # expand latest shikaku history file
        zipObject = MyZipClass()
        self.df_shikaku = zipObject.readZipFile()
        zipObject.toCsv(self.df_shikaku,"資格確認_保険証.csv")

        # read NIKKEI data to hold Domestic/Social Insurance
        nikkeiObject = NIKKEIHokenClass()
        self.df_nikkei = nikkeiObject.readShikaku()
        nikkeiObject.toCsv(self.df_nikkei)

    def dftoCsv(self,df, filename):

        filename = os.path.join(self.output_dir,filename)
        df.to_csv(filename, index=False, encoding='cp932', errors='replace')

    def mergeCheck(self):
        
        selected=['chozai','id','name','birth','hokenShu','hoken','kigo','bango','kouhi1','kouhi_jyu1','kouhi2','kouhi_jyu2',
            'kyufu','institution']

        df_nikkei = self.df_nikkei[selected].copy()
        df_nikkei = df_nikkei[~df_nikkei.duplicated()].copy()

        df_nikkei = df_nikkei[df_nikkei.id > 90009358].sort_values('id', ascending=False).copy()

        #print(df_nikkei.head(10))
        df_merged = pd.merge(df_nikkei,self.df_shikaku,on=["birth"], how="left")

        
        masks = (df_merged.hoken_x == df_merged.hoken_y) & (df_merged.kigo_x == df_merged.kigo_y )  &   \
             (df_merged.bango_x == df_merged.bango_y)


        print("** file output shikaku with NIKKEI confirmed.....")
        #print(df_merged[masks])
        self.toCsv(df_merged[masks],"NIKKEI_shikaku_confirmed.csv")

        print("** NON confirmed file output shikaku with NIKKEI .....")
        #print(df_merged[masks])
        self.toCsv(df_merged[~masks],"日計未確認.csv")


    def toCsv(self, df, filename):

        filename = os.path.join(self.output_dir,filename)
        df.to_csv(filename, index=False, encoding='cp932', errors='replace')


def main():

    myObject = HokenCheckClass()
    myObject.mergeCheck()

if __name__ == "__main__":
    main()