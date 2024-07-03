import psycopg2
from flask import url_for

# Decision was made to not use a Model Framework like SQL alchemy to keep flexibility and meet IVOA standards
# I hope, I won't regret this


class Model:
    @staticmethod
    def connect():
        # I am disgusted by this
        connection = psycopg2.connect(dbname="spherinator", user="postgres", host='localhost', password="admin")
        cursor = connection.cursor()
        return connection, cursor

    @staticmethod
    def select(query, connection, cursor):
        assert query.startswith(cursor.mogrify('SELECT *'))
        cursor.execute(query)
        result = [ record for record in cursor]
        connection.close()
        cursor.close()
        return result

    def to_json(self):
        pass


class Survey(Model):
    def __init__(self, id, name, description, max_order, hierarchy):
        self.id = id
        self.name = name
        self.description = description
        self.max_order = max_order
        self.hierarchy = hierarchy

    def survey_url(self):
        return url_for('.static', filename='surveys/'+self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'max_order': self.max_order,
            'hierarchy': self.hierarchy,
            'survey_url': self.survey_url()
        }

    @classmethod
    def select_by_name(cls, survey_name):
        conn, cur = Survey.connect()
        q = cur.mogrify("SELECT * FROM survey WHERE name = %s;", (survey_name, ))
        sid, name, description, max_order, hierarchy = Survey.select(q, conn, cur)[0]
        survey = cls(sid, name, description, max_order, hierarchy)
        return survey

    @classmethod
    def select_by_id(cls, survey_id):
        conn, cur = Survey.connect()
        q = cur.mogrify("SELECT * FROM survey WHERE id = %s;", (survey_id, ))
        sid, name, description, max_order, hierarchy = Survey.select(q, conn, cur)[0]
        survey = cls(sid, name, description, max_order, hierarchy)
        return survey

    @classmethod
    def select_all(cls):
        conn, cur = Survey.connect()
        rows = Survey.select(cur.mogrify("SELECT * FROM survey"), conn, cur)
        surveys = [ cls(sid, name, description, max_order, hierarchy) for sid, name, description, max_order, hierarchy in rows ]
        return surveys
