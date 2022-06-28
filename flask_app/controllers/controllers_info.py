from flask_app import app
from flask import redirect, render_template, request, session

# renders the index page
@app.route('/')
def index():
    return render_template('index.html')

# renders the create/login page
@app.route('/registerlogin')
def account():
    # this is to prevent the user from going back to logincreate template when the user is in session
    if 'sfirst_name' and 'semail' in session:
        if (session['sprovider'] == 'provider'):
            return redirect ('/provider')
        elif (session['sprovider'] == 'seeker'):
            return redirect ('/seeker')
        # return redirect('/user/registered')
    return render_template('logincreate.html')

# performs action for the Register user on create/login page
# action route
@app.route('/user/register', methods = ['POST'])
def userregister():
    # request.form gets the data from the form. In this case, the registration form.
    # session is a dictionary
    session['sfirst_name'] = request.form["first_name"]
    session['slast_name'] = request.form["last_name"]
    session['semail'] = request.form["email"]
    session['sprovider'] = request.form['seeker_provider']
    """When the code reaches this step, the data from the form is lost.
        Because of this there is no information that is available on the template in the display action
        To get the data from the form, we need to use session"""
    # when a route has a post method, do not render template on this route. redirect to a different route.
    if(session['sprovider'] == 'provider'):
        return redirect ("/provider")
    elif(session['sprovider'] == 'seeker'):
        return redirect ("/seeker")
    # return redirect('/user/registered')

@app.route('/provider')
def provider():
    # this is to prevent crashing of page when a user has logged out and tries to use a back button
    if 'sfirst_name' and 'semail' not in session:
        return redirect('/')
    # this is one way to transfer data from the session to the template
    # another way is to called the session in the template itself
    return render_template("provider.html", sfirst = session['sfirst_name'])

@app.route('/seeker')
def seeker():
    # this is to prevent crashing of page when a user has logged out and tries to use a back button
    if 'sfirst_name' and 'semail' not in session:
        return redirect('/')
    # this is one way to transfer data from the session to the template
    # another way is to called the session in the template itself
    return render_template("seeker.html", sfirst = session['sfirst_name'])


# session must be cleared when user exit the page
@app.route("/user/logout")
def userlogout():
    # WIP
    session.clear()
    # we can also delete specific data from the session when logging out (del)
    # del session["sfirst_name"]
    return redirect("/")


@app.route('/male')
def male():
    return render_template('info.html')

@app.route('/female')
def female():
    return render_template('info.html')

@app.route('/lgbtq')
def lgbtq():
    return render_template('info.html')

@app.route('/donot')
def donot():
    return render_template('info.html')

@app.route('/physical')
def physical():
    return render_template('info.html')

@app.route('/mental')
def mental():
    return render_template('info.html')

@app.route('/financial')
def financial():
    return render_template('info.html')

@app.route('/other')
def other():
    return render_template('info.html')

@app.route('/citizen')
def citizen():
    return render_template('info.html')

@app.route('/immigrant')
def immigrant():
    return render_template('info.html')

@app.route('/refugee')
def refugee():
    return render_template('info.html')