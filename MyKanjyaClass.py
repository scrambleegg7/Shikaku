
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

class MyKanjyaClass(MyMasterClass):

    def __init__(self, data_dir=u"L:\\Miyuki", output_dir = u"L:\\epson_pxm840f\\Shikakku"):
        super().__init__(data_dir, output_dir)


        filename = "KANJA_List.txt"
        self.filename = os.path.join(self.data_dir, filename)

    def readCSV(self):

        df = super().readCSV(self.filename)
        df = df.iloc[:,1:7].copy()

        newcols = ["id","kaiin","Kana","Name","birth","sex2"]

        df.columns = newcols
        delcols = ["kaiin","Kana","Name","birth"]
        df.drop(delcols, inplace=True, axis=1)
        df.drop_duplicates(inplace=True)
        
        #print(df.shape)
        return df