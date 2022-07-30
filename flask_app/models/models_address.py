from flask_app.config.mysqlconnection import connectToMySQL

class Address:
    def __init__(self,data):
        self.house_number = data['house_number']
        self.street_name = data ['street_name']
        self.suite_number = data['suite_number']
        self.city_name = data['city_name']
        self.state = data['state']
        self.zip_code = data['zip_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_email = data['user_email']

    @classmethod
    def get_provider_address_by_email(cls, data):
        query = "SELECT * FROM work_address WHERE user_email = %(email)s;"
        results = connectToMySQL ('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    # @classmethod
    # def create_address(cls,data):
    #     query = "INSERT INTO work_address (house_number, street_name, suite_number, city_name, state, zip_code, created_at, updated_at, user_email) VALUES (%(house_number)s, %(street_name)s, %(suite_number)s, %(city_name)s, %(state)s, %(zip_code)s, NOW(), NOW(), %(user_email)s);"
    #     return connectToMySQL('helping_hand_schema').query_db(query,data)

    @classmethod
    def update_address_by_email(cls, data):
        query = "UPDATE work_address SET house_number = %(house_number)s, street_name = %(street_name)s, suite_number = %(suite_number)s, city_name = %(city_name)s, state = %(state)s, zip_code = %(zip_code)s,  created_at = NOW(),  updated_at = NOW() WHERE user_email = %(user_email)s"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    
    @classmethod
    def get_seeker_address_by_email(cls, data):
        query = "SELECT * FROM work_address WHERE user_email = %(email)s;"
        results = connectToMySQL ('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False

    # @classmethod
    # def update_seeker_address_by_email(cls, data):
    #     query = "UPDATE work_address SET city_name = %(city_name)s, state = %(state)s, zip_code = %(zip_code)s,  created_at = NOW(),  updated_at = NOW() WHERE user_email = %(user_email)s"
    #     return connectToMySQL('helping_hand_schema').query_db(query, data)