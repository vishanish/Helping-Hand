from flask_app.config.mysqlconnection import connectToMySQL

class Appointment:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.seeker_email = data['seeker_email']
        self.seeker_phone_number = data['seeker_phone_number']
        self.apptdate = data['apptdate']
        self.appttime = data['appttime']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_email = data['user_email']

    @classmethod
    def create_appt_provider(cls, data):
        query = "INSERT INTO appointments (first_name, last_name, seeker_email, seeker_phone_number, apptdate, appttime, created_at, updated_at, user_email) VALUES (%(first_name)s, %(last_name)s, %(seeker_email)s, %(seeker_phone_number)s, %(apptdate)s, %(appttime)s, NOW(), NOW(), %(email)s);"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def show_confirmed_appts(cls):
        query = "SELECT * FROM appointments WHERE confirmed = 1;"
        return connectToMySQL('helping_hand_schema').query_db(query)
    
    @classmethod
    def show_unconfirmed_appts(cls):
        query = "SELECT * FROM appointments WHERE confirmed = 0;"
        return connectToMySQL('helping_hand_schema').query_db(query)