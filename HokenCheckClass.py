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
from MyKanjyaClass import MyKanjyaClass

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
        nikkeiObject.toCsv(self.df_nikkei, filename="NIKKEI_hoken.csv")

        kanjyaObject = MyKanjyaClass()
        self.df_kanjya = kanjyaObject.readCSV()
        kanjyaObject.toCsv(self.df_kanjya,"kanjya.csv")

    def dftoCsv(self,df, filename):
        super().toCsv(df, filename)
        #filename = os.path.join(self.output_dir,filename)
        #df.to_csv(filename, index=False, encoding='cp932', errors='replace')

    def mergeCheck(self):
        
        selected=['chozai','id','Name','birth','InsurerSegment','InsurerNumber',
                    'InsuredCardSymbol','InsuredIdentificationNumber',
                    'kouhi1','kouhi_jyu1','kouhi2','kouhi_jyu2',
                    'kyufu','institution']

        df_nikkei = self.df_nikkei[selected].copy()
        df_nikkei = df_nikkei[~df_nikkei.duplicated()].copy()

        df_nikkei = pd.merge(df_nikkei, self.df_kanjya, on=["id"], how="left")

        #print(df_nikkei.columns)
        #df_nikkei = df_nikkei[df_nikkei.id > 90009358].sort_values('id', ascending=False).copy()
        #selectednew=['chozai','id','Name_x','birth_x','InsurerSegment','InsurerNumber',
        #            'InsuredCardSymbol','InsuredIdentificationNumber',
        #            'kouhi1','kouhi_jyu1','kouhi2','kouhi_jyu2',
        #            'kyufu','institution']
        #df_nikkei[selectednew].columns = selected
        #print(df_nikkei.head(10))
        df_merged = pd.merge(df_nikkei,self.df_shikaku,on=["birth"], how="left")        
        df_merged_name = pd.merge(df_nikkei,self.df_shikaku,on=["Name"], how="left")

              
        masks = (df_merged.InsurerNumber_x == df_merged.InsurerNumber_y)  &  \
            (df_merged.InsuredCardSymbol_x == df_merged.InsuredCardSymbol_y )  &   \
             (df_merged.InsuredIdentificationNumber_x == df_merged.InsuredIdentificationNumber_y) & \
                 (df_merged.sex1 == df_merged.sex2)

        masks_name = (df_merged_name.InsurerNumber_x == df_merged_name.InsurerNumber_y)  &  \
            (df_merged_name.InsuredCardSymbol_x == df_merged_name.InsuredCardSymbol_y )  &   \
             (df_merged_name.InsuredIdentificationNumber_x == df_merged_name.InsuredIdentificationNumber_y) & \
                 (df_merged_name.sex1 == df_merged_name.sex2)

        print("** file output shikaku with NIKKEI confirmed.....")
        #print(df_merged[masks])
        self.toCsv(df_merged[masks],"NIKKEI_shikaku_confirmed.csv")


        print("** NON confirmed file output shikaku with NIKKEI .....")
        #print(df_merged[masks])
        self.toCsv(df_merged[~masks],"日計未確認_byBirth.csv")


        print("** NON confirmed file output shikaku with NIKKEI by Name.....")
        #print(df_merged[masks])
        #self.toCsv(df_merged_name[~masks_name],"日計未確認_byName.csv")

        selected_df = df_merged_name[~masks_name].copy()
        #print(selected_df.columns  )
        target = ["Name","birth_x","InsurerNumber_x", "InsuredCardSymbol_x", "InsuredIdentificationNumber_x"]

        selected_df = selected_df[target].copy()
        selected_df.columns = ["Name","birth","InsurerNumber", "InsuredCardSymbol", "InsuredIdentificationNumber"]
        df_merged_name = pd.merge(selected_df,self.df_shikaku,on=["InsurerNumber", "InsuredCardSymbol", "InsuredIdentificationNumber"], how="left")
        self.toCsv(df_merged_name,"日計未確認_byName.csv")


        #self.df_shikaku.InsurerNumber 


    def toCsv(self, df, filename):

        filename = os.path.join(self.output_dir,filename)
        df.to_csv(filename, index=False, encoding='cp932', errors='replace')


def main():

    myObject = HokenCheckClass()
    myObject.mergeCheck()

if __name__ == "__main__":
    main()