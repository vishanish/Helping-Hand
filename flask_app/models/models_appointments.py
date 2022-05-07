from flask_app.config.mysqlconnection import connectToMySQL

class Appointment:
    def __init__(self,data):
        self.id = data['id']
        self.date = data['date']
        self.time = data['time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.provider_id = data['provider_id']
        self.user_id = data['user_id']