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

from MyMasterClass import MyMasterClass
from HOKENKeyClass import HokenKeyClass

class NIKKEIHokenClass(MyMasterClass):

    def __init__(self,data_dir = u"L:\\Miyuki"):

        #self.data_dir = u"L:\\Miyuki"
        self.data_dir = data_dir
        self.output_dir = u"L:\\epson_pxm840f\\Shikakku"

        self.filename = os.path.join(self.data_dir,"NIKKEI.TXT")

        # 保険番号convert Class
        self.HOKENKeyObject = HokenKeyClass()

    def readShikaku(self):

        read_data_types = {"保険者番号":str,  "被保険者記号":str, "被保険者番号":str ,
                            '公費負担者番号１':str,
                            '公費受給番号１':str,
                            '公費負担者番号２':str,
                            '公費受給番号２':str,
                            }

        self.df = pd.read_csv(self.filename,encoding='cp932', dtype=read_data_types)
        targetCols = ['調剤日',
        '患者No',
        '患者名',
        '患者フリガナ',
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

        newcolname=['chozai','id','Name','Kana','birth','InsurerSegment','InsurerNumber', 
                'InsuredCardSymbol','InsuredIdentificationNumber','kouhi1','kouhi_jyu1','kouhi2','kouhi_jyu2',
                'kyufu','institution','accept_counts','prescript_counts','total','paid']

        df.columns = newcolname
        df = df[df.institution != "東武練馬ｸﾘﾆｯｸ"].copy()
        df = df[ ~df.InsurerSegment.isin(["自費","公単", "労災"]) ].copy()


        df['kouhi1'] = df['kouhi1'].fillna("")
        df['kouhi_jyu1'] = df['kouhi_jyu2'].fillna("")
        df['kouhi2'] = df['kouhi2'].fillna("")
        df['kouhi_jyu2'] = df['kouhi_jyu2'].fillna("")

        self.HOKENKeyObject.setData(
                    df["InsurerNumber"],
                    df["InsuredCardSymbol"],
                    df["InsuredIdentificationNumber"],
                    None
           )
        df_HOKEN = self.HOKENKeyObject.operation()

        df["InsurerNumber"] = df_HOKEN["InsurerNumber"]
        df["InsuredCardSymbol"] = df_HOKEN["InsuredCardSymbol"]
        df["InsuredIdentificationNumber"] = df_HOKEN["InsuredIdentificationNumber"]

        # Exclude MealCoupon Dealers / mental patient
        df = df[ ((df.kouhi1.str[:2] != "12") & (df.kouhi1.str[:2] != "15")) ].copy()

        df.reset_index(drop=True,inplace=True)
        df.fillna("",inplace=True)

        return df

    #def toCsv(self,df, filename="NIKKEI_hoken.csv"):
    #    NIKKEI = os.path.join(self.output_dir,filename)
    #    df.to_csv(NIKKEI, encoding='cp932', errors='replace', index=False)





def main():

    nkObject = NIKKEIHokenClass()
    df = nkObject.readShikaku()

    selectObj = ["InsurerNumber","InsuredCardSymbol","InsuredIdentificationNumber"]
    df = df[selectObj].copy()

    print(df.head(3))
    print(df.tail(3))
    #print()
    #zipObject.toCsv(df,"shikaku.csv")



if __name__ == "__main__":
    main()