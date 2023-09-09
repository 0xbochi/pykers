"""View of port application"""
from http.client import NOT_FOUND
from flask import render_template, jsonify, request, redirect, url_for, flash
import yaml
from urllib.parse import unquote
from ipaddress import ip_network



def login_view():
    
    return render_template('login.html')

