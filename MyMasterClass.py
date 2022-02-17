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

class MyMasterClass(object):

    def __init__(self,data_dir=u"S:\\", output_dir = u"L:\\epson_pxm840f\\Shikakku"):

        self.data_dir = data_dir
        self.output_dir = output_dir

    def toCsv(self, df, filename, sw="J"):
        if sw == "J":
            self.toCsvCP932(df, filename)
        else:
            raise("[MyMasterClass] Error toCsv : need to sw parameter.")

    def toCsvCP932(self, df, filename):

        filename = os.path.join(self.output_dir,filename)
        df.to_csv(filename, index=False, encoding='cp932', errors='replace')

        
