import os
import secrets
import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_file, session, url_for)

from datetime import datetime, timedelta
from src.genai import chatbot_response,prompt_educational,prompt_sales


current_date = str(datetime.now()).split(" ")[0]
date_obj = datetime.strptime(current_date, "%Y-%m-%d")

one_year_ago = date_obj + timedelta(days=1)  # 365, 450
current_date_info = one_year_ago.strftime("%Y-%m-%d")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(24))

# metainfo
metainfo = dict()
metainfo['type_prompt']    = ['Educational','Sales']


# User data for Demonstration
USERS               = {"admin": "1234"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if USERS.get(username) == password:
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials, please try again.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("home_form_data", None)  # Clear home form data from the session
    session.pop("page_form_data", None)  # Clear page form data from the session
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Define a route for the sectoral page
@app.route('/')
def home():
    if "username" in session:

        return render_template(
            "home.html",
            username=session["username"],
            form_data=metainfo,
            current_date=current_date,
        )
    
    return redirect(url_for("login"))

@app.route("/submit_home_form", methods=["POST"])
def submit_home_form():
    # Retrieve form data from home.html


    prompt_info      = request.form.get('type_prompt')
    
    prompt_type_list = [prompt_info]

    for cols in ['Educational','Sales']:
        if cols not in prompt_type_list:
            prompt_type_list.append(cols)
     
    metainfo['type_prompt']       = prompt_type_list

    flash("Form submitted successfully for Home page!", "success")
    return redirect(url_for("home"))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    # print(metainfo['type_prompt'])
    try:
        if metainfo['type_prompt'][0]=='Educational':
            bot_reply = chatbot_response(user_message,prompt_educational)

        if metainfo['type_prompt'][0]=='Sales':
            bot_reply = chatbot_response(user_message,prompt_sales)
    except:
            bot_reply = "I'm not sure how to respond to that."

    print(f"User:{user_message}\nResponse:{bot_reply}")
    return jsonify({"reply": bot_reply})

# def get_bot_response(message):
#     responses = {
#         "hi": "Hello! How can I assist you?",
#         "how are you": "I'm just a bot, but I'm doing great!",
#         "bye": "Goodbye! Have a great day!"
#     }
#     return responses.get(message.lower(), "I'm not sure how to respond to that.")

if __name__ == '__main__':
    app.run(debug=True)