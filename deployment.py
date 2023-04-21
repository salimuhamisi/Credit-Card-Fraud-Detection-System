from flask import Flask, render_template, request
import pandas as pd
import csv
import pickle
import pyrebase

config = {'apiKey': "AIzaSyBefe2mKXt1VKAQX8mIBO-t8P9vlSnOxOI",
          'authDomain': "authentication-aa8a2.firebaseapp.com",
          'projectId': "authentication-aa8a2",
          'storageBucket': "authentication-aa8a2.appspot.com",
          'messagingSenderId': "990851559095",
          'appId': "1:990851559095:web:84b9a9321fbc80d2b7e732",
          'measurementId': "G-LJ8QV83Q4F",
          'databaseURL': ""
          }


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()




app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.sign_in_with_email_and_password(email, password)
        return render_template("upload.html")

    elif request.method == 'GET':
        return "Get request"


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/read")
def read_page():
    return render_template("read.html")


@app.route("/upload", methods=['GET', 'POST'])
def upload_page():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        global results
        f = request.form['user_csv']
        results = pd.read_csv(f, names=['Time','V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28','Amount','Class'])
        with open(f) as file:
            user_csv = csv.reader(file)
            for row in user_csv:
                results.append(row)
        #results = pd.DataFrame(results)
        #results.columns = ['Time','V1',	'V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12','V13','V14','V15','V16','V17','V18','V19','V20','V21','V22','V23','V24','V25','V26','V27','V28','Amount','Class']
        #results = results
        return render_template('read.html', results=results.to_html(header=True, index=True))


@app.route("/contacts")
def contact_page():
    return render_template("contacts.html")


@app.route("/service")
def service_page():
    return render_template("service.html")


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    return render_template("register.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        auth.create_user_with_email_and_password(email, password)
        return render_template("home.html")

    elif request.method == 'GET':
        return "Get request"


@app.route("/analysis")
def analysis_page():
    global results

    shape= results.shape
    null= results.isnull().values.any()
    unique=[0, 1]
    counts = results['Class'].value_counts()
    percentage = results['Class'].value_counts(normalize=True)
    percentage=round(percentage, 4)



    items = [
        {"Feature": "Data Shape", "Description": shape},
        {"Feature": "Unique Target Values", "Description": unique},
        {"Feature": "Is There any null Values", "Description": null},
        {"Feature": "Total Normal Transactions", "Description": counts[0]},
        {"Feature": "Total Fraudulent Transactions", "Description": counts[1]},
        {"Feature": "percentage of Normal Transactions", "Description": percentage[0]* 100},
        {"Feature": "percentage of Fraudulent Transactions", "Description": percentage[1] * 100}
    ]
    return render_template("analysis.html", items=items)


@app.route("/prediction")
def prediction_page():
    global results

    filtered_df = results[results['Class'] == 1]
    # Convert dataframe to HTML table
    table_html = filtered_df.to_html()
    # Pass the HTML table to the template
    return render_template("predict.html", table=table_html)


if __name__ == '__main__':
    app.run(debug=True)
