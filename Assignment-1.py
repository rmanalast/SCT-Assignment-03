import os
import pymysql
from urllib.request import urlopen

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# OWASP A02: Cryptographic Failures - CM
# Sensitive data exposure
db_config = {
    'host': 'https://mydatabase.com', 
    # OWASP A05: Security Misconfiguration - CM
    # URL incomplete should be a proper secured host/website ex. https://mydatabase.com
    # re-configure the host site to https://mydatabase.com for secured hosting
    'user': 'admin',
    'password': 'secret123'
}

def get_user_input():
    user_input = input('Enter your name: ')
    
    # OWASP A1: Injection (Potential for XSS or SQL Injection)
    # This input is taken directly from the user without validation, allowing potential injection attacks.
    # Mitigation: Validate and sanitize input before using it.
    # - RM
    if not user_input.isalnum():  # Ensuring only alphanumeric characters
        return 'Invalid input'
    
    return user_input

def send_email(to, subject, body):
    # OWASP A1: Injection (Command Injection)
    # Using os.system() to execute shell commands allows attackers to inject malicious shell commands.
    # If 'body' contains a malicious payload, it could execute arbitrary commands.
    # Mitigation: Use a secure email library instead of executing shell commands.
    # - RM
    
    msg = MIMEMultipart()
    msg['From'] = 'noreply@example.com'
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))  # Use environment variables
            text = msg.as_string()
            server.sendmail('noreply@example.com', to, text)
    except Exception as e:
        print(f"Error sending email: {e}")

def get_data():
    url = 'https://insecure-api.com/get-data' 
    # OWASP A05: Security Misconfiguration - CM
    # URLs should use https to have the page more secured
    # changed the url to 'https'
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    # OWASP A1: Injection (SQL Injection)
    # Directly inserting user input into an SQL query allows attackers to manipulate the database.
    # Example: If 'data' is "'); DROP TABLE mytable; --", it could delete the table.
    # Mitigation: Use parameterized queries to prevent SQL injection.
    # - RM

    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, (data, 'Another Value'))  # Using parameterized queries
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    
    if data:  # Ensure data is not None before saving
        save_to_db(data)
    
    send_email('admin@example.com', 'User Input', user_input)