from flask_app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('logincreate.html')

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