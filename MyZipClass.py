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

from MyMasterClass import MyMasterClass
from HOKENKeyClass import HokenKeyClass

sns.set()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

#import japanize_matplotlib
import unicodedata
import mojimoji

class MyZipClass(MyMasterClass):

    def __init__(self):

        self.data_dir = u"S:\\"
        self.output_dir = u"L:\\epson_pxm840f\\Shikakku"

        self.shikaku_tag = {}        
        self.shikaku = []

        self.zipShikaku = u"資格確認履歴*.zip"
        self.zipShikaku = os.path.join(self.data_dir, self.zipShikaku)

        # 保険番号convert Class
        self.HOKENKeyObject = HokenKeyClass()

    def readZipFile(self):
        
        zfile =  self.readFileDirectory()
        
        with zipfile.ZipFile(zfile) as thezip:

            print(thezip.namelist() )
            
            # change filename with cp932 for Japanese language
            for info in thezip.infolist():
                info.filename = info.orig_filename.encode('cp437').decode('cp932')
                #info.filename = os.path.join(self.output_dir, info.filename)
            
            os.chdir(self.output_dir)
            print("change current directory --> %s" % os.getcwd())

            thezip.extract(info)

            #with thezip.open(origfile,mode='r') as thefile:
            #Let us verify the operation..
            unzipfilename = os.path.join(self.output_dir, info.filename)

            read_data_types = {"被保険者証記号":str, "保険者番号":str , "被保険者証番号":str, "被保険者証枝番":str }

            df = pd.read_csv(unzipfilename, dtype=read_data_types)
            df.dropna(subset=["保険者番号"],    inplace=True)

            #print(df.columns)
            #print(df.head(3))

            delcols = [u"処理実行日時",u"利用者コード",u"医療機関コード",u'限度額適用認定証長期入院該当年月日',u'特定疾病表示同意フラグ',u'特定疾病療養受療証認定疾病区分１', \
                    u'特定疾病療養受療証交付年月日１', u'特定疾病療養受療証有効開始年月日１', u'特定疾病療養受療証有効終了年月日１', \
                    u'特定疾病療養受療証自己負担限度額１', u'特定疾病療養受療証認定疾病区分２', u'特定疾病療養受療証交付年月日２', \
                    u'特定疾病療養受療証有効開始年月日２', u'特定疾病療養受療証有効終了年月日２', u'特定疾病療養受療証自己負担限度額２', \
                    u'特定疾病療養受療証認定疾病区分３', u'特定疾病療養受療証交付年月日３', u'特定疾病療養受療証有効開始年月日３', \
                    u'特定疾病療養受療証有効終了年月日３', u'特定疾病療養受療証自己負担限度額３', u'照会番号', u'特健閲覧同意フラグ', \
                    u'薬剤閲覧同意フラグ', '照会時入力項目',u'氏名（その他）',u'氏名カナ', u'性別2',u'被保険者氏名(世帯主氏名','未就学区分' ]

            df.drop(delcols, inplace=True, axis=1)
            df.drop_duplicates(inplace=True, subset=["氏名"])

            print("## delte unzipped shikaku file...", unzipfilename)
            os.remove(unzipfilename)

            cols = ["conf_date","segment","facial","validation","InsurerNumber","InsurerName",
                            "InsuredCardSymbol","InsuredIdentificationNumber","InsuredBranchNumber",
                            "hoken_segment","yours","Name",
                    "NameKana","sex1","birth","Address","PostNumber","hoken_issue_date","hoken_validation_date","hoken_end_date","ratio",
                    "invalid_data","korei_issue","korei_start","korei_end","korei_ratio","gendo_kubun","limit_certification","limit_segment", 
                    "limit_issue","limit_start","limit_end"]

            df.columns = cols

            self.HOKENKeyObject.setData(
                        df["InsurerNumber"],
                        df["InsuredCardSymbol"],
                        df["InsuredIdentificationNumber"],
                        df["InsuredBranchNumber"]
            )
            df_HOKEN = self.HOKENKeyObject.operation()

            df["InsurerNumber"] = df_HOKEN["InsurerNumber"]
            df["InsuredCardSymbol"] = df_HOKEN["InsuredCardSymbol"]
            df["InsuredIdentificationNumber"] = df_HOKEN["InsuredIdentificationNumber"]
            df["InsuredBranchNumber"] = df_HOKEN["InsuredBranchNumber"]
            
            df.fillna("", inplace=True)
            df.reset_index(inplace=True,drop=True)

            
            return df

    def readFileDirectory(self):

        self.targets = sorted( glob(self.zipShikaku), reverse=True)


        if self.targets:
            for f in self.targets:
                return f
        else:
            raise("Error %s not found" % self.zipShikaku)
            




def main():

    zipObject = MyZipClass()
    df = zipObject.readZipFile()

    selectObj = ["InsurerNumber","InsuredCardSymbol","InsuredIdentificationNumber","InsuredBranchNumber"]
    df = df[selectObj].copy()

    print(df.head(3))
    print(df.tail(3))

    zipObject.toCsv(df,"test.csv")

if __name__ == "__main__":
    main()