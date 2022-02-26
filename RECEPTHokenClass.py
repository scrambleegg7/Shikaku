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
from HOKENKeyClass import HokenKeyClass


class RECEPTHokenClass(MyMasterClass):

    def __init__(self, data_dir=u"L:\\RECEPTY\\national",  output_dir = u"L:\\epson_pxm840f\\Shikakku"):
        super().__init__(data_dir, output_dir)


        filename = "RECEIPTY.CYO"
        self.nfilename = os.path.join(self.data_dir, filename)
        
        data_dir2=u"L:\\RECEPTY\\tokyo"
        self.tfilename = os.path.join(data_dir2, filename)

        # 保険番号convert Class
        self.HOKENKeyObject = HokenKeyClass()


    def readData(self,filename):

        with codecs.open(filename, "r", "Shift-JIS", "ignore") as file:
            col_names = [ 'c{0:02d}'.format(i) for i in range(180) ]

            read_data_types = { "c01":str, "c02":str , "c03":str }

            df_re = pd.read_csv(file, delimiter=",", names=col_names, engine="python", dtype=read_data_types )
            #print(df_re.head())
            print("[ReceiptyClass] recepty csv data file size --> ",df_re.shape)

            return df_re
    
    def integrateInsurancedata(self):

        df_n = self.readData(self.nfilename)
        df_nat = self.makeInsurancedata(df_n)

        df_t = self.readData(self.tfilename)
        df_tok = self.makeInsurancedata(df_t)

        return pd.concat([df_nat,df_tok]).reset_index(drop=True)

    def makeKouhiData(self,df_RE):
    
        df_RE_index = df_RE[df_RE.c00 == "RE"].index.tolist() 
        kotargetcols = ["c01","c02","c03","c07","c09"]
        _ko = df_RE[df_RE.c00 == "KO"][kotargetcols] # .reset_index(drop=True)

        data1 = {"c01":np.nan,"c02":np.nan,"c03":np.nan,"c07":np.nan,"c09":np.nan }
        data2 = {"c01x":np.nan,"c02x":np.nan,"c03x":np.nan,"c07x":np.nan,"c09x":np.nan}

        # Kouhi loop (1)(2)
        ko_list1 = []
        ko_list2 = []

        for idx, re_idx in enumerate(df_RE_index[:-1]):
            
            ko_idx_list = []
            
            tmp_re_idx = None
            tmp_ko_idx = None

            ko_idx_list2 = []
            for ko_idx in _ko.index.tolist():
                
                if ko_idx > re_idx and ko_idx <= df_RE_index[idx+1]:
                    try:
                        tmp_re_idx = re_idx
                        tmp_ko_idx = ko_idx
                        
                        data1 = {"re_idx":re_idx, "c01":_ko.c01,"c02":_ko.c02,"c03":_ko.c03,"c07":_ko.c07,"c09":_ko.c09 }
                        ko_idx_list.append(pd.DataFrame(data1, index=[tmp_ko_idx]) )

                    except:
                        print("Error : re idx %d ko_idx %d" % ( re_idx, ko_idx ))
                
            if len(ko_idx_list) == 1: # case 2nd kouhi not found dummy record added
                _tmp_df=pd.DataFrame(data2, index=[tmp_ko_idx])
                ko_idx_list2.append(ko_idx_list[0])
                ko_idx_list2.append( _tmp_df )
            
                _tmp = pd.concat( ko_idx_list2,axis=1)
                #_tmp.index = tmp_re_idx

                #print(_tmp)

                ko_list1.append(_tmp)

            if len(ko_idx_list) == 2: # case 2nd kouhi found 
                #print(ko_idx_list)
                #print(df_RE.loc[re_idx])
                ko_list2.append(ko_idx_list)

        # build kouhi x 1        
        kouhi_columns = ["RE_index1", "kouhi1","kouhi_jyu1","kyufu_kubu1","futan1","kouhifutan1",
                            "kouhi2","kouhi_jyu2","kyufu_kubu2","futan2","kouhifutan2" ]     
        df_kouhilist1 = pd.concat( ko_list1, axis=0).fillna("")   
        df_kouhilist1.columns = kouhi_columns

        # build kouhi x 2 (multiple kouhi)
        _tmp_list = []
        for _klist in ko_list2:
            np_list = pd.concat( _klist ).to_numpy()
            np_list = np_list.reshape(  np_list.shape[0] * np_list.shape[1])
            df_kouhilist = pd.DataFrame(np_list   ).T.fillna("")
            df_kouhilist.index = _klist[0].index

            _tmp_list.append(df_kouhilist)

        kouhi_columns2 = ["RE_index1", "kouhi1","kouhi_jyu1","kyufu_kubu1","futan1","kouhifutan1",
                        "RE_index2", "kouhi2","kouhi_jyu2","kyufu_kubu2","futan2","kouhifutan2" ]    

        if len(_tmp_list) > 0:
            df_kouhilist2 = pd.concat( _tmp_list, axis=0 )
            df_kouhilist2.columns = kouhi_columns2

            df_kouhi_final = pd.concat( [df_kouhilist1, df_kouhilist2], axis = 0 )
            df_kouhi_final.index = df_kouhi_final.RE_index1
            df_kouhi_final.drop(["RE_index1","RE_index2"], inplace=True, axis=1)

        else:
            df_kouhi_final = df_kouhilist1.copy()
            df_kouhi_final.index = df_kouhi_final.RE_index1
            df_kouhi_final.drop(["RE_index1"], inplace=True, axis=1)
            
        #print(df_kouhi_final.head(3))

        return df_kouhi_final

        
    def makeInsurancedata(self, df_RE):

        df_RE_index = df_RE[df_RE.c00 == "RE"].index.tolist() 

        retargetcols = ["c04","c05","c06","c07","c08"]
        hotargetcols = ["c01","c02","c03","c09"]
        kotargetcols = ["c01","c02","c03","c07","c09"]

        _re = df_RE[df_RE.c00 == "RE"][retargetcols] # .reset_index(drop=True)  
        _ho = df_RE[df_RE.c00 == "HO"][hotargetcols] #.reset_index(drop=True)

        _ho.index = _ho.index - 1

        df_ko_2 = self.makeKouhiData(df_RE)

        _df2 = pd.concat( [_re,_ho], axis=1)
        df = pd.merge(_df2, df_ko_2, how="left", left_index=True, right_index=True)

        df.columns = ["Name","sex","birth","ratio","SpecialPurpose","InsurerNumber", 
                        "InsuredCardSymbol","InsuredIdentificationNumber", "InsuredFutan", 
                        "kouhi1","kouhi_jyu1","kyufu_kubu1","futan1","kouhifutan1",
                        "kouhi2","kouhi_jyu2","kyufu_kubu2","futan2","kouhifutan2" ]     


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

        df['sex'] = [ s.replace('2','女') for s in df['sex'].tolist() ]
        df['sex'] = [ s.replace('1','男') for s in df['sex'].tolist() ]
        df['birth'] = df['birth'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

        # 12 and 15 excluded from outputlist
        df = df[ ((df.kouhi1.str[:2] != "12") & (df.kouhi1.str[:2] != "15")) ].copy()        

        return df.fillna("")
    
def main():

    nkObject = RECEPTHokenClass()
    df = nkObject.integrateInsurancedata()

    selectObj = ["InsurerNumber","InsuredCardSymbol","InsuredIdentificationNumber"]
    df = df[selectObj].copy()

    print(df.head(3))
    print(df.tail(3))
    nkObject.toCsv(df,"test.csv")



if __name__ == "__main__":
    main()