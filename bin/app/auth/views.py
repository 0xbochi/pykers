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

        if user and bcrypt.checkpw(password, user[2]):
            session['logged_in'] = True
            return redirect(url_for('home.index'))
        return "Invalid credentials", 401

    else:
        return render_template('login.html')


def users_view():
    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    conn.close()
    user_list = [user[0] for user in users]
    return render_template('users.html', users=user_list) 


def resetpasswd_view():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            conn = sqlite3.connect('app/database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
            conn.commit()
            conn.close()
            return "Password updated successfully", 200
        return "Passwords do not match", 400
    else:
        return render_template('reset_password.html')

def delete_user_view():
    username = request.form['username']
    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return "User deleted successfully", 200


def new_user_view():
    username = request.form['username']
    password = request.form['password']
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('app/database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return "User created successfully", 200
