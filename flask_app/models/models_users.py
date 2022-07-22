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
            'gender_other' : 'None',
            'physical' : 'None',
            'mental' : 'None',
            'financial' : 'None',
            'hardship_other' : 'None',
            'citizen' : 'None',
            'immigrant' : 'None',
            'refugee' : 'None',
            'status_other' : 'None',
            'user_email' : data['email']
        }
        query3 =  "INSERT INTO specialities (male, female, lgbtq, gender_other, physical, mental, financial, hardship_other, citizen, immigrant, refugee, status_other, created_at, updated_at, user_email) VALUES (%(male)s, %(female)s, %(lgbtq)s, %(gender_other)s, %(physical)s, %(mental)s, %(financial)s, %(hardship_other)s, %(citizen)s, %(immigrant)s, %(refugee)s, %(status_other)s, NOW(), NOW(), %(user_email)s);"
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

    # @classmethod
    # def users_by_email(cls, data):
    #     query ='SELECT * FROM users JOIN businesshours ON users.email = businesshours.user_email JOIN specialities ON businesshours.user_email = specialities.user_email JOIN work_address ON specialities.user_email = work_address.user_email WHERE users.email = %(email)s;'
    #     results = connectToMySQL('helping_hand_schema').query_db(query, data)
    #     print('results: ', results)
    #     if results:
    #         return cls(results[0])
    #     return False

    # @classmethod
    # def users_by_id(cls,data):
    #     query = "SELECT * FROM users WHERE id = %(id)s"
    #     results = connectToMySQL('helping_hand_schema').query_db(query, data)
    #     if results:
    #         return cls(results[0])
    #     return False

    @classmethod
    def update_provider_users_by_email(cls, data):
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
        query4 = "DELETE FROM users WHERE email = %(email)s;"
        result4 = connectToMySQL('helping_hand_schema').query_db(query4, data)
        return [result1, result2, result3, result4]

    @classmethod
    def update_seeker_users_by_email(cls, data):
        query =  "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, phone_number = %(phone_number)s, updated_at = NOW() WHERE email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def delete_seeker_user_account(cls,data):
        query2 = "DELETE FROM specialities WHERE user_email = %(email)s;"
        result2 = connectToMySQL('helping_hand_schema').query_db(query2, data)
        query3 = "DELETE FROM work_address WHERE user_email = %(email)s;"
        result3 = connectToMySQL('helping_hand_schema').query_db(query3, data)
        query4 = "DELETE FROM users WHERE email = %(email)s;"
        result4 = connectToMySQL('helping_hand_schema').query_db(query4, data)
        return [result2, result3, result4]

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