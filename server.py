from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = "SecretSecret123"
mysql = MySQLConnector(app,'emaildb')

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')


    
@app.route('/success', methods=['POST']) #THIS MAKES YOUR DATABASE ENTRY SHOW ON THE PAGE!!
def success():
    session['email'] = request.form['email']
    
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Email is not valid!")
        print "2"
        return redirect('/')
    #we want to insert into our query
    else:
        
        flash("The email address you entered {} is a VALID email address! Thank you!".format(session['email']))
        
        query = "SELECT * FROM emails"
        emails = mysql.query_db(query)
        print emails

        query2 = "INSERT INTO emails(email,created_at,updated_at) VALUES (:email, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    
        data = {
            'email': request.form['email'],
        }
    # Run query, with dictionary values injected into the query
        mysql.query_db(query,data)
        return render_template('success.html',all_emails=emails)


app.run(debug=True)