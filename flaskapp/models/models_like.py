from flaskapp.config.mysqlconnection import connectToMySQL

db = 'pet_boarding_db'

class Like:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.pet_id = data['pet_id']

    @classmethod
    def liked(cls, data):
        query = """
                INSERT INTO likes ( user_id, pet_id )
                VALUES ( %(user_id)s, %(pet_id)s );
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def disliked(cls, data):
        query = """
                DELETE FROM likes
                WHERE pet_id = %(pet_id)s
                AND user_id = %(user_id)s
                """
        return connectToMySQL(db).query_db(query, data)