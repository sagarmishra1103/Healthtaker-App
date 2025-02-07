import datetime
from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from db import mongo  # Import mongo from db.py

def handle_signup():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        contact_no = request.form.get('contact_no')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        username = request.form.get('username')  # Get username from the form
        # Validate input fields
        if not firstname or not lastname or not email or not contact_no or not password or not confirm_password:
            flash("All fields are required!", "error")
            return redirect('/signup')

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect('/signup')

        # Hash the password before saving it
        hashed_password = generate_password_hash(password)

        # Insert into MongoDB
        mongo.db.users.insert_one({
            'firstname': firstname,
            'lastname': lastname,
            'username': username,  # Include username in the MongoDB insert
            'email': email,
            'contact_no': contact_no,
            'password': hashed_password,
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        })

        flash("Signup successful! You can now log in.", "success")
        return redirect('/login')  # Redirect to login page after signup

    return render_template('signup.html')  # Render the signup form if GET request




