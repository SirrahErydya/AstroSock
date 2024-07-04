"""
Save a Spherinator survey project to the data base
"""
import os
from distutils.dir_util import copy_tree
import sys
import math
import csv

import psycopg2

survey_container_path = os.path.join("/home/fenja/AstroSock/AstroSockServer", "services", "spherinator", "static", "surveys")
connection = psycopg2.connect(dbname="spherinator", user="postgres", host='localhost', password="admin")
cursor = connection.cursor()


def create_survey(survey_name, survey_descr, max_order, hierarchy):
    cursor.execute(
        "INSERT INTO survey(name, description, max_order, hierarchy) VALUES(%s, %s, %s, %s);",
        (survey_name, survey_descr, max_order, hierarchy)
    )


def traverse_catalog(survey_name):
    cursor.execute(
        "SELECT id, max_order, hierarchy FROM survey WHERE name = %s;", (survey_name, )
    )
    survey_id, max_order, hierarchy = cursor.fetchone()

    cat_path = os.path.join(survey_container_path, survey_name, 'interaction_catalog')
    for n_order in range(max_order):
        max_pixel = 12 * 4**n_order
        for n_pixel in range(max_pixel):
            dir = str(int(math.floor(n_pixel/10000))*10000)
            tsv_path = os.path.join(cat_path,
                                    "Norder" + str(n_order),
                                    "Dir" + dir,
                                    "Npix" + str(n_pixel) + '.tsv')
            with open(tsv_path, 'r', encoding='utf-8') as catalog:
                tsv_reader = csv.reader(catalog, delimiter='\t')
                next(tsv_reader)
                for row in tsv_reader:
                    query = "INSERT INTO spherinator_cell(ra, dec, norder, pixel, survey, dp_id) VALUES(%s, %s, %s, %s, %s, %s);"
                    dp_id = row[1]
                    if dp_id != "undefined":
                        pixel = n_pixel
                        if hierarchy > 0:
                            pixel = pixel * 4 * hierarchy + int(row[0])
                        cursor.execute(query, [
                            row[2],
                            row[3],
                            n_order + int(hierarchy),
                            pixel,
                            survey_id,
                            dp_id
                        ])






if __name__ == "__main__":
    sname = str(sys.argv[1])
    sdesc = str(sys.argv[2])
    max_order = sys.argv[3]
    hierarchy = sys.argv[4]
    #create_survey(sname, sdesc, max_order, hierarchy)
    traverse_catalog(sname)
    connection.commit()
    cursor.close()
    connection.close()
