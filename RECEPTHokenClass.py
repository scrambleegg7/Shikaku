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


from MyMasterClass import MyMasterClass

class RECEPTClass(MyMasterClass):

    def __init__(self, data_dir=u"L:\\RECEPTY\\national", output_dir = u"L:\\epson_pxm840f\\Shikakku"):
        super().__init__(data_dir, output_dir)


        filename = "RECEIPTY.CYO"
        self.filename = os.path.join(self.data_dir, filename)

    def readData(self):

        with codecs.open(self.filename, "r", "Shift-JIS", "ignore") as file:
            col_names = [ 'c{0:02d}'.format(i) for i in range(180) ]

            df_re = pd.read_csv(file, delimiter=",", names=col_names, engine="python" )
            #print(df_re.head())
            print("[ReceiptyClass] recepty csv data file size --> ",df_re.shape)

            return df_re
    
    def makeInsurancedata(self):
        df_RE = self.readData()
        df_RE_index = df_RE[df_RE.c00 == "RE"].index.tolist() 

        retargetcols = ["c04","c05","c06","c07","c08"]
        hotargetcols = ["c01","c02","c03","c09"]
        kotargetcols = ["c01","c02","c03","c07","c09"]

        _re = df_RE[df_RE.c00 == "RE"][retargetcols].reset_index(drop=True)  
        _ho = df_RE[df_RE.c00 == "HO"][hotargetcols].reset_index(drop=True)
        _ko = df_RE[df_RE.c00 == "KO"][kotargetcols]# .reset_index(drop=True)

        df_list = []
        data1 = {"c01":np.nan,"c02":np.nan,"c03":np.nan,"c07":np.nan,"c09":np.nan }
        data2 = {"c01x":np.nan,"c02x":np.nan,"c03x":np.nan,"c07x":np.nan,"c09x":np.nan}

        # Kouhi loop (1)(2)
        ko_list1 = []
        ko_list2 = []

        for idx, re_idx in enumerate(df_RE_index[:-1]):
            
            ko_idx_list = []
            tmp_ko_idx = None
            for ko_idx in _ko.index.tolist():
                
                if ko_idx > re_idx and ko_idx <= df_RE_index[idx+1]:
                    try:
                        tmp_ko_idx = ko_idx
                        data1 = {"c01":_ko.c01,"c02":_ko.c02,"c03":_ko.c03,"c07":_ko.c03,"c09":_ko.c09 }
                        ko_idx_list.append(pd.DataFrame(data1, index=[ko_idx]) )
                    except:
                        print("Error : re idx %d ko_idx %d" % ( re_idx, ko_idx ))
                
            if len(ko_idx_list) == 1: # case 2nd kouhi not found dummy record added
                _tmp_df=pd.DataFrame(data2, index=[tmp_ko_idx])
                ko_idx_list.append( _tmp_df )
            
                _tmp = pd.concat( ko_idx_list,axis=1)
                #print(_tmp)

                ko_list1.append(_tmp)


        _df_ko_2 = pd.concat(ko_list1)    
        _df2 = pd.concat( [_re,_ho], axis=1)
        _df = pd.merge(_df2, _df_ko_2, how="left", left_index=True, right_index=True)

        _df.columns = ["Name","sex","birth","ratio","SpecialPurpose","InsurerNumber", 
                        "InsuredCardSymbol","InsuredIdentificationNumber", "InsuredFutan", 
                        "kouhi1","kouhi_jyu1","kyufu_kubu1","futan1","kouhifutan1",
                        "kouhi2","kouhi_jyu2","kyufu_kubu2","futan2","kouhifutan2" ]     

        _df['InsuredCardSymbol'] = [unicodedata.normalize("NFKC",str(z)) for z in _df['InsuredCardSymbol'].fillna("").apply(str)]
        _df['InsuredCardSymbol'] = [ s.replace('\u2010','-') for s in _df['InsuredCardSymbol'].tolist() ]
        _df['InsuredCardSymbol'] = [ s.replace('\u2212','-') for s in _df['InsuredCardSymbol'].tolist() ]
        _df['sex'] = [ s.replace('2',u'女') for s in _df['sex'].tolist() ]
        _df['sex'] = [ s.replace('1',u'男') for s in _df['sex'].tolist() ]
        _df['birth'] = _df['birth'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

        
        _df['InsuredIdentificationNumber'] = [unicodedata.normalize("NFKC",str(z)) for z in _df['InsuredIdentificationNumber'].fillna("").apply(str)]

        return _df.fillna("")