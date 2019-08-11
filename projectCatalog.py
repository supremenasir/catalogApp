from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash
from functools import wraps
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
# login_session.clear()
CLIENT_ID = json.loads(
    open('/var/www/catalogApp/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# Connect to Database and create database session
#engine = create_engine('sqlite:///catalogwithusers.db')
engine = create_engine('postgresql://catalog:pass@localhost/catalog')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    email = login_session.get('email')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps(
                'Current user is already connected %s' %
                email), 200)
        response.headers['Content-Type'] = 'application/json'
        user_id = getUserID(email)
        login_session['user_id'] = user_id
        login_session['access_token'] = credentials.access_token
        login_session['gplus_id'] = gplus_id
        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        login_session['username'] = data['name']
        login_session['picture'] = data['picture']
        login_session['email'] = data['email']
        # ADD PROVIDER TO LOGIN SESSION
        login_session['provider'] = 'google'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showMain'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showMain'))


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


@app.route('/')
@app.route('/catalog')
def showMain():
    categories = session.query(Category).order_by(asc(Category.name))
    recentItems = session.query(Item).order_by(desc(Item.created_date))[:5]
    if 'username' not in login_session:
        return render_template('show_categories_public.html',
                               categories=categories,
                               recentItems=recentItems,
                               login_session=login_session)
    else:
        return render_template('show_categories_login.html',
                               categories=categories,
                               recentItems=recentItems,
                               login_session=login_session)


@app.route('/addItem', methods=['GET', 'POST'])
@login_required
def addItem():
    if request.method == 'POST':
        category = session.query(Category).filter_by(
            name=request.form['category']).one()
        newItem = Item(login_session['user_id'],
                       name=request.form['name'],
                       description=request.form['description'],
                       category=category)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMain'))
    else:
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template('new_item.html', categories=categories)


@app.route('/editItem/<int:itemId>', methods=['GET', 'POST'])
@login_required
def editItem(itemId):
    item = session.query(Item).filter_by(id=itemId).one()
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized.');\
        }</script><body onload='myFunction()'>"
    if request.method == 'GET':
        categories = session.query(Category).order_by(asc(Category.name))
        return render_template(
            'edit_item.html', item=item, categories=categories)
    else:
        category = session.query(Category).filter_by(
            name=request.form['category']).one()
        # Incase someone has changed the category, we have to remove the item
        # from existing.
        if (item.category.name != request.form['category']):
            session.delete(item)
            session.commit()
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            item.category.name = request.form['category']
        session.add(item)
        session.commit()
        return redirect(url_for('showMain'))


@app.route('/deleteItem/<int:itemId>', methods=['GET', 'POST'])
@login_required
def deleteItem(itemId):
    item = session.query(Item).filter_by(id=itemId).one()
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized.');}\
        </script><body onload='myFunction()'>"
    if request.method == 'GET':
        return render_template('deleteItem.html', item=item)
    else:
        session.delete(item)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showMain'))


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).order_by(asc(Category.name))
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    if 'username' not in login_session:
        return render_template('public.html', categories=categories,
                               items=items, category=category,
                               creator=creator, number=len(items))
    else:
        return render_template('users.html', categories=categories,
                               items=items, category=category,
                               creator=creator, number=len(items))


@app.route('/category/item/<int:ItemId>')
def showItem(ItemId):
    item = session.query(Item).filter_by(id=ItemId).one()
    if 'username' not in login_session:
        return render_template('showItem.html', item=item)
    else:
        return render_template('showItemEditable.html', item=item)


@app.route('/catalog/JSON')
def catalogJSON():
    items = session.query(Item).all()
    return jsonify(Category=[i.serialize for i in items])


@app.route('/catalog/<int:itemId>/JSON')
def itemJson(itemId):
    item = session.query(Item).filter_by(id=itemId).one()
    return jsonify(Item=item.serialize)


@app.route('/catalog/category/<int:categoryId>/JSON')
def categoryJson(categoryId):
    items = session.query(Item).filter_by(category_id=categoryId).all()
    return jsonify(Items=[i.serialize for i in items])


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
