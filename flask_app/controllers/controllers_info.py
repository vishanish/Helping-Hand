from ast import Add
from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.models_users import User
from flask_app.models.models_specialities import Speciality
from flask_app.models.models_businesshours import Business
from flask_app.models.models_address import Address

# renders the index page
@app.route('/')
def index():
    return render_template('index.html')


# renders the create/login page
@app.route('/registerlogin')
def account():
    # this is to prevent the user from going back to logincreate template when the user is in session
    if 'sfirst_name' and 'semail' in session:
        if (session['seekprov'] == 'provider'):
            return redirect ('/provider')
        elif (session['seekprov'] == 'seeker'):
            return redirect ('/seeker')
    return render_template('logincreate.html')

# performs action to Register the user on create/login page
# action route
@app.route('/user/register', methods = ['POST'])
def userregister():
    if not User.validate_register(request.form):
        return redirect('/registerlogin')
    # request.form gets the data from the form. In this case, the registration form.
    # session is a dictionary
    session['first_name'] = request.form["first_name"]
    session['email'] = request.form["email"]
    session['password'] = request.form['password']
    session['seekprov'] = request.form['seekprov']
    """When the code reaches this step, the data from the form is lost.
        Because of this there is no information that is available on the template in the display action
        To get the data from the form, we need to use session"""
    data = {
        "first_name" : request.form['first_name'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "seekprov" : request.form['seekprov']
        }
    User.save_reg(data)
    # when a route has a post method, do not render template on this route. redirect to a different route.
    if(session['seekprov'] == 'provider'):
        return redirect ("/provider")
    elif(session['seekprov'] == 'seeker'):
        return redirect ("/seeker")

# session must be cleared when user exit the page
@app.route("/user/logout")
def userlogout():
    session.clear()
    # we can also delete specific data from the session when logging out (del)
    # del session["sfirst_name"]
    return redirect("/")
    

# performs action for the Register user on create/login page
# action route
@app.route('/user/login', methods = ['POST'])
def userlogin():
    if not User.login_validation(request.form):
        return redirect('/registerlogin')
    data = {
        "email" : request.form['email']
        }
    # request.form gets the data from the form. In this case, the registration form.
    # session is a dictionary
    """When the code reaches this step, the data from the form is lost.
        Because of this there is no information that is available on the template in the display action
        To get the data from the form, we need to use session"""

    user_db = User.get_users_by_email(data)
    session["email"] = user_db.email
    session["seekprov"] = user_db.seekprov
    session['first_name'] = user_db.first_name
    # when a route has a post method, do not render template on this route. redirect to a different route.
    if(session['seekprov'] == 'provider'):
        return redirect ("/provider")
    elif(session['seekprov'] == 'seeker'):
        return redirect ("/seeker")

@app.route('/provider')
def provider():
    # this is to prevent crashing of page when a user has logged out and tries to use a back button
    # if 'first_name' and 'email' not in session:
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }

    # this is one way to transfer data from the session to the template
    # another way is to called the session in the template itself
    return render_template("provider.html", user_card = User.get_users_by_email(data), business_card = Business.get_provider_hours_by_email(data),
    speciality_card = Speciality.get_provider_speciality_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route('/provider/form')
def providerform():
    data = {
        "email":session["email"]
    }
    return render_template("providerform.html", user_card = User.get_users_by_email(data), business_card = Business.get_provider_hours_by_email(data),
    speciality_card = Speciality.get_provider_speciality_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route("/provider/form/add", methods = ['POST'])
def providerformadd():
    data1 = {
        "email" : session ['email'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "phone_number" : request.form['phone_number'],
        "occupation" : request.form['occupation']
    }
    User.update_provider_users_by_email(data1)
    data2 = {
        "sundayopen" : request.form ['sundayopen'],
        "sundayclose" : request.form['sundayclose'],
        "mondayopen" : request.form['mondayopen'],
        "mondayclose" : request.form['mondayclose'],
        "tuesdayopen" : request.form['tuesdayopen'],
        "tuesdayclose" : request.form['tuesdayclose'],
        "wednesdayopen" : request.form['wednesdayopen'],
        "wednesdayclose" : request.form['wednesdayclose'],
        "thursdayopen" : request.form['thursdayopen'],
        "thursdayclose" : request.form ['thursdayclose'],
        "fridayopen" : request.form ['fridayopen'],
        "fridayclose" : request.form['fridayclose'],
        "saturdayopen" : request.form['saturdayopen'],
        "saturdayclose" : request.form['saturdayclose'],
        "user_email" : session['email']
    }
    Business.update_provider_hours_by_email(data2)
    data3 = {
        "male" : True if request.form.get('male') else False,
        "female" : True if request.form.get('female') else False,
        "lgbtq" : True if request.form.get('lgbtq') else False,
        "gender_other" : request.form['gender_other'],
        "physical" : True if request.form.get('physical') else False,
        "mental" : True if request.form.get('mental') else False,
        "financial" : True if request.form.get('financial') else False,
        "hardship_other" : request.form ['hardship_other'],
        "citizen" : True if request.form.get('citizen') else False,
        "immigrant" : True if request.form.get('immigrant') else False,
        "refugee": True if request.form.get('refugee') else False,
        "status_other" : request.form['status_other'],
        "user_email": session['email']
    }
    Speciality.update_provider_speciality_by_email(data3)
    data4 = {
        "house_number" : request.form['house_number'],
        "street_name" : request.form['street_name'],
        "suite_number" :request.form['suite_number'],
        "city_name" : request.form['city_name'],
        "state" : request.form['state'],
        "zip_code" : request.form ['zip_code'],
        "user_email" : session['email']
    }
    Address.update_provider_address_by_email(data4)
    return redirect("/provider")

@app.route('/provider/delete', methods = ['POST'])
def providerdelete():
    data ={
        "email": session['email']
    }
    User.delete_provider_user_account(data)
    return redirect('/registerlogin')


@app.route('/seeker')
def seeker():
    # this is to prevent crashing of page when a user has logged out and tries to use a back button
    if 'first_name' and 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    # this is one way to transfer data from the session to the template
    # another way is to called the session in the template itself
    return render_template("seeker.html", user_card = User.get_users_by_email(data), speciality_card = Speciality.get_seeker_speciality_by_email(data), address_card = Address.get_seeker_address_by_email(data))

@app.route('/seeker/form')
def seekerform():
    data = {
        "email":session["email"]
    }
    return render_template("seekerform.html", user_card = User.get_users_by_email(data), speciality_card = Speciality.get_seeker_speciality_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route("/seeker/form/add", methods = ['POST'])
def seekerformadd():
    data1 = {
        "email" : session ['email'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "phone_number" : request.form['phone_number']
    }
    User.update_seeker_users_by_email(data1)
    data3 = {
        "male" : True if request.form.get('male') else False,
        "female" : True if request.form.get('female') else False,
        "lgbtq" : True if request.form.get('lgbtq') else False,
        "gender_other" : request.form['gender_other'],
        "physical" : True if request.form.get('physical') else False,
        "mental" : True if request.form.get('mental') else False,
        "financial" : True if request.form.get('financial') else False,
        "hardship_other" : request.form ['hardship_other'],
        "citizen" : True if request.form.get('citizen') else False,
        "immigrant" : True if request.form.get('immigrant') else False,
        "refugee": True if request.form.get('refugee') else False,
        "status_other" : request.form['status_other'],
        "user_email": session['email']
    }
    Speciality.update_seeker_speciality_by_email(data3)
    data4 = {
        "city_name" : request.form['city_name'],
        "state" : request.form['state'],
        "zip_code" : request.form ['zip_code'],
        "user_email" : session['email']
    }
    Address.update_seeker_address_by_email(data4)
    return redirect("/seeker")

@app.route('/seeker/delete', methods = ['POST'])
def seekerdelete():
    data ={
        "email": session['email']
    }
    User.delete_seeker_user_account(data)
    return redirect('/registerlogin')