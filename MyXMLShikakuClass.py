import xml.etree.ElementTree as ET
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
from scipy.stats import pearsonr
from sklearn import preprocessing


import seaborn as sns
sns.set()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

#import japanize_matplotlib
from MyMasterClass import MyMasterClass

class MyXMLShikakuClass(MyMasterClass):

    def __init__(self):

        self.data_dir = "S:\\"
        self.output_dir = "L:\\epson_pxm840f\\Shikakku"

        self.shikaku_tag = {}        
        self.shikaku = []

        self.readFileDirectory()


        self.taglist = []

        self.dictList = []
        

    def readFileDirectory(self):

        files = os.listdir(self.data_dir)
        self.files = [f for f in files if f.endswith(".xml")]
        #print(self.files)
        #return files

    def reader(self,f):

        tree = ET.parse(f)
        root = tree.getroot()
        self.tagDict = {}
        for child in root.iter("ResultOfQualificationConfirmation"):
            for c in child:
                self.taglist.append(c.tag) 

                try:
                    self.tagDict[c.tag] = c.text
                    #print(c.text)
                except:
                    print("key error : tag dictionary")
                    
                if c.tag == "LimitApplicationCertificateRelatedInfo":
                    #print("限度額適用")

                    limitchild = c
                    for lm in limitchild:
                        #print(lm.tag, lm.text)
                        self.taglist.append(lm.tag) 
        self.dictList.append(self.tagDict)
            
    
    def getDataFrame(self):

        for f in self.files:
            f = os.path.join(self.data_dir,f)
            self.reader(f)
        
        uniq_tagList = list(set( self.taglist ) )
        self.dataList = []
        for dataItemDict in self.dictList:

            keys = dataItemDict.keys()
            unlistdkeys = (uniq_tagList - keys)

            #print("occurrences of unlisted keys : %d" % len(unlistdkeys) )
            #print(unlistdkeys)
            for ul in unlistdkeys:
                dataItemDict[ul] = ""
            self.dataList.append( dataItemDict )
        
        # tranparent into pandas dataframe
        self.df = pd.DataFrame(self.dataList)

        self.df["birth"] = pd.to_datetime(self.df.Birthdate)


        return self.df


def main():

    xmlObject = MyXMLShikakuClass()
    df = xmlObject.getDataFrame()
    xmlObject.toCsv(df,"XMLShikaku.csv")

if __name__ == "__main__":
    main()