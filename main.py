import os
from flask import current_app, Blueprint, abort, redirect, request, url_for
from flask import render_template

from knn import get_top_k
from __init__ import dbconn
from emailSendUtil import sendEmail

main = Blueprint('main', __name__)

@main.route('/')
def index():
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('index.html', messages = messages)

@main.route('/userinfo')
def route_user_info():
    userid = int(request.args.get('userid'))
    isSomeoneElse = request.args.get('isSomeoneElse')
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    matchStr = request.args.get('matchStr')
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
      return render_template('additionalDetails.html',isSomeoneElse=isSomeoneElse, user=user, matchStr=matchStr)
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
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('mainPage.html', messages = messages)

@main.route('/profileSetup')
def profileSetup():
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    return render_template('profileSetup.html', user = current_app.config['curruser_info'])

@main.route('/profileSetup', methods=['POST'])
def profileSetup_post():
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    UPLOAD_FOLDER = 'static/'
    print(len(request.files))
    print(request.files['file'])
    file = request.files['file']
    name1 = request.form.get('name') 
    email = current_app.config['curruser_info'].email
    gender = request.form.get('Gender') 
    lang = request.form.get('Lang') 
    age = request.form.get('age') 
    food_pref = request.form.get('food_pref') 
    drinker = bool(int(request.form.get('Drinker')))
    username =current_app.config['curruser_info'].username
    shift = request.form.get('Shift') 
    filename = file.filename
    print(name1,email,gender,lang,age,food_pref,drinker,shift,username,filename) 

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    current_app.config['curruser_info'].profile_picture = filename
    current_app.config['curruser_info'].name = name1
    current_app.config['curruser_info'].email = email
    current_app.config['curruser_info'].gender = gender
    current_app.config['curruser_info'].lang= lang
    current_app.config['curruser_info'].age = age
    current_app.config['curruser_info'].food_pref = food_pref
    current_app.config['curruser_info'].drinker = drinker
    current_app.config['curruser_info'].shift = shift
    current_app.config['curruser_info'].username = username
    
    query, vals =current_app.config['curruser_info'].profileSetup()
     
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute(query, vals)
    conn.commit()
    return redirect(url_for('main.mainpage'))

@main.route('/viewprofile')
    
def viewprofile():
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    messages = request.args.get('messages')
    if not messages:
        messages = ""
    username=current_app.config['curruser_info'].username
    user = list(get_user_info(username))
    return redirect(url_for('main.route_user_info', userid=user[0], isSomeoneElse = False))
    
@main.route('/search')
def search():
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select passion from passions")
    passions = cur.fetchall()
    conn.close()
    return render_template('searchCriteria.html', passions = passions)

@main.route('/search', methods=['POST'])
def search_post():
    gender = request.form.get('gender')
    minAge = int(request.form.get('minAge'))
    maxAge = int(request.form.get('maxAge'))
    age = (minAge+maxAge)/2
    city = request.form.get('city')
    area = request.form.get('area')
    lang = request.form.get('lang')
    food_pref = request.form.get('food_pref')
    shift = request.form.get('shift')
    drinker = int(request.form.get('drinker'))
    passions = request.form.get('passions')

    print(gender, age, city, area, lang, food_pref, shift, drinker, passions)
    matches = get_top_k([gender, age, city, area, lang, food_pref, shift, drinker, passions])
    
    return redirect(url_for('main.result', matches=matches))

@main.route('/result')
def result():
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    matchStr = request.args.get('matchStr')
    print(matchStr)
    if not matchStr:
        matches = request.args.getlist('matches')
        matchStr = ""
        for m in matches:
            matchStr+=str(m)+","
        matchStr= matchStr[:-1]
    else:
        matches = []
        for m in matchStr.split(","):
            matches.append(int(m))
    print(matches)
    results = []
    for m in matches:
        results.append(get_user_info_by_id(m))

    return render_template('result.html', results=results, matchStr=matchStr)
 
@main.route('/email')
def email():
    if not current_app.config['curruser_info']:
        return redirect(url_for('auth.login'))
    user = request.args.getlist('user')
    curruser = get_user_info(current_app.config['curruser_info'].username)
    return render_template('email.html', user = user, curruser = curruser)
@main.route('/email', methods=['POST'])
def email_post():
    emailBody = request.form.get('emailBody')
    toUserid = int(request.form.get('toUserid'))
    sendEmail(emailBody,toUserid)
    return render_template('emailSuccess.html')


