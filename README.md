# flask-crud
[Personal Project] - flask-crud
Simple web app that hosts inventory dashboard created with python3, okta, bootstrap and firebase.
You can go to dashboard and from there you can either go to users inventory dashboard, look at pie-chart of barcodes or 
logout.

<img src="https://github.com/prakHr/flask-crud/blob/master/flask-introduction/flask_introduction/library/static/flask-crud.jpg" width="480" height="300">

## Table of contents
* [Summary](#summary)
* [Setup](#setup)
* [Technologies](#technologies)
* [Modules](#modules)
* [Material Icons](#icons)
* [Other Downloads](#downloads)
* [Directory Structure](#structure)
* [Installation Procedure](#procedure)

---
### Summary
My first in the series of coming apps using flask. Have this idea of building an __interactive dashboard app__ for a very 
long time. Choosen __flask__ for its simplicity and scalability into large nosql database (in this case firestore).
Also flask uses very useful __jinja2__ template rendering that can take multiple variables and __python list__ as well as 
__dict__ as input and renders that.

Then I started looking into __login page__ and choose okta for first time building purpose. After that I reconfigured 
__OpenID connect__ of okta portal and finally created the login page. Used firestore as database among many as it 
was developed by google and being very easy extractability of __collections__ and __documents__ inside it using a single api.

I followed the __[tutorial](https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one 
"Simple Flask app with database SQLAlchemy")__ and the idea, but then decided to challenge myself by changing the technology
the tutorial used.
Instead of ~~SQLAlchemy and Google App Engine~~ I used __Flask and server as python anywhere__.
This was challenging since it was my first time using firebase-admin api, flask-oidc and deploying a Web Application.

---

### Setup
At this stage I experimented with different javascript like chartist.js and charts.js for making all sorts of charts like
__spline area__, __column__, __doughnut__ ones apart from simple __line__, __bar__ ones. Then I looked into __dataTables__ to render 
a huge chunk of data taken from database present in __array__ and added options like __search and list either 10 or 25 items__ 
in a page.

After that I looked into __caching__ the data as well as the page so that it loads immediately after refreshing the page 
for the same data as this information can be easily __memoized__. But I ran into problems like memoizing the login page at the
first iteration.Then took that into consideration and realised that other coders can manipulate data using their 
own javascript code. So reconfigured the app.

Finally, added __material icons__ for attraction purpose which also renders data. 


---

### Technologies
* Python3.6
* Flask
* Okta
* Firebase
* Google App Engine
* Git

---

### Modules
* okta
* Flask
* Werkzeug
* flask-oidc
* flask-caching
* firebase-admin
* bootstrap -4/3.4.1
* chartist
* dataTables.min.css/js-1.10.20
* canvasjs
* jquery-3.4.1/3.3.1
* popper.js@1.16.0
* core.js
* charts.js
* wordCloud.js
* animated.js
* font-awesome.min.css
* jquery-1.11.1.min.js
* gcloud
* google-cloud-storage

---

### Icons
* dashboard 
* added
* mic
* local_offer
* update
* fa fa-barcode

---

### Downloads
* [available error pages to choose from](https://colorlib.com/wp/free-error-page-templates/ "My favorite 404 error page")
* [canvasjs downloader](https://canvasjs.com/download-html5-charting-graphing-library/ "Download examples of charts here")
* [portions that you like to use from existing material dashboard](https://www.creative-tim.com/product/material-dashboard/?partner=49926 "By Creative Tim")

---

### Structure
```bash
|_flask_introduction
  |_myFlaskApp.py
  |_database_extractor.py
  |_ client_secrets.json
  |_ project1-a9674-firebase-adminsdk-ddztm-263a615578.json
  |_library
  | |_ _01_simple.py
  | |_ _02_html_inside_view.py
  | |_ _03_01_template_str_inside_view_with_database.py
  | |_ _03_template_str_inside_view.py
  | |_ _04_template_outside_view.py
  | |_ _05_database_app_template_eng.py
  | |_ client_secrets.json
  | |_ project1-a9674-firebase-adminsdk-ddztm-263a615578.json
  |___static
  |   |_bg.jpg
  |   |_canvasjs.min.js
  |   |_clients_secrets.json
  |   |_colorlib-style.css
  |   |_flask-crud.jpg
  |   |_style.css
  |___templates
       |_database
       |  |_barcodes_template.html
       |  |_data_table_demo.html
       |  |_template_engine.html
       |  |_template_engine_1.html
       |  |_word_cloud_demo.html
       |_routing
       |  |_404.html
       |_dashboard.html
       |_index.html
       |_layout.html
```

---

### Procedure
```console
prakhar@prakhar:~$ cd Downloads/flask-introduction
prakhar@prakhar:~~/Downloads/flask-introduction$ source virtual/bin/activate
(virtual)prakhar@prakhar:~~/Downloads/flask-introduction$ pip install -r requirements.txt
(virtual)prakhar@prakhar:~~/Downloads/flask-introduction$ cd flask_introduction
(virtual)prakhar@prakhar:~~/Downloads/flask-introduction/flask_introduction$ FLASK_APP=myFlaskApp.py flask run
```

