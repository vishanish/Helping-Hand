from datetime import date
from re import S
from flask_app import app
from flask import redirect, render_template, request, session
from flask_app.models.models_users import User
from flask_app.models.models_specialities import Speciality
from flask_app.models.models_businesshours import Business
from flask_app.models.models_address import Address
from flask_app.models.models_appointments import Appointment

# renders the index page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gender/male')
def male():
    return render_template('male.html', male_provider = User.get_male_provider_seeker_homepage())

@app.route('/gender/female')
def female():
    return render_template('female.html', female_provider = User.get_female_provider_seeker_homepage())

@app.route('/gender/lgbtq')
def lgbtq():
    return render_template('lgbtq.html', lgbtq_provider = User.get_lgbtq_provider_seeker_homepage())

@app.route('/gender/any_gender')
def any_gender():
    return render_template('any_gender.html', any_gender_provider = User.get_any_gender_provider_seeker_homepage())

@app.route('/hardship/physical')
def physical():
    return render_template('physical.html', physical_provider = User.get_physical_provider_seeker_homepage())

@app.route('/hardship/mental')
def mental():
    return render_template('mental.html', mental_provider = User.get_mental_provider_seeker_homepage())

@app.route('/hardship/financial')
def financial():
    return render_template('financial.html', financial_provider = User.get_financial_provider_seeker_homepage())

@app.route('/hardship/any_hardship')
def any_hardship():
    return render_template('any_hardship.html', any_hardship_provider = User.get_any_hardship_provider_seeker_homepage())

@app.route('/status/citizen')
def citizen():
    return render_template('citizen.html', citizen_provider = User.get_citizen_provider_seeker_homepage())

@app.route('/status/immigrant')
def immigrant():
    return render_template('immigrant.html', immigrant_provider = User.get_immigrant_provider_seeker_homepage())

@app.route('/status/refugee')
def refugee():
    return render_template('refugee.html', refugee_provider = User.get_refugee_provider_seeker_homepage())

@app.route('/status/any_status')
def any_status():
    return render_template('any_status.html', any_status_provider = User.get_any_status_provider_seeker_homepage())


# ---------------------------------------- User Routes ----------------------------------------
# renders the create/login page
@app.route('/registerlogin')
def account():
    # this is to prevent the user from going back to logincreate template when the user is in session
    if 'first_name' and 'email' in session:
        if (session['seekprov'] == 'provider'):
            return redirect ('/provider/dashboard')
        elif (session['seekprov'] == 'seeker'):
            return redirect ('/seeker/dashboard')
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
        return redirect ("/provider/dashboard")
    elif(session['seekprov'] == 'seeker'):
        return redirect ("/seeker/dashboard")

    

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
        return redirect ("/provider/dashboard")
    elif(session['seekprov'] == 'seeker'):
        return redirect ("/seeker/dashboard")

# session must be cleared when user exit the page
@app.route("/user/logout")
def userlogout():
    session.clear()
    # we can also delete specific data from the session when logging out (del)
    # del session["sfirst_name"]
    return redirect("/")

# ---------------------------------------- Provider Routes ----------------------------------------

@app.route('/provider/dashboard')
def providerdashboard():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("providerdashboard.html", user_card = User.get_users_by_email(data), set_appointment = Appointment.show_confirmed_appts_provider(data))

@app.route('/provider/setappointment')
def providersetappt():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("providerappointsetup.html", user_card = User.get_users_by_email(data))

@app.route('/provider/appointment/set', methods = ['POST'])
def providerapptset():
    data ={
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "seeker_email" : request.form["seeker_email"],
        "seeker_phone_number" : request.form["seeker_phone_number"],
        "apptdate" : request.form["apptdate"],
        "appttime" : request.form["appttime"],
        "confirmed" : True if request.form.get('confirmed') else False,
        "requested" : 0,
        "email" : session['email']
    }
    Appointment.create_appts(data)
    return redirect("/provider/dashboard")

@app.route("/provider/confirmed/update", methods = ['POST'])
def providconfirmupdate():
    data ={
        
        "id": request.form["id"],
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "seeker_email" : request.form["seeker_email"],
        "seeker_phone_number" : request.form["seeker_phone_number"],
        "apptdate" : request.form["apptdate"],
        "appttime" : request.form["appttime"]
    }
    Appointment.update_confirmed_appts_provider(data)
    return redirect ("/provider/dashboard")

@app.route("/dashboard/provider/delete", methods = ['POST'])
def deleteproviderdashappt():
    data = {
        "id": request.form["id"]
    }
    Appointment.delete_appointments(data)
    return redirect("/provider/dashboard")

@app.route('/provider/unconfirmed')
def providerunconfirmedappt():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("providerunconfirmed.html", user_card = User.get_users_by_email(data), unconfirmed_appointment = Appointment.show_unconfirmed_appts_provider(data))

@app.route("/provider/unconfirmed/update", methods = ['POST'])
def providunconfirmupdate():
    data ={
        
        "id": request.form["id"],
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "seeker_email" : request.form["seeker_email"],
        "seeker_phone_number" : request.form["seeker_phone_number"],
        "apptdate" : request.form["apptdate"],
        "appttime" : request.form["appttime"]
    }
    Appointment.update_unconfirmed_appts_provider(data)
    return redirect ("/provider/unconfirmed")

@app.route("/unconfirmed/provider/delete", methods = ['POST'])
def deleteproviderunconfappt():
    data = {
        "id": request.form["id"]
    }
    Appointment.delete_appointments(data)
    return redirect("/provider/unconfirmed")

@app.route("/provider/requested")
def providerequestedappt():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("providerrequested.html", requested_appointment = Appointment.show_requested_appts_provider(data))

@app.route("/provider/requested/update", methods = ["POST"])
def providerrequestupdate():
    data = {
        "id": request.form["id"],
        "apptdate": request.form["apptdate"],
        "appttime": request.form["appttime"]
    }
    Appointment.update_requested_appts_provider(data)
    return redirect("/provider/requested")

@app.route("/provider/requested/delete", methods = ["POST"])
def providerrequestdelete():
    data = {
        "id": request.form["id"]
    }
    Appointment.delete_appointments(data)
    return redirect("/provider/requested")


@app.route('/provider/profile')
def providerprofile():
    # this is to prevent crashing of page when a user has logged out and tries to use a back button
    # if 'first_name' and 'email' not in session:
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }

    # this is one way to transfer data from the session to the template
    # another way is to called the session in the template itself
    return render_template("providerprofile.html", user_card = User.get_users_by_email(data), business_card = Business.get_provider_hours_by_email(data),
    speciality_card = Speciality.get_speciality_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route('/provider/form')
def providerform():
    data = {
        "email":session["email"]
    }
    return render_template("providerform.html", user_card = User.get_users_by_email(data), business_card = Business.get_provider_hours_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route("/provider/form/add", methods = ['POST'])
def providerformadd():
    data1 = {
        "email" : session ['email'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "phone_number" : request.form['phone_number'],
        "occupation" : request.form['occupation']
    }
    User.update_users_by_email(data1)
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
    # Business.create_provider_hours(data2)
    Business.update_provider_hours_by_email(data2)
    data3 = {
        "male" : True if request.form.get('male') else False,
        "female" : True if request.form.get('female') else False,
        "lgbtq" : True if request.form.get('lgbtq') else False,
        "any_gender" : True if request.form.get('any_gender') else False,
        "physical" : True if request.form.get('physical') else False,
        "mental" : True if request.form.get('mental') else False,
        "financial" : True if request.form.get('financial') else False,
        "any_hardship" : True if request.form.get('any_hardship') else False,
        "citizen" : True if request.form.get('citizen') else False,
        "immigrant" : True if request.form.get('immigrant') else False,
        "refugee": True if request.form.get('refugee') else False,
        "any_status" : True if request.form.get('any_status') else False,
        "user_email": session['email']
    }
    # Speciality.create_speciality(data3)
    Speciality.update_speciality_by_email(data3)
    data4 = {
        "house_number" : request.form['house_number'],
        "street_name" : request.form['street_name'],
        "suite_number" :request.form['suite_number'],
        "city_name" : request.form['city_name'],
        "state" : request.form['state'],
        "zip_code" : request.form ['zip_code'],
        "user_email" : session['email']
    }
    # Address.create_address(data4)
    Address.update_address_by_email(data4)
    return redirect("/provider/profile")

@app.route('/provider/delete', methods = ['POST'])
def providerdelete():
    data ={
        "email": session['email']
    }
    User.delete_provider_user_account(data)
    return redirect('/')

# ---------------------------------------- Patient/Seeker Routes ----------------------------------------

@app.route('/seeker/dashboard')
def seekerdashboard():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("seekerdashboard.html", user_card = User.get_users_by_email(data), seeker_confirmed = Appointment.show_confirmed_appts_seeker(data))

@app.route("/dashboard/seeker/delete", methods = ['POST'])
def deleteseekerdashappt():
    data = {
        "id": request.form["id"]
    }
    Appointment.delete_appointments(data)
    return redirect("/seeker/dashboard")

@app.route('/seeker/selectedproviders')
def seekerselectprovider():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("selectedproviders.html", user_card = User.get_users_by_email(data), seeker_speciality = Speciality.get_speciality_by_email(data), provider_speciality = Speciality.get_providers_with_speciality())

@app.route('/seeker/requesting', methods = ['POST'])
def seekerrequesting():
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "seeker_email" : request.form["seeker_email"],
        "seeker_phone_number" : request.form["seeker_phone_number"],
        "apptdate" : date.today(),
        "appttime" : 0,
        "confirmed" : 0,
        "requested" : 1,
        "email" : request.form['user_email']
    }
    Appointment.create_appts(data)
    return redirect ("/seeker/requested")

@app.route('/seeker/requested')
def seekerrequested():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("seekerrequested.html", seeker_requested = Appointment.show_requested_appts_seeker(data))

@app.route("/requested/seeker/delete", methods = ['POST'])
def deleteseekerreqappt():
    data = {
        "id": request.form["id"]
    }
    Appointment.delete_appointments(data)
    return redirect("/seeker/requested")

@app.route('/seeker/unconfirmed')
def seekerunconfirmedappt():
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }
    return render_template("seekerunconfirmed.html", user_card = User.get_users_by_email(data), seeker_unconfirmed = Appointment.show_unconfirmed_appts_seeker(data))

@app.route("/unconfirmed/seeker/delete", methods = ['POST'])
def deleteseekerunconfappt():
    data = {
        "id": request.form["id"]
    }
    Appointment.delete_appointments(data)
    return redirect("/seeker/unconfirmed")

@app.route("/unconfirmed/seeker/confirm", methods = ['POST'])
def confirmseekerunconfappt():
    data = {
        "id": request.form["id"],
        "confirmed": 1
    }
    Appointment.confirm_unconfirmed_appts_seeker(data)
    return redirect("/seeker/unconfirmed")

@app.route('/seeker/profile')
def seekerprofile():
    # this is to prevent crashing of page when a user has logged out and tries to use a back button
    # if 'first_name' and 'email' not in session:
    if 'email' not in session:
        return redirect('/')
    data = {
        "email": session["email"]
    }

    # this is one way to transfer data from the session to the template
    # another way is to called the session in the template itself
    return render_template("seekerprofile.html", user_card = User.get_users_by_email(data),
    speciality_card = Speciality.get_speciality_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route('/seeker/form')
def seekerform():
    data = {
        "email":session["email"]
    }
    return render_template("seekerform.html", user_card = User.get_users_by_email(data), speciality_card = Speciality.get_speciality_by_email(data), address_card = Address.get_provider_address_by_email(data))

@app.route("/seeker/form/add", methods = ['POST'])
def seekerformadd():
    data1 = {
        "email" : session ['email'],
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "phone_number" : request.form['phone_number'],
        "occupation" : request.form['occupation']
    }
    User.update_users_by_email(data1)
    data3 = {
        "male" : True if request.form.get('male') else False,
        "female" : True if request.form.get('female') else False,
        "lgbtq" : True if request.form.get('lgbtq') else False,
        "any_gender" : True if request.form.get('any_gender') else False,
        "physical" : True if request.form.get('physical') else False,
        "mental" : True if request.form.get('mental') else False,
        "financial" : True if request.form.get('financial') else False,
        "any_hardship" : True if request.form.get('any_hardship') else False,
        "citizen" : True if request.form.get('citizen') else False,
        "immigrant" : True if request.form.get('immigrant') else False,
        "refugee": True if request.form.get('refugee') else False,
        "any_status" : True if request.form.get('any_status') else False,
        "user_email": session['email']
    }
    Speciality.update_speciality_by_email(data3)
    # Speciality.update_speciality_by_email(data3)
    data4 = {
        "city_name" : request.form['city_name'],
        "state" : request.form['state'],
        "zip_code" : request.form ['zip_code'],
        "user_email" : session['email']
    }
    Address.update_address_by_email(data4)
    # Address.update_seeker_address_by_email(data4)
    return redirect("/seeker/profile")

@app.route('/seeker/delete', methods = ['POST'])
def seekerdelete():
    data ={
        "email": session['email']
    }
    User.delete_seeker_user_account(data)
    return redirect('/')

# ---------------------------------------- Cancel Appt ----------------------------------------







