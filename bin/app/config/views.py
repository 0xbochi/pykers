"""View of port application"""
from http.client import NOT_FOUND
from flask import render_template, jsonify, request, redirect, url_for, flash
import yaml
from urllib.parse import unquote
from ipaddress import ip_network


def config_view():
    if request.method == 'POST':
        if 'auth_required' in request.form or 'auth_config_submit' in request.form:
            auth_required = request.form.get('auth_required') == 'on'
            print(f"Auth Required: {auth_required}") 
            with open('app/config.yaml', 'r') as file:
                config = yaml.safe_load(file)

            config['AUTH_REQUIRED'] = auth_required

            with open('app/config.yaml', 'w') as file:
                yaml.safe_dump(config, file)

        elif 'ip_address' in request.form:
            new_ip = request.form.get('ip_address')

            try:
                ip_network(new_ip)
            except ValueError:
                flash('Invalid IP/CIDR', 'error')
                return redirect(url_for('config.config_view'))

            with open('app/config.yaml', 'r') as file:
                config = yaml.safe_load(file)

            config['ALLOWED_IPS'].append(new_ip)

            with open('app/config.yaml', 'w') as file:
                yaml.safe_dump(config, file)

        return redirect(url_for('config.config_view'))

    with open('app/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    return render_template('config.html', allowed_ips=config['ALLOWED_IPS'], auth_required=config.get('AUTH_REQUIRED', False))


def delete_ip():
    data = request.get_json()
    ip_to_delete = data.get('ip')

    with open('app/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    if ip_to_delete in config.get('ALLOWED_IPS', []):
        config['ALLOWED_IPS'].remove(ip_to_delete)

        with open('app/config.yaml', 'w') as file:
            yaml.safe_dump(config, file)

        return jsonify(success=True)
    else:
        return jsonify(success=False), 400