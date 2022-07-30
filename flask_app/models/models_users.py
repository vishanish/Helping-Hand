from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_businesshours import Business
from datetime import time as times
from flask_bcrypt import Bcrypt
from flask_app import app
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt(app)

class User:
    def __init__(self,data):
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone_number = data['phone_number']
        self.occupation = data['occupation']
        self.seekprov = data['seekprov']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_reg(cls,data):
        
        pass_hash = bcrypt.generate_password_hash(data['password'])
        user ={
            'first_name': data['first_name'],
            'email': data['email'],
            'seekprov':data['seekprov'],
            'password': pass_hash
        }
        query1 = 'INSERT INTO users(first_name, email, seekprov, password, created_at, updated_at) VALUES (%(first_name)s, %(email)s, %(seekprov)s, %(password)s, NOW(), NOW());'
        result1=connectToMySQL('helping_hand_schema').query_db(query1, user)
        
        time = {
            'sundayopen' : times(),
            'sundayclose' : times(),
            'mondayopen' : times(),
            'mondayclose' : times(),
            'tuesdayopen' : times(),
            'tuesdayclose' : times(),
            'wednesdayopen' : times(),
            'wednesdayclose' :times(),
            'thursdayopen' : times(),
            'thursdayclose' : times(),
            'fridayopen' : times(),
            'fridayclose' : times(),
            'saturdayopen' : times(),
            'saturdayclose' : times(),
            'user_email' : data['email']
        }
        query2 =  "INSERT INTO businesshours (sundayopen, sundayclose, mondayopen, mondayclose, tuesdayopen, tuesdayclose, wednesdayopen, wednesdayclose, thursdayopen, thursdayclose, fridayopen, fridayclose, saturdayopen, saturdayclose, created_at, updated_at, user_email) VALUES (%(sundayopen)s, %(sundayclose)s, %(mondayopen)s, %(mondayclose)s, %(tuesdayopen)s, %(tuesdayclose)s, %(wednesdayopen)s, %(wednesdayclose)s, %(thursdayopen)s, %(thursdayclose)s, %(fridayopen)s, %(fridayclose)s, %(saturdayopen)s, %(saturdayclose)s, NOW(), NOW(), %(user_email)s);"
        result2 = connectToMySQL('helping_hand_schema').query_db(query2, time)
        
        speciality = {
            'male' : 'None',
            'female' : 'None',
            'lgbtq' : 'None',
            'any_gender' : 'None',
            'physical' : 'None',
            'mental' : 'None',
            'financial' : 'None',
            'any_hardship' : 'None',
            'citizen' : 'None',
            'immigrant' : 'None',
            'refugee' : 'None',
            'any_status' : 'None',
            'user_email' : data['email']
        }
        query3 =  "INSERT INTO specialities (male, female, lgbtq, any_gender, physical, mental, financial, any_hardship, citizen, immigrant, refugee, any_status, created_at, updated_at, user_email) VALUES (%(male)s, %(female)s, %(lgbtq)s, %(any_gender)s, %(physical)s, %(mental)s, %(financial)s, %(any_hardship)s, %(citizen)s, %(immigrant)s, %(refugee)s, %(any_status)s, NOW(), NOW(), %(user_email)s);"
        result3 = connectToMySQL('helping_hand_schema').query_db(query3, speciality)

        address = {
            'house_number' : 0,
            'street_name' : 'street',
            'suite_number' : 0,
            'city_name' : 'city',
            'state' : 'ST',
            'zip_code' :0,
            'user_email' : data['email']
        }
        query4 =  "INSERT INTO work_address (house_number, street_name, suite_number, city_name, state, zip_code, created_at, updated_at, user_email) VALUES (%(house_number)s, %(street_name)s, %(suite_number)s, %(city_name)s, %(state)s, %(zip_code)s, NOW(), NOW(), %(user_email)s);"
        result4 = connectToMySQL('helping_hand_schema').query_db(query4, address)
        return [result1, result2, result3, result4]

    @classmethod
    def login_validation(cls, data):
        registered_user = User.get_users_by_email(data)
        if not registered_user:
            flash("Invalid Email/Password")
            return False
        if not bcrypt.check_password_hash(registered_user.password, data['password']):
            flash("Invalid Email/Password")
            return False
        return True

    @classmethod
    def get_users_by_email(cls, data):
        query ='SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def update_users_by_email(cls, data):
        query =  "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, phone_number = %(phone_number)s, occupation = %(occupation)s, updated_at = NOW() WHERE email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)

    @classmethod
    def delete_provider_user_account(cls,data):
        query1 = "DELETE FROM work_address WHERE user_email = %(email)s;"
        result1 = connectToMySQL('helping_hand_schema').query_db(query1, data)
        query2 = "DELETE FROM specialities WHERE user_email = %(email)s;"
        result2 = connectToMySQL('helping_hand_schema').query_db(query2, data)
        query3 = "DELETE FROM businesshours WHERE user_email = %(email)s;"
        result3 = connectToMySQL('helping_hand_schema').query_db(query3, data)
        query4 = "DELETE FROM appointments WHERE user_email = %(email)s;"
        result4 = connectToMySQL('helping_hand_schema').query_db(query4, data)
        query5 = "DELETE FROM users WHERE email = %(email)s;"
        result5 = connectToMySQL('helping_hand_schema').query_db(query5, data)
        return [result1, result2, result3, result4, result5]
    
    @classmethod
    def delete_seeker_user_account(cls,data):
        query1 = "DELETE FROM appointments WHERE user_email = %(email)s;"
        result1 = connectToMySQL('helping_hand_schema').query_db(query1, data)
        query2 = "DELETE FROM specialities WHERE user_email = %(email)s;"
        result2 = connectToMySQL('helping_hand_schema').query_db(query2, data)
        query3 = "DELETE FROM work_address WHERE user_email = %(email)s;"
        result3 = connectToMySQL('helping_hand_schema').query_db(query3, data)
        query4 = "DELETE FROM users WHERE email = %(email)s;"
        result4 = connectToMySQL('helping_hand_schema').query_db(query4, data)
        return [result1, result2, result3, result4]

    @classmethod
    def get_male_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.male = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_female_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.female = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)
    
    @classmethod
    def get_lgbtq_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.lgbtq = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_any_gender_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.any_gender = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_physical_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.physical = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_mental_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.mental = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_financial_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.financial = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)
    
    @classmethod
    def get_any_hardship_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.any_hardship = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_citizen_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.citizen = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)
    
    @classmethod
    def get_immigrant_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.immigrant = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_refugee_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.refugee = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def get_any_status_provider_seeker_homepage(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email LEFT JOIN businesshours ON specialities.user_email = businesshours.user_email LEFT JOIN work_address ON businesshours.user_email = work_address.user_email WHERE users.seekprov = 'provider' AND specialities.any_status = '1'"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash('First name needs to be atleast 3 characters long', 'registration')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Email address is not valid!", 'registration')
            is_valid = False
        if len(data['email']) < 1:
            flash('Email cannot be empty', 'registration')
            is_valid = False
        # if len(data['seekprov']) <1:
        #     flash('Need to select "Provider" or "Client" option', 'registration')
        #     is_valid = False
        if len(data['password']) < 8:
            flash('Password needs to be atleast 8 characters long', 'registration')
            is_valid = False
        elif (data['confirm'] != data['password']):
            flash('Your passwords do not match', 'registration')
            is_valid = False
        return is_valid