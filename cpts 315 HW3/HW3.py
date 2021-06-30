## Name:Hongqi Guo
## Student ID:011552159
## This program is not complete.

import numpy as np
iterations = 20

def get_stoplist():
    stoplist = set()
    stoplis = open("stoplist.txt",'r')
    for key in stoplis:
        value = (key.strip())
        stoplist.add(value)
    return stoplist,stoplis
def get_traindata(stoplist):
    number = 0
    traindata = set()
    traindat = open("traindata.txt","r")
    for key in traindat:
        for value in key.split():
            if value in stoplist:
                if value in traindata:
                    continue
                else:
                    traindata.add(value)
                    number += 1
    weight = np.zeros(number,np.int)
    return weight,traindat,traindata

def get_trainlabels():
    trainlabels = open("trainlabels.txt","r")
    return trainlabels
def get_testdata():
    testdata = open("testdata.txt","r")
    return testdata
def get_testlabers():
    testlabels = open("testlabels.txt","r")
    return testlabels

def zip_trdata_trlabels(traindata,traindat,trainlabels):
    trdata = list()
    trlabel = list()
    trgetdata = sorted(traindata)
    zip_data = zip(str(traindat),str(trainlabels))
    for k_data,k_label in zip_data:
        trtemp = list()
        for key in trgetdata:
            if key in k_data.split():
                trtemp.append(1)
            else:
                trtemp.append(0)
    trdata.append(trtemp)
    trlabel.append(k_label.strip())
    return trdata,trlabel

def zip_tedata_telabels(traindata,testdata,testlabels):
    tedata = list()
    telabel = list()
    trgetdata = sorted(traindata)
    zip_data = zip(str(testdata),str(testlabels))
    for k_data,k_label in zip_data:
        tetemp = list()
        for key in trgetdata:
            if key in k_data.split():
                tetemp.append(1)
            else:
                tetemp.append(0)
    tedata.append(tetemp)
    telabel.append(k_label.strip())
    return tedata,telabel




def main():
    f = open("output.txt","w")
    
    f.close()
if __name__ == "__main__":
    main()







