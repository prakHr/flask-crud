from flask import Flask,g,render_template,redirect,url_for,jsonify  # !Important
from flask_oidc import OpenIDConnect
from okta import UsersClient

from flask_caching import Cache

import os

import firebase_admin
from firebase_admin import *
from firebase_admin import firestore
import time
import sys

import database_extractor as de
#from random import sample
config1={
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 50
}
app = Flask(__name__)

app.config.from_mapping(config1)
cache=Cache(app)

#app._static_folder = os.path.abspath("templates/static/")
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
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
        #cred=credentials.Certificate("project1-a9674-firebase-adminsdk-ddztm-263a615578.json")
        g.db=de.extractDatabase(cred)
    else:g.user = None
    
@app.route("/",endpoint="index")
def index():
    return render_template("index.html")

# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     # string="no-cache, no-store, must-revalidate"
#     # pre_check_string="no-cache, no-store, must-revalidate, pre-check=0"
#     # post_check_string="no-cache, no-store, must-revalidate, post-check=0"
#     # pre_post_check_string="no-cache, no-store, must-revalidate, pre-check=0, post-check=0"
#     # r.headers["Cache-Control"] = string
#     # r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

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
 

@app.route('/data')
@cache.cached(timeout=50)
def data():
    if(oidc.user_loggedin):

        users_collection = ref = g.db.collection('users')
        UsersArray=de.ExtractorID(ref)
        kiranaNamesSet=de.ExtractorOfKiranaNames(ref)
        arrayOfNames=[]
        arrayOfBills=[]
        arrayOfSpeechItems=[]
        arrayOfBarcodeItems=[]
        kirana_Barcode_Set={}

        for k in kiranaNamesSet:
            total,totalBarcodes,totalSpeechInventory=0,0,0
        
            for doc in UsersArray:
                barcode_inventory_documents=g.db.collection(u'users').document(doc[0]).collection(u'barcode_inventory')
                bills_documents=g.db.collection(u'users').document(doc[0]).collection(u'bills')
                speech_inventory_documents=g.db.collection(u'users').document(doc[0]).collection(u'speech_inventory')     

                barcode_inventory_collection=barcode_inventory_documents.get()
                bills_collection=bills_documents.get()
                speech_inventory_collection=speech_inventory_documents.get()
                
                barcodes=de.lengthOfCollection(barcode_inventory_collection)
                bills=de.lengthOfCollection(bills_collection)
                speechItems=de.lengthOfCollection(speech_inventory_collection)

                if 'kiranaName' in doc[1]:
                    current_owner=doc[1]['kiranaName']
                    current_owner=current_owner.replace(' ','')
                    current_owner=current_owner.lower()
                if k==current_owner:
                    totalBarcodes+=barcodes
                    total+=bills
                    totalSpeechInventory+=speechItems
                    
            arrayOfNames.append(k)
            arrayOfBills.append(total)
            arrayOfBarcodeItems.append(totalBarcodes)
            arrayOfSpeechItems.append(totalSpeechInventory)

        return jsonify({
                'array_NBBS':[arrayOfNames,arrayOfBills,arrayOfBarcodeItems,arrayOfSpeechItems]#used in template_engine_1.html
                

            }) 
    else:return jsonify({
        'array_NBBS':[[],[],[],[]]
        })

@app.route('/barcodes_template_data')
@cache.cached(timeout=50)
def barcodes_template_data():
    if(oidc.user_loggedin):
        barcodes_collection = g.db.collection('barcode_inventory')
        #barcodes_collection = g.db.collection('barcodes')
        #BarcodesArray=de.ExtractorID(barcodes_collection)
        #return jsonify({'results':sample(range(1,10),5)}) 
        #freq_dict={}
        #for [a,b] in BarcodesArray:
        #    if 'barcodeName' in b:
        #        key=b['barcodeName']
        #        freq_dict[key]=freq_dict.get(key,0)+1
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
@cache.cached(timeout=50)
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
@cache.cached(timeout=50)
def hello_world():
    if(oidc.user_loggedin):
        #users_collection= ref =g.db.collection('users')
        #kiranaNamesSet2=de.ExtractorOfKiranaNamesAndCorrespondingPhones(ref)
        #new_list=[]
        #for (a,b) in kiranaNamesSet2:
        #    new_list.append(dict(ID=a,name=b))
        barcodes_collection = g.db.collection('barcode_inventory')
        BarcodesSet=de.ExtractorOfBarcodes(barcodes_collection)

        users_collection = ref = g.db.collection('users')
        UsersArray=de.ExtractorID(ref)
        kiranaNamesSet=de.ExtractorOfKiranaNames(ref)
        kirana_Barcode_Set={}

        totalBills,totalBarcodes,totalSpeechInventory=0,0,0
        for k in kiranaNamesSet:
            kirana_Barcode_Set[k]=set()
            for doc in UsersArray:
                barcode_inventory_documents=g.db.collection(u'users').document(doc[0]).collection(u'barcode_inventory')
                bills_documents=g.db.collection(u'users').document(doc[0]).collection(u'bills')
                speech_inventory_documents=g.db.collection(u'users').document(doc[0]).collection(u'speech_inventory')

                barcode_inventory_collection=barcode_inventory_documents.get()
                bills_collection=bills_documents.get()
                speech_inventory_collection=speech_inventory_documents.get()

                Barcodes_Subset=de.ExtractorOfBarcodes(barcode_inventory_documents)
                
                totalBarcodes+=de.lengthOfCollection(barcode_inventory_collection)
                totalBills+=de.lengthOfCollection(bills_collection)
                totalSpeechInventory+=de.lengthOfCollection(speech_inventory_collection)

                if 'kiranaName' in doc[1]:
                    current_owner=doc[1]['kiranaName']
                    current_owner=current_owner.replace(' ','')
                    current_owner=current_owner.lower()
                if k==current_owner:
                    if kirana_Barcode_Set[k]==set():
                        kirana_Barcode_Set[k]=Barcodes_Subset & BarcodesSet 
                    else:
                        kirana_Barcode_Set[k]=kirana_Barcode_Set[k].union(Barcodes_Subset & BarcodesSet)
        new_list=[]
        for k in kirana_Barcode_Set.keys():
            for (a,b) in kirana_Barcode_Set[k]:
                new_list.append([k,a,b])
        
        return render_template('database/template_engine_1.html',authors=new_list,totalBills=totalBills,totalBarcodes=totalBarcodes,totalSpeechInventory=totalSpeechInventory)
    else:return(render_template("layout.html"))

@app.errorhandler(404)
def not_found(error):
    if(oidc.user_loggedin):
        return (render_template('routing/404.html'),404)
    else:return(render_template("layout.html"))
