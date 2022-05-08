from inspect import currentframe
import os
from unicodedata import name
from flask import Blueprint, abort, redirect, request, url_for
from flask import render_template
from . import dbconn
from . import animal
from . import user_info

main = Blueprint('main', __name__)

@main.route('/')
def index():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('index.html', messages = messages)

@main.route('/<int:userid>')
def route_user_info(userid):
    if not user_info.curruser_info:
        return redirect(url_for('auth.login'))
        
    user = list(get_user_info_by_id(userid))
    print(user)
    print(user[15])
    if not user[15]:
        user[15] = "notfound"
    if  user[16]:
        user[16] = "Yes"
    else:
        user[16]="No"
    if  user[13]:
        user[13] = "Yes"
    else:
        user[13]="No"
    if user[18]:
      return render_template('additionalDetails.html',user=user)
    else:
     return render_template('viewProfile.html',user=user)

def get_user_info_by_id(userid):
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from user_info where userid=%s", (userid,))
    userinfo = cur.fetchone()
    conn.close()
    if userinfo is None:
        abort(404)
    return userinfo    
 

def get_user_info(username):
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select * from user_info where username=%s", (username,))
    userinfo = cur.fetchone()
    conn.close()
    if userinfo is None:
        abort(404)
    return userinfo

@main.route('/mainpage')
def mainpage():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('mainPage.html', messages = messages)

@main.route('/search')
def search():
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select passion from passions")
    passions = cur.fetchall()
    conn.close()
    return render_template('searchCriteria.html', passions = passions)

@main.route('/search', methods=['POST'])
def search_post():
    # TODO: implement search criteria knn whatever
    return "TODO"


@main.route('/profileSetup')
def profileSetup():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('profileSetup.html', user = user_info.curruser_info)

@main.route('/profileSetup', methods=['POST'])
def profileSetup_post():
    UPLOAD_FOLDER = 'static/'
    print(len(request.files))
    print(request.files['file'])
    file = request.files['file']
    name1 = request.form.get('name') 
    email = user_info.curruser_info.email
    gender = request.form.get('Gender') 
    lang = request.form.get('Lang') 
    age = request.form.get('age') 
    food_pref = request.form.get('food_pref') 
    drinker = bool(int(request.form.get('Drinker')))
    username =user_info.curruser_info.username
    shift = request.form.get('Shift') 
    filename = file.filename
    print(name1,email,gender,lang,age,food_pref,drinker,shift,username,filename) 

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    user_info.curruser_info.profile_picture = filename
    user_info.curruser_info.name = name1
    user_info.curruser_info.email = email
    user_info.curruser_info.gender = gender
    user_info.curruser_info.gang= lang
    user_info.curruser_info.age = age
    user_info.curruser_info.food_pref = food_pref
    user_info.curruser_info.drinker = drinker
    user_info.curruser_info.shift = shift
    user_info.curruser_info.username = username
    
    query, vals =user_info.curruser_info.profileSetup()
     
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute(query, vals)
    conn.commit()
    return redirect(url_for('main.mainpage'))

@main.route('/viewprofile')
    
def viewprofile():
    print("drinker:",user_info.curruser_info.drinker)
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    username=user_info.curruser_info.username
    user = list(get_user_info(username))
    return redirect(url_for('main.route_user_info', userid=user[0]))
     

#TODO: this is sus
@main.route('/details')
def details():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    username=user_info.curruser_info.username
    user = list(get_user_info(username))
    if not user[15]:
        user[15] = "notfound"
    if  user[13]:
        user[13] = "Yes"
    else:
        user[13]="No"
    if  user[16]:
        user[16] = "Yes"
    else:
        user[16]="No"
    return render_template('additionalDetails.html',user=user, messages = messages)
@main.route('/details', methods=['POST'])
def details_post():
    return redirect(url_for('main.details'))
# until here

@main.route('/email')
def email():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('email.html', messages = messages)
@main.route('/email', methods=['POST'])
def email_post():
    #TODO implement this
    return "TODO"

@main.route('/result')
def result():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('result.html', messages = messages)
@main.route('/viewprofile', methods=['POST'])
def result_post():
    return redirect(url_for('main.result'))
