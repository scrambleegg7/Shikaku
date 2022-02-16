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


class MyShikakuXMLStruct(object):

    def __init__(self):

        self.data_dir = "S:\\"
        self.output_dir = "L:\\epson_pxm840f\\Shikakku"

        self.shikaku_tag = {}        
        self.shikaku = []

    def readFileDirectory(self):

        files = os.listdir(self.data_dir)
        self.files = [f for f in files if f.endswith(".xml")]
        print(self.files)
        #return files


    def readXML(self,f):



        tree = ET.parse(f)
        root = tree.getroot()

        for child in root.iter("ResultOfQualificationConfirmation"):
            patient = []
            for c in child:
                print(c.tag)
                #print(c.text)
                patient.append(c.text)

                if c.tag == "LimitApplicationCertificateRelatedInfo":
                    print("限度額適用")

                    limitchild = c
                    for lm in limitchild:
                        print(lm.tag, lm.text)
            
            self.shikaku.append(patient)

    def operation(self):

        self.readFileDirectory()
        for f in self.files:
            f = os.path.join(self.data_dir,f)
            self.readXML(f)


        #columns = ["InsuredCardClassification","InsurerNumber","InsuredIdentificationNumber" \ 
        #            ,"Name","NameKana","Sex1","Birthdate","Address","PostNumber" \    
        #            ,"InsuredCertificateIssuanceDate","InsuredCardValidDate" \ 
        #            ,"InsuredPartialContributionRatio","InsurerName","LimitApplicationCertificateRelatedConsFlg"]
        df = pd.DataFrame(self.shikaku)  #, columns=columns)

        print(df.head(3))
        print(df.tail(3))

        shikakufile = os.path.join(self.output_dir,"shikaku.csv")

        df.to_csv(shikakufile,index=False, encoding='cp932')
        


def main():

    xmlObject = MyShikakuXMLStruct()
    xmlObject.operation()

if __name__ == "__main__":
    main()