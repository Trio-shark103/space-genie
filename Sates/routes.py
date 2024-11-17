from Sates import app, db
from flask import render_template,request, redirect, url_for, flash
from Sates.models import Satellite, User
from Sates.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/Info')
def info_page():
    return render_template('info.html')

with app.app_context():
    if not os.path.exists("satellite.db"):
        db.create_all()

# update route       
@app.route("/Updates")
def sate_update():
    search_term = request.args.get("search", "").strip()
    if search_term:
        # Filter satellites where search term matches any field
            satellites = Satellite.query.filter(
                Satellite.name.ilike(f"%{search_term}%")|
                Satellite.satellite_type.ilike(f"%{search_term}%") |
                Satellite.manufacturer.ilike(f"%{search_term}%") |
                Satellite.continent.ilike(f"%{search_term}%") |
                Satellite.cost.ilike(f"%{search_term}%")
                ).all()
    else:
        # Show all satellites by default if no search term is provided
        satellites = Satellite.query.all()
        
    return render_template("Updates.html", satellites=satellites)

# route to register the new users
@app.route('/register', methods=['GET','POST'])
def register_page():
    form= RegisterForm()
    #Adding Validation to the submit button
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category="success")
        
        return redirect(url_for('sate_update'))
    if form.errors !={}: #if any error occur during validations
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}', category='danger')
            
    return render_template('register.html', form=form)


#route to enable users to login on the page .
@app.route('/login', methods=['GET','POST'])
def login_page():
    form=LoginForm()
    #Adding validation to the login button
    if form.validate_on_submit():
        attempted_user =User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='Success')
            return redirect(url_for('sate_update'))
        else:
            flash('Username and password are not match! Please try again',category='danger')
            
    return render_template('login.html', form=form)

#route to enable users to logout off the page
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))