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
import csv
import codecs
import glob
import mojimoji


from MyMasterClass import MyMasterClass



class HokenKeyClass(object):

    def __init__(self):


        self.InsurerNumber = None     # 保険番号
        self.InsuredCardSymbol = None # 番号
        self.InsuredIdentificationNumber = None # 記号
        self.InsuredBranchNumber = None # 枝番

    def setData(self,InsurerNumber,InsuredCardSymbol,InsuredIdentificationNumber,InsuredBranchNumber=np.nan):

        self.InsurerNumber = InsurerNumber     # 保険番号
        self.InsuredIdentificationNumber = InsuredIdentificationNumber # 番号
        self.InsuredCardSymbol = InsuredCardSymbol # 記号
        self.InsuredBranchNumber = InsuredBranchNumber # 枝番
    
        dataObj = {"InsurerNumber": self.InsurerNumber, 
                    "InsuredCardSymbol": self.InsuredCardSymbol, 
                    "InsuredIdentificationNumber": self.InsuredIdentificationNumber,
                    "InsuredBranchNumber":self.InsuredBranchNumber}

        self.df_Hoken = pd.DataFrame(dataObj)


    def preparation(self):

        df = self.df_Hoken.copy()

        df['InsurerNumber'] = df['InsurerNumber'].fillna("").apply(str).apply(str.strip)
        df['InsuredCardSymbol'] = [unicodedata.normalize("NFKC",str(z)) for z in df['InsuredCardSymbol'].fillna("").apply(str)]        
        df['InsuredCardSymbol'] = [unicodedata.normalize("NFKC",str(z.strip(" "))) for z in df['InsuredCardSymbol'].fillna("").apply(str)]
        df['InsuredCardSymbol'] = df['InsuredCardSymbol'].apply(mojimoji.zen_to_han)
        df['InsuredCardSymbol'] = [ s.replace('\u2010','-') for s in df['InsuredCardSymbol'].tolist() ]
        df['InsuredCardSymbol'] = [ s.replace('\u2212','-') for s in df['InsuredCardSymbol'].tolist() ]
        df['InsuredIdentificationNumber'] = [unicodedata.normalize("NFKC",str(z)) for z in df['InsuredIdentificationNumber'].fillna("").apply(str)]


        self.df_Hoken = df.copy()

    def convertStr(self):

        df = self.df_Hoken.copy()

        df["InsurerNumber"] = df["InsurerNumber"].apply(lambda x: '"' + str(x) + '"')
        df["InsuredCardSymbol"] = df["InsuredCardSymbol"].apply(lambda x: '"' + str(x) + '"')
        df["InsuredIdentificationNumber"] = df["InsuredIdentificationNumber"].apply(lambda x: '"' + str(x) + '"')
        df["InsuredBranchNumber"] = df["InsuredBranchNumber"].apply(lambda x: '"' + str(x) + '"')
        
        self.df_Hoken = df.copy()


    def operation(self):
        self.preparation()
        #self.convertStr()


        df = self.df_Hoken.copy()
        return df


def main():




    obj = HokenKeyClass()

if __name__ == "__main__":
    main()

