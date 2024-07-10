import psycopg2
from flask import url_for
import yaml
import os

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

    @classmethod
    def create(cls, record):
        pass

    def to_json(self):
        pass


class Survey(Model):
    def __init__(self, id, name, description, max_order, hierarchy):
        self.id = id
        self.name = name
        self.description = description
        self.max_order = max_order
        self.hierarchy = hierarchy

        aspects = yaml.load(open(os.path.join(self.survey_path(), 'data_cube', 'data_aspects.yaml'), 'r'), yaml.Loader)
        self.data_aspects = aspects['data_aspects']

    def survey_path(self):
        return os.path.join('services', 'spherinator', 'static', 'surveys', self.name)

    def survey_url(self):
        return os.path.join('/service', 'spherinator', 'static', 'surveys', self.name)

    def cube_url(self):
        return os.path.join(self.survey_url(), 'data_cube')



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
    def create(cls, record):
        sid, name, description, max_order, hierarchy = record
        return cls(sid, name, description, max_order, hierarchy)

    @classmethod
    def select_by_name(cls, survey_name):
        conn, cur = Survey.connect()
        q = cur.mogrify("SELECT * FROM survey WHERE name = %s;", (survey_name, ))
        rec = Survey.select(q, conn, cur)[0]
        return cls.create(rec)

    @classmethod
    def select_by_id(cls, survey_id):
        conn, cur = Survey.connect()
        q = cur.mogrify("SELECT * FROM survey WHERE id = %s;", (survey_id, ))
        rec = Survey.select(q, conn, cur)[0]
        return cls.create(rec)

    @classmethod
    def select_all(cls):
        conn, cur = Survey.connect()
        rows = Survey.select(cur.mogrify("SELECT * FROM survey;"), conn, cur)
        surveys = [ cls.create(rec) for rec in rows ]
        return surveys


class SpherinatorCell(Model):
    def __init__(self, ra, dec, norder, pixel, survey, id, dp_id):
        self.ra = ra
        self.dec = dec
        self.norder = norder
        self.pixel = pixel
        self.survey = survey
        self.id = id
        self.dp_id = dp_id

    def to_json(self):
        return {
            'ra': self.ra,
            'dec': self.dec,
            'norder': self.norder,
            'pixel': self.pixel,
            'survey': self.survey.to_json(),
            'id': self.id,
            'dp_id': self.dp_id
        }

    @classmethod
    def create(cls, record):
        ra, dec, norder, pixel, survey_id, cid, dp_id = record
        survey = Survey.select_by_id(survey_id)
        return cls(ra, dec, norder, pixel, survey, cid, dp_id)

    @classmethod
    def select_by_dp_id(cls, dp_id):
        conn, cur = SpherinatorCell.connect()
        q = cur.mogrify("SELECT * FROM spherinator_cell WHERE dp_id = %s;", (dp_id, ))
        cell = cls.create(SpherinatorCell.select(q, conn, cur)[0])
        return cell

    @classmethod
    def select_by_id(cls, cid):
        conn, cur = SpherinatorCell.connect()
        q = cur.mogrify("SELECT * FROM spherinator_cell WHERE id = %s;", (cid, ))
        cell = cls.create(SpherinatorCell.select(q, conn, cur)[0])
        return cell

    @classmethod
    def select_all(cls):
        conn, cur = SpherinatorCell.connect()
        rows = SpherinatorCell.select(cur.mogrify("SELECT * FROM spherinator_cell;"), conn, cur)
        cells = [ cls.create(rec) for rec in rows ]
        return cells

    @classmethod
    def select_by_healpix(cls, order, pixel):
        conn, cur = SpherinatorCell.connect()
        q = cur.mogrify("SELECT * FROM spherinator_cell WHERE norder = %s AND pixel = %s;", (int(order), int(pixel)))
        res = SpherinatorCell.select(q, conn, cur)
        if len(res) < 1:
            return None
        return cls.create(res[0])


if __name__ == "__main__":
    test_s = Survey(0, 'TNG100-99', '', 3, 1)
    print(test_s.name)
