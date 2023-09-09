"""View of port application"""
from http.client import NOT_FOUND
import bcrypt
from flask import render_template, jsonify, request, redirect, url_for, flash, session
import yaml
from urllib.parse import unquote
from ipaddress import ip_network
import sqlite3


def login_view():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = sqlite3.connect('app/database.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        conn.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['logged_in'] = True
            print("OK CONNECTED")
            return redirect(url_for('home.index'))
            
        else:
            print("!!!! NOT CONNECTED")
            return "Invalid credentials", 401
            
    else:
        return render_template('login.html')
