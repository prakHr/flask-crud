import firebase_admin
from firebase_admin import *
from firebase_admin import firestore
import time
import sys

#function takes the credentials(=>input) and gives reference address to database(=>db)
def extractDatabase(cred):
    app=firebase_admin.initialize_app(cred)
    db=firestore.client()
    delete_app(app)#instance of app is deleted to reuse again
    return db

#function saves id and data-fields into array from reference node of the tree in firestore and return that array
def ExtractorID(reference):
    docs=reference.get()
    array=[]
    #print(docs)
    for doc in docs:
        array.append([doc.id,doc.to_dict()])
       #print(doc)
    return array


#function takes reference of barcodes collection as input and returns freqDict(barcodeName,barcodeNumber)
def ExtractorOfBarcodesFreqDict(reference):
    docs=reference.get()
    freq_dict={}
    for doc in docs:
        mydict=doc.to_dict()
        if 'barcodeName' in mydict:
            newstring=mydict['barcodeName'].replace(' ','')
            newstring=newstring.lower()
            if newstring=='':
                continue
            key=newstring
            freq_dict[key]=freq_dict.get(key,0)+1
    return freq_dict

#function takes reference of barcodes collection as input and returns tuple(barcodeName,barcodeNumber)
def ExtractorOfBarcodes(reference):
    docs=reference.get()
    Set=set()
    for doc in docs:
        mydict=doc.to_dict()
        if 'barcodeName' in mydict:
            newstring=mydict['barcodeName'].replace(' ','')
            newstring=newstring.lower()
            if newstring=='':
                continue
            Set.add((newstring,doc.id))
    return Set

#function takes reference of users collection as input and returns Set(kiranaOwnerName)
def ExtractorOfKiranaNames(reference):
    docs=reference.get()
    Set=set()
    for doc in docs:
        mydict=doc.to_dict()
        if 'kiranaName' in mydict:
            newstring=mydict['kiranaName']
            #newstring=newstring.replace(' ','')
            #newstring=newstring.lower()
            if newstring=='':
                continue
            Set.add(newstring)
    return Set

#function takes reference of users collection as input and returns tuple(kiranaOwnerName,phoneNo)
def ExtractorOfKiranaNamesAndCorrespondingPhones(reference):
    docs=reference.get()
    Set=set()

    for doc in docs:
        mydict=doc.to_dict()
        if 'kiranaName' in mydict:
             newstring=mydict['kiranaName']
            #newstring=newstring.replace(' ','')
            #newstring=newstring.lower()
            if newstring=='':
                continue
            Set.add((newstring,doc.id))  
    return Set

def lengthOfCollection(collection):
    length=0
    for docs in collection:
        length+=1
    return length


