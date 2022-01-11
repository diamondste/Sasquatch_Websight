from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user 

class Sight: 

    db = "sasquatch_websighting"
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.date_seen = data['date_seen']
        self.happened = data['happened']
        self.num_sasq = data['num_sasq']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
    

    @classmethod
    def save(cls, data):
        query = "INSERT INTO sights (location, date_seen, happened, num_sasq, user_id) VALUES (%(location)s , %(date_seen)s , %(happened)s, %(num_sasq)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_sights(cls):
        query = "SELECT * FROM sights;"
        results = connectToMySQL(cls.db).query_db(query)
        sights = []
        for row in results:
            print(row['date_seen'])
            sights.append(cls(row))
        return sights
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM sights LEFT JOIN users on sights.user_id = users.id WHERE sights.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE sights SET location = %(location)s, date_seen = %(date_seen)s, happened = %(happened)s, num_sasq = %(num_sasq)s, updated_at = NOW() WHERE id = %(id)s; "
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_user_report(cls):
        query = "SELECT * FROM sights LEFT JOIN users ON sights.user_id = users.id;"
        sights = connectToMySQL(cls.db).query_db(query)
        results = []
        for sight in sights:
            data = { 

                'id': sight['users.id'],
                'first_name': sight['first_name'],
                'last_name': sight['last_name'],
                'email': sight['email'],
                'password': sight['password'],
                'created_at': sight['users.created_at'],
                'updated_at': sight['users.updated_at']
            }
            s = cls(sight)
            s.user = user.User(data)
            results.append(s)
        return results



    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM sights WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_sight(sight):
        is_valid = True
        if sight['location'] == "":
            is_valid = False 
            flash("Please enter a location", "sight")
        if sight['date_seen'] == "":
            is_valid = False 
            flash("Please enter a date", "sight")
        if sight['happened'] == "":
            is_valid = False 
            flash("Please enter what happened", "sight")
        if sight['num_sasq'] == "" :
            is_valid = False 
            flash("You must enter in at least one sasquatch", "sight")
        return is_valid