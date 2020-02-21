#!/usr/bin/python3.6
from flask import Flask,g,render_template,redirect,url_for,jsonify,request  # !Important
from flask_oidc import OpenIDConnect
from okta import UsersClient


import os

import firebase_admin
from firebase_admin import *
from firebase_admin import firestore
import time
import sys
import math
from datetime import datetime

import database_extractor as de
app = Flask(__name__)

static_folder_path = "/home/zorroP/.virtualenvs/flask-introduction/library/static"
app.config["OIDC_CLIENT_SECRETS"] = "/home/zorroP/.virtualenvs/flask-introduction/library/static/client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"

oidc = OpenIDConnect(app)
okta_client = UsersClient("https://dev-283049.okta.com","00nGaldbmuaeAwci-mQCB-ovbWBTANUYe3bO4l2dWg")

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
        json_data={
        "type": "service_account",
        "project_id": "{{ }}",
        "private_key_id": "{{ }}",
        "private_key": "{{ }}",
        "client_email": "{{ }}",
        "client_id": "{{ }}",
        "auth_uri": "{{ }}",
        "token_uri": "{{ }}",
        "auth_provider_x509_cert_url": "{{ }}",
        "client_x509_cert_url": "{{ }}"
        }
        cred=credentials.Certificate(json_data)
        g.db=de.extractDatabase(cred)
    else:g.user = None

@app.route("/",endpoint="index")
def index():
    return render_template("index.html")

@app.route("/dashboard",endpoint="dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")

@app.route("/login",endpoint="login")
def login():
    return redirect(url_for(".dashboard"))

@app.route("/logout",endpoint="logout")
def logout():
    oidc.logout()
    #return 'Hi, you have been logged out! <a href="/">Return</a>'
    return redirect(url_for(".index"))


@app.route('/barcodes_template_data')
def barcodes_template_data():
    if(oidc.user_loggedin):
        barcodes_collection = g.db.collection('barcode_inventory')
        freq_dict=de.ExtractorOfBarcodesFreqDict(barcodes_collection)
        key_arr=list(freq_dict.keys())
        value_arr=list(freq_dict.values())

        return jsonify({
                'results':[key_arr,value_arr]#used in barcodes_template.html
            })
    else:return jsonify({
        'results':[[],[]]
        })

@app.route('/barcode',endpoint="take_barcodes")
def take_barcodes():
    if(oidc.user_loggedin):
    	barcodes_collection = g.db.collection('barcodes')
    	collections_list=de.ExtractorID(barcodes_collection)
    	new_list=[]
    	for [a,b] in collections_list:new_list.append(dict(ID=a, name=b))
    	return render_template('database/barcodes_template.html',authors=new_list)
    else:
        return(render_template("layout.html"))

@app.route('/users',endpoint="hello_world")
def hello_world():
    if(oidc.user_loggedin):
        users_collection = ref = g.db.collection('users')
        kiranaNamesSet2=de.ExtractorOfKiranaNamesAndCorrespondingPhones(ref)

        kirana_Barcode_Set={}
        barcodes_collection = g.db.collection('barcode_inventory')
        BarcodesSet=de.ExtractorOfBarcodes(barcodes_collection)

        UsersArray=de.ExtractorID(ref)

        totalBills,totalBarcodes,totalSpeechInventory=0,0,0
        newkiranaNamesSet2={}

        arrayOfNames=[]
        arrayOfBills=[]
        arrayOfSpeechItems=[]
        arrayOfBarcodeItems=[]

        for (k,phone_no) in kiranaNamesSet2:
            total1,totalBarcodes1,totalSpeechInventory1=0,0,0
            if k not in newkiranaNamesSet2:
                newkiranaNamesSet2[k]=[phone_no]#phone_no is  unique document id so not an issue of appending duplicate value
            else:
                newkiranaNamesSet2[k].append(phone_no)

            kirana_Barcode_Set[k]=set()
            for doc in UsersArray:

                if 'kiranaName' in doc[1]:
                    current_owner=doc[1]['kiranaName']
                    #current_owner=current_owner.replace(' ','')
                    #current_owner=current_owner.lower()
                if k==current_owner:
                    barcode_inventory_documents=g.db.collection(u'users').document(doc[0]).collection(u'barcode_inventory')
                    bills_documents=g.db.collection(u'users').document(doc[0]).collection(u'bills')
                    speech_inventory_documents=g.db.collection(u'users').document(doc[0]).collection(u'speech_inventory')

                    Barcodes_Subset=de.ExtractorOfBarcodes(barcode_inventory_documents)

                    barcode_inventory_collection=barcode_inventory_documents.get()
                    bills_collection=bills_documents.get()
                    speech_inventory_collection=speech_inventory_documents.get()

                    x=de.lengthOfCollection(barcode_inventory_collection)
                    y=de.lengthOfCollection(bills_collection)
                    z=de.lengthOfCollection(speech_inventory_collection)

                    totalBarcodes+=x
                    totalBills+=y
                    totalSpeechInventory+=z

                    totalBarcodes1+=x
                    total1+=y
                    totalSpeechInventory1+=z


                    if kirana_Barcode_Set[k]==set():
                        kirana_Barcode_Set[k]=Barcodes_Subset & BarcodesSet
                    else:
                        kirana_Barcode_Set[k]=kirana_Barcode_Set[k].union(Barcodes_Subset & BarcodesSet)
            arrayOfNames.append(k)
            arrayOfBills.append(total1)
            arrayOfBarcodeItems.append(totalBarcodes1)
            arrayOfSpeechItems.append(totalSpeechInventory1)

        new_list=[]
        for k in kirana_Barcode_Set.keys():
            for (a,b) in kirana_Barcode_Set[k]:
                new_list.append([k,a,b,newkiranaNamesSet2[k]])

        return render_template('database/template_engine_2.html',authors=new_list,totalBills=totalBills,totalBarcodes=totalBarcodes,totalSpeechInventory=totalSpeechInventory,a=arrayOfNames,b=arrayOfBills,c=arrayOfBarcodeItems,d=arrayOfSpeechItems)
    else:return(render_template("layout.html"))
    
class Posts(object):
    def __init__(self,barcodeName,barcodeNumber,date=datetime.now(),barcodePrice=0):
        self.barcodeName=barcodeName
        self.barcodeNumber=barcodeNumber
        self.barcodePrice=barcodePrice
        self.date=date
        
    @staticmethod
    def from_dict(source):
        post=Posts(source[u'barcodeName'],source[u'barcodeNumber'])
        if u'barcodePrice' in source:
            post.barcodePrice=source[u'barcodePrice']
        if u'date' in source:
            post.barcodePrice=source[u'date']
        return post

    def to_dict(self):
        dest={
            u'barcodeName':self.barcodeName,
            u'barcodeNumber':self.barcodeNumber
            }
        if self.barcodePrice:
            dest[u'barcodePrice']=self.barcodePrice
        if self.date:
            dest[u'date']=self.date
        return dest

    def __repr__(self):
        return(u'Posts(barcodeName={},barcodeNumber={},date={},barcodePrice={})'.format(
            self.barcodeName,self.barcodeNumber,self.date,self.barcodePrice))

def checkStringMadeOfInt(string):
    digits="0123456789"
    for s in string:
        if s not in digits:
            return False
    return True
         
@app.route("/edit/<string:phoneNumber>",methods=['GET','POST'])
def edit(phoneNumber):
    if(oidc.user_loggedin):
        if request.method=='POST':
            kiranaName=request.form.get('kiranaName')
            barcodeName=request.form.get('barcodeName')
            barcodeNumber=request.form.get('barcodeNumber')
            phone_no=request.form.get('phone_no')
            date=datetime.now()
            if phoneNumber=='0':
                #add data to database
                data1={
                    u'kiranaName':kiranaName,
                    u'phoneNumber':phone_no
                    }
        
                #data2={u'barcodeName':barcode_name,u'barcodeNumber':barcode_no,u'date':date}
                #data2=Posts(barcodeName,barcodeNumber,date).to_dict()
                g.db.collection('users').document(phone_no).set(data1)
                #db.collection('users').document(phoneno).collection('barcode_inventory').document(barcode_no).set(data2)
                g.db.collection('users').document(phone_no).collection('barcode_inventory').document(barcodeNumber).set(Posts(barcodeName,barcodeNumber,date).to_dict())

    
        barcodeName,barcodeNumber,kiranaName='','',''
        docs=g.db.collection('users').where(u'phoneNumber',u'==',phoneNumber).stream()
        for i,doc in enumerate(docs):
            if i>0:break
            else:
                #phoneNumber=doc.id
                mydict1=doc.to_dict()
                kiranaName=mydict1['kiranaName']
                barcodeNoDocs=g.db.collection(u'users').document(phoneNumber).collection(u'barcode_inventory').get()
                for j,barcodeNoDoc in enumerate(barcodeNoDocs):
                    if j>0:break
                    else:
                        mydict2=barcodeNoDoc.to_dict()
                        barcodeName=mydict2['barcodeName']
                        barcodeNumber=mydict2['barcodeNumber']
        post=Posts(barcodeName,barcodeNumber).to_dict()                
        post[u'kiranaName']=kiranaName
        post[u'phoneNumber']=phoneNumber
        #db.collection(u'users').document(phoneNumber).collection(u'barcode_inventory').document(barcodeNumber).update(post)
        
        return render_template('edit.html',post=post,phoneNumber=phoneNumber)
    else:return(render_template("layout.html"))


@app.route("/delete/<string:phoneNumber>/<string:barcodeNumber>",methods=['GET','POST'])
def delete(phoneNumber,barcodeNumber):
    if(oidc.user_loggedin):
        doc=g.db.collection(u'users').document(phoneNumber).collection(u'barcode_inventory').document(barcodeNumber)
        doc.delete()
        return redirect(url_for(".dashboard"))
    else:return(render_template("layout.html"))

@app.route("/read/<string:phoneNumber>")
def read(phoneNumber):
    if(oidc.user_loggedin):
        ref=g.db.collection(u'users').document(phoneNumber).collection(u'barcode_inventory')
        barcodesArray=de.ExtractorID(ref)
        return render_template("read.html",authors=barcodesArray)
    else:return(render_template("layout.html"))

@app.route("/add/<string:barcodeNumber>/<string:barcodeName>")
def add(barcodeNumber,barcodeName):
    if(oidc.user_loggedin):
        checks=checkStringMadeOfInt(barcodeNumber)
        msg="Barcode Number"
        if not checks:
            flash(msg+" should be integer","alert alert-danger")
        else:
            g.db.collection(u'barcode_inventory').document(barcodeNumber).set({'barcodeNumber':barcodeNumber,'barcodeName':barcodeName})
            flash("Congratulations data has been added to barcode inventory","alert alert-success")
        return redirect(url_for(".dashboard"))
    else:return(render_template("layout.html"))

@app.errorhandler(404)
def not_found(error):
    if(oidc.user_loggedin):
        return (render_template('routing/404.html'),404)
    else:return(render_template("layout.html"))
