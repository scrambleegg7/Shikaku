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
from RECEPTHokenClass import RECEPTHokenClass

from MyMasterClass import MyMasterClass

class RECEPTHokenCheckClass(MyMasterClass):

    def __init__(self):

        self.data_dir = u"S:\\"
        self.output_dir = u"L:\\epson_pxm840f\\Shikakku"

        self.shikaku_tag = {}        
        self.shikaku = []

        # expand latest shikaku history file
        zipObject = MyZipClass()
        self.df_shikaku = zipObject.readZipFile()

        # change pd_datetime to merge recept class
        self.df_shikaku.birth = pd.to_datetime( self.df_shikaku.birth )    
        #zipObject.toCsv(self.df_shikaku,"資格確認_保険証.csv")
        #print("shikaku file size : ", self.df_shikaku.shape)

        # read NIKKEI data to hold Domestic/Social Insurance
        receptObj = RECEPTHokenClass()
        df = receptObj.integrateInsurancedata()

        self.df_recept = df[ ((df.kouhi1.str[:2] != "12") & (df.kouhi1.str[:2] != "15")) ].copy()
        print("RECEPT file size : ", self.df_recept.shape)

    def dftoCsv(self,df, filename):
        super().toCsv(df, filename)
        #filename = os.path.join(self.output_dir,filename)
        #df.to_csv(filename, index=False, encoding='cp932', errors='replace')

    def mergeCheck(self):
        
        selected=['chozai','id','Name','birth','InsurerSegment','InsurerNumber',
                    'InsuredCardSymbol','InsuredIdentificationNumber',
                    'kouhi1','kouhi_jyu1','kouhi2','kouhi_jyu2',
                    'kyufu','institution']

    
        df_merged = pd.merge(self.df_recept, self.df_shikaku, on=["Name", "birth"], how="left")
        df_merged.fillna("", inplace=True)

        masks = (df_merged.InsurerNumber_x.apply(str) == df_merged.InsurerNumber_y.apply(str))  &  \
            (df_merged.InsuredCardSymbol_x.apply(str) == df_merged.InsuredCardSymbol_y.apply(str) )  &   \
             (df_merged.InsuredIdentificationNumber_x.apply(str) == df_merged.InsuredIdentificationNumber_y.apply(str)) & \
                 (df_merged.sex.apply(str) == df_merged.sex1.apply(str))

        print("** NON confirmed file output shikaku with RECEPT file .....")
        #print(df_merged[masks])
        self.toCsv(df_merged[~masks],"レセプト_byBirthName.csv")





def main():


    obj = RECEPTHokenCheckClass()
    obj.mergeCheck()




if __name__ == "__main__":
    main()