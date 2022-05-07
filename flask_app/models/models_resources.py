from flask_app.config.mysqlconnection import connectToMySQL

class Resource:
    def __init__(self,data):
        self.id = data['id']
        self.facility = data['facility']
        self.street = data['street']
        self.suite = data['suite']
        self.city = data['city']
        self.state = data['state']
        self.zipcode = data['zipcode']
        self.candidate = data['candidate']
        self.work_hours = data['work_hours']
        self.work_days = data['work_days']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

