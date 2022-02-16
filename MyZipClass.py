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

class MyZipClass(object):

    def __init__(self):

        self.data_dir = u"S:\\"
        self.output_dir = u"L:\\epson_pxm840f\\Shikakku"

        self.shikaku_tag = {}        
        self.shikaku = []

        self.zipShikaku = u"資格確認履歴*.zip"
        self.zipShikaku = os.path.join(self.data_dir, self.zipShikaku)

    def toCsv(self,df):

        filename = os.path.join(self.output_dir,"資格確認_保険証.csv")
        df.to_csv(filename, index=False, encoding='cp932', errors='replace')

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
            df = pd.read_csv(unzipfilename)
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

            df['被保険者証記号'] = [unicodedata.normalize("NFKC",str(z.strip(" "))) for z in df['被保険者証記号'].fillna("").apply(str)]
            df['被保険者証記号'] = df['被保険者証記号'].apply(mojimoji.zen_to_han)
            #df['被保険者証記号'].replace(['‐'], '-', inplace=True)
            df['被保険者証記号'] = [ s.replace('\u2010','-') for s in df['被保険者証記号'].tolist() ]

            #print("after vanishing unicode escape..........")
            #print(df['被保険者証記号'].tolist())
            

            print("## delte unzipped shikaku file...", unzipfilename)
            os.remove(unzipfilename)

            cols = ["conf_date","segment","facial","validation","hoken","hoken_name","kigo","bango","eda","hoken_segment","yours","name",
            "kana","sex1","birth","address","postal","hoken_issue_date","hoken_validation_date","hoken_end_date","ratio",
            "invalid_data","korei_issue","korei_start","korei_end","korei_ratio","gendo_kubun","limit_certification","limit_segment", 
            "limit_issue","limit_start","limit_end"]

            df.columns = cols
            df['hoken'] = df['hoken'].fillna(0).apply(int).apply(str).replace(['0'],' ')
            #df['kigo'] = [unicodedata.normalize("NFKC",str(z)) for z in df['kigo'].fillna("").apply(str)]
            # special purpose to change hyfun chord of Japanese
            #df['kigo'] = [ s.replace('\u2010','-') for s in df['kigo'].tolist() ]
            df['bango'] = [unicodedata.normalize("NFKC",str(z)) for z in df['bango'].fillna("").apply(str)]

            df.reset_index(inplace=True,drop=True)

            print(df.dtypes)

            return df

    def readFileDirectory(self):

        self.targets = glob(self.zipShikaku)

        if self.targets:
            for f in self.targets:
                return f
        else:
            exit




def main():

    zipObject = MyZipClass()
    df = zipObject.readZipFile()
    zipObject.dftoCsv(df)

if __name__ == "__main__":
    main()