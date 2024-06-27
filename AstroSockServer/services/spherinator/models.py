import psycopg2

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
        assert query.startswith('SELECT *')
        cursor.execute(query)
        result = [ record for record in cursor]
        connection.close()
        cursor.close()
        return result


class Survey(Model):
    def __init__(self, id, name, description, max_order, hierarchy):
        self.id = id
        self.name = name
        self.description = description
        self.max_order = max_order
        self.hierarchy = hierarchy

    @classmethod
    def select_by_name(cls, survey_name):
        conn, cur = Survey.connect()
        q = cur.mogrify("SELECT * FROM survey WHERE name = %s;", (survey_name, ))
        sid, name, description, max_order, hierarchy = Survey.select(q, conn, cur)[0]
        survey = cls(sid, name, description, max_order, hierarchy)
        return survey

    @classmethod
    def select_all(cls):
        conn, cur = Survey.connect()
        rows = Survey.select("SELECT * FROM survey", conn, cur)
        surveys = [ cls(sid, name, description, max_order, hierarchy) for sid, name, description, max_order, hierarchy in rows ]
        return surveys
