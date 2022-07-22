from flask_app.config.mysqlconnection import connectToMySQL

class Speciality:
    def __init__(self, data):
        self.id = data ['id']
        self.male = data['male']
        self.female = data['female']
        self.lgbtq = data['lgbtq']
        self.gender_other = data['gender_other']
        self.physical = data['physical']
        self.mental = data['mental']
        self.financial = data['financial']
        self.hardship_other = data['hardship_other']
        self.citizen = data['citizen']
        self.immigrant = data['immigrant']
        self.refugee = data['refugee']
        self.status_other = data['status_other']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_email = data['user_email']

    @classmethod
    def get_provider_speciality_by_email(cls, data):
        query = "SELECT * FROM specialities WHERE user_email = %(email)s;"
        results = connectToMySQL ('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def update_provider_speciality_by_email(cls, data):
        query = "UPDATE specialities SET male = %(male)s, female = %(female)s, lgbtq = %(lgbtq)s, gender_other = %(gender_other)s, physical = %(physical)s, mental = %(mental)s, financial = %(financial)s, hardship_other = %(hardship_other)s, citizen = %(citizen)s, immigrant = %(immigrant)s, refugee = %(refugee)s, status_other = %(status_other)s, created_at = NOW(), updated_at = NOW() WHERE user_email = %(user_email)s"
        return connectToMySQL('helping_hand_schema').query_db(query, data)

    @classmethod
    def get_seeker_speciality_by_email(cls, data):
        query = "SELECT * FROM specialities WHERE user_email = %(email)s;"
        results = connectToMySQL ('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def update_seeker_speciality_by_email(cls, data):
        query = "UPDATE specialities SET male = %(male)s, female = %(female)s, lgbtq = %(lgbtq)s, gender_other = %(gender_other)s, physical = %(physical)s, mental = %(mental)s, financial = %(financial)s, hardship_other = %(hardship_other)s, citizen = %(citizen)s, immigrant = %(immigrant)s, refugee = %(refugee)s, status_other = %(status_other)s, created_at = NOW(), updated_at = NOW() WHERE user_email = %(user_email)s"
        return connectToMySQL('helping_hand_schema').query_db(query, data)