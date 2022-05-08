from email import message_from_binary_file
from pyexpat.errors import messages
from flask import Blueprint, redirect, render_template, request, url_for
from . import dbconn
from .import user_info

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('login.html', messages = messages)

@auth.route('/login', methods=['POST'])
def login_post():
    username=request.form.get('username')
    password = request.form.get('password')

    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from user_info where username=%s", (username,))
    a = cur.fetchone()

    if not a:
        return redirect(url_for('auth.signup', messages = "Account does not exist, please sign up"))
    
    is_profile_setup = False
    if a[4] != 0:
        is_profile_setup = True
    user = user_info.user_info(a[1], a[2], a[3], is_profile_setup,a[5], a[6], a[7],a[8], a[9], a[10],a[11], a[12], a[13],a[14], a[15], a[16],a[17])
    if user.password == password:
        
        user_info.curruser_info = user
        if not user_info.curruser_info.is_profile_Setup:
            return redirect(url_for('main.profileSetup',message="Welcome  "+user.username))
        else:
            return redirect(url_for('main.mainpage'))
    else:
        return redirect(url_for('auth.login', messages = "Incorrect username or password, please try again"))


@auth.route('/signup')
def signup():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('signup.html', messages = messages)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    cfmpassword = request.form.get('cfmpassword')
    print(username,email,password)
    if password != cfmpassword:
        return redirect(url_for('auth.signup', messages = "Passwords do not match please try again"))
        
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from user_info where username=%s", (username,))
    if len(cur.fetchall())==0:
        a = user_info.user_info(username,email,password)
        query, vals = a.insert()
        conn.reconnect()
        cur = conn.cursor()
        cur.execute(query, vals)
        conn.commit()
        
    else:
        return redirect(url_for('auth.signup', messages = "user name  already exists. go back to login"))
    return redirect(url_for('auth.login', messages = "User successfully created! Please Login to start your journey."))

@auth.route('/logout')
def logout():
    user_info.curruser_info = None
    return redirect(url_for('main.index'))