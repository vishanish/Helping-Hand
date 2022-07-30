from flask_app.config.mysqlconnection import connectToMySQL

class Speciality:
    def __init__(self, data):
        self.id = data ['id']
        self.male = data['male']
        self.female = data['female']
        self.lgbtq = data['lgbtq']
        self.any_gender = data['any_gender']
        self.physical = data['physical']
        self.mental = data['mental']
        self.financial = data['financial']
        self.any_hardship = data['any_hardship']
        self.citizen = data['citizen']
        self.immigrant = data['immigrant']
        self.refugee = data['refugee']
        self.any_status = data['any_status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_email = data['user_email']

    @classmethod
    def get_speciality_by_email(cls, data):
        query = "SELECT * FROM specialities WHERE user_email = %(email)s;"
        results = connectToMySQL ('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_providers_with_speciality(cls):
        query = "SELECT * FROM users LEFT JOIN specialities ON users.email = specialities.user_email WHERE seekprov = 'provider';"
        return connectToMySQL('helping_hand_schema').query_db(query)

    @classmethod
    def update_speciality_by_email(cls, data):
        query = "UPDATE specialities SET male = %(male)s, female = %(female)s, lgbtq = %(lgbtq)s, any_gender = %(any_gender)s, physical = %(physical)s, mental = %(mental)s, financial = %(financial)s, any_hardship = %(any_hardship)s, citizen = %(citizen)s, immigrant = %(immigrant)s, refugee = %(refugee)s, any_status = %(any_status)s, created_at = NOW(), updated_at = NOW() WHERE user_email = %(user_email)s"
        return connectToMySQL('helping_hand_schema').query_db(query, data)
    

    