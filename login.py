from flask import request, redirect, session, flash, render_template
from werkzeug.security import check_password_hash
from db import mongo  # Import mongo from db.py

def handle_login():
    if request.method == 'POST':
        identifier = request.form.get('username')  # Use the identifier field for username/email
        password = request.form.get('password')

        # Validate input fields
        if not identifier or not password:
            flash("Username or email and password are required!", "error")
            return redirect('/login')

        # Find user in the database by either email or username
        user = mongo.db.users.find_one({
            '$or': [
                {'username': identifier},  # Assuming you have a username field
                {'email': identifier}      # Email field
            ]
        })

        if user and check_password_hash(user['password'], password):
            # Set session variables upon successful login
            session['username'] = user['username']  # Store the username in the session
            flash("Login successful!", "success")
            return redirect('/dashboard')  # Redirect to the dashboard after login
        else:
            flash("Invalid username/email or password!", "error")
            return redirect('/login')

    return render_template('login.html')  # Render the login page if GET request
