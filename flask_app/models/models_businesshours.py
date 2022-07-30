from flask_app.config.mysqlconnection import connectToMySQL

class Business:
    def __init__(self, data):
        self.id = data ['id']
        self.sundayopen = data['sundayopen']
        self.sundayclose = data['sundayclose']
        self.mondayopen = data['mondayopen']
        self.mondayclose = data['mondayclose']
        self.tuesdayopen = data['tuesdayopen']
        self.tuesdayclose = data['tuesdayclose']
        self.wednesdayopen = data['wednesdayopen']
        self.wednesdayclose = data['wednesdayclose']
        self.thursdayopen = data['thursdayopen']
        self.thursdayclose = data['thursdayclose']
        self.fridayopen = data['fridayopen']
        self.fridayclose = data['fridayclose']
        self.saturdayopen = data['saturdayopen']
        self.saturdayclose = data['saturdayclose']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_email = data['user_email']

    @classmethod
    def get_provider_hours_by_email(cls, data):
        query = "SELECT * FROM businesshours WHERE user_email = %(email)s;"
        results = connectToMySQL ('helping_hand_schema').query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def update_provider_hours_by_email(cls, data):
        query = "UPDATE businesshours SET sundayopen = %(sundayopen)s, sundayclose = %(sundayclose)s, mondayopen = %(mondayopen)s, mondayclose = %(mondayclose)s, tuesdayopen = %(tuesdayopen)s, tuesdayclose = %(tuesdayclose)s, wednesdayopen = %(wednesdayopen)s, wednesdayclose = %(wednesdayclose)s, thursdayopen = %(thursdayopen)s, thursdayclose = %(thursdayclose)s, fridayopen = %(fridayopen)s, fridayclose = %(fridayclose)s, saturdayopen = %(saturdayopen)s, saturdayclose = %(saturdayclose)s, updated_at = NOW() WHERE user_email = %(user_email)s;"
        return connectToMySQL('helping_hand_schema').query_db(query, data)