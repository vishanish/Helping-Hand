from flask_app.config.mysqlconnection import connectToMySQL

class Appointment:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.seeker_email = data['seeker_email']
        self.seeker_phone_number = data['seeker_phone_number']
        self.apptdate = data['apptdate']
        self.appttime = data['appttime']
        self.confirmed = data['confirmed']
        self.requested = data['requested']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_email = data['user_email']

    @classmethod
    def show_confirmed_appts_provider(cls, data):
        query = "SELECT * FROM appointments WHERE confirmed = 1 AND requested = 0 AND user_email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def create_appt_provider(cls, data):
        query = "INSERT INTO appointments (first_name, last_name, seeker_email, seeker_phone_number, apptdate, appttime, confirmed, requested, created_at, updated_at, user_email) VALUES (%(first_name)s, %(last_name)s, %(seeker_email)s, %(seeker_phone_number)s, %(apptdate)s, %(appttime)s, %(confirmed)s, %(requested)s, NOW(), NOW(), %(email)s);"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def delete_appointments(cls, data):
        query = "DELETE FROM appointments WHERE id = %(id)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)

    @classmethod
    def show_unconfirmed_appts_provider(cls, data):
        query = "SELECT * FROM appointments WHERE confirmed = 0 AND requested = 0 AND user_email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def show_requested_appts_provider(cls, data):
        query = "SELECT * FROM appointments WHERE confirmed = 0 AND requested = 1 AND user_email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def update_requested_appts_provider(cls, data):
        query = "UPDATE appointments SET apptdate = %(apptdate)s, appttime = %(appttime)s, requested = 0, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('helping_hand_schema').query_db(query,data)

    @classmethod
    def update_confirmed_appts_provider(cls, data):
        query = "UPDATE appointments SET first_name = %(first_name)s, last_name = %(last_name)s, seeker_email = %(seeker_email)s, seeker_phone_number = %(seeker_phone_number)s, apptdate = %(apptdate)s, appttime = %(appttime)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL('helping_hand_schema').query_db(query,data)

    @classmethod
    def create_requested_appt_seeker(cls, data):
        query = "INSERT INTO appointments (first_name, last_name, seeker_email, seeker_phone_number, apptdate, appttime, confirmed, requested, created_at, updated_at, user_email) VALUES (%(first_name)s, %(last_name)s, %(seeker_email)s, %(seeker_phone_number)s, %(apptdate)s, %(appttime)s, %(confirmed)s, %(requested)s, NOW(), NOW(), %(user_email)s);"
        return connectToMySQL('helping_hand_schema').query_db(query, data)

    @classmethod
    def show_confirmed_appts_seeker(cls, data):
        query = "SELECT * FROM users JOIN appointments ON users.email = appointments.user_email JOIN work_address ON appointments.user_email = work_address.user_email WHERE appointments.confirmed = 1 AND appointments.requested = 0 AND appointments.seeker_email = %(email)s"
        return connectToMySQL('helping_hand_schema').query_db(query, data)

    @classmethod
    def show_unconfirmed_appts_seeker(cls, data):
        query = "SELECT * FROM users LEFT JOIN appointments ON users.email = appointments.user_email WHERE appointments.confirmed = 0 AND appointments.requested = 0 AND appointments.seeker_email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query,data)

    @classmethod
    def show_requested_appts_seeker(cls, data):
        query = "SELECT * FROM appointments JOIN users ON appointments.user_email = users.email WHERE appointments.confirmed = 0 AND appointments.requested = 1 AND appointments.seeker_email = %(email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)