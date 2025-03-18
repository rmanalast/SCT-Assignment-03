import os
import pickle
import yaml
import subprocess
import hashlib
import marshal
import xml.etree.ElementTree as ET
from flask import Flask, session, request
import tempfile
import ssl

app = Flask(__name__)
app.secret_key = "very_secret_key_12345"

# Dangerous import of Pickle
def load_user_preferences(data):
    return pickle.loads(data)  # Insecure deserialization

# Python OS injection
def run_command(command):
    os.system(command)  # Command injection vulnerability

# Insecure Hash Algorithm
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is insecure

# Popen command injection
def execute_ping(ip_address):
    subprocess.Popen(f"ping -c 1 {ip_address}", shell=True)  # Command injection

# Python insecure cryptography
def weak_encrypt(data, key):
    # Very weak XOR encryption
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

# Python SQL injection
def get_user(username):
    conn = None  # Placeholder for actual DB connection
    query = f"SELECT * FROM users WHERE username = '{username}'"  # SQL injection
    # cursor.execute(query)
    return None

# Raw XML packages
def parse_xml(xml_data):
    return ET.fromstring(xml_data)  # Potential XXE vulnerability

# Eval code injection
def calculate(expression):
    return eval(expression)  # Dangerous eval

# Input name store procedure
def process_user_input():
    user_input = input("Enter command: ")
    return calculate(user_input)  # Passes user input to eval

# Insecure YAML load usage
def parse_config(yaml_data):
    return yaml.load(yaml_data)  # Should use yaml.safe_load instead

# Join and relpath path traversal
def get_file_path(filename):
    base_dir = "/var/www/"
    return os.path.join(base_dir, filename)  # Path traversal if filename contains ../

# mark_safe is vulnerable to XSS
def display_user_content(content):
    # Simulating Django's mark_safe
    return f"<div>{content}</div>"  # XSS vulnerability

# Marshal file load in Python
def load_code_object(file_path):
    with open(file_path, 'rb') as f:
        return marshal.load(f)  # Insecure deserialization

# SSL context override
def create_insecure_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

# UserData in a flask session cookie
@app.route('/set_user_data')
def set_user_data():
    user_data = request.args.get('data')
    session['user_data'] = user_data  # No validation before storing
    return "User data set"

# Using 777 with umask
def create_temp_file():
    fd, path = tempfile.mkstemp()
    os.chmod(path, 0o777)  # Insecure permissions
    return path

# Insecure FTP usage
def connect_ftp():
    import ftplib
    ftp = ftplib.FTP('ftp.example.com')
    ftp.login('anonymous', 'anonymous@')  # Anonymous FTP login
    return ftp

if __name__ == "__main__":
    # Testing various vulnerable functions
    user_data = b'\x80\x04\x95\x10\x00\x00\x00\x00\x00\x00\x00\x8c\x08builtins\x94\x8c\x07__dict__\x94\x93\x94.'
    prefs = load_user_preferences(user_data)
    
    run_command("echo Hello World")
    
    hashed = hash_password("password123")
    
    execute_ping("8.8.8.8")
    
    app.run(debug=True)  # Running Flask in debug mode