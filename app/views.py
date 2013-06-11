from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from datetime import datetime

from app import app, collection, lm, oid

from forms import LoginForm, PostForm

from models import ROLE_USER, ROLE_ADMIN, User

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    user = g.user
    form = PostForm()
    if form.validate_on_submit():
        collection['posts'].insert({'body':form.body.data, 'author':g.user.doc['_id'], 'time': datetime.utcnow().isoformat()})
    posts = collection['posts'].find().sort('time', -1).limit(5)
    return render_template("index.html",        
        title = 'Home',        
        user = user,        
        posts = posts,
        form = form,
        col = collection
        )
        

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
        
@lm.user_loader
def load_user(id):
    u = collection['users'].find_one({'nickname':id})
    collection['log'].insert({'id':id, 'user':u})
    if u:
        return User(u['email'])
    else:
        return None
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@oid.after_login
def afer_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login, please try again.')
        return redirect(url_for('login'))
    
    user = collection['users'].find_one({'email':resp.email})
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = {'nickname':nickname, 'email':resp.email, 'role':ROLE_USER}
        collection['users'].insert(user)
        user = User(resp.email)
    else:
        user = User(user['email'])
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
    login_user(user, remember = remember_me )
    return redirect(request.args.get('next') or url_for('index'))
    
@app.before_request
def before_request():
    g.user = current_user

    