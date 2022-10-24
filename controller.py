import sys
from flask import abort
import pymysql as mysql
from config import OPENAPI_AUTOGEN_DIR, DB_HOST, DB_USER, DB_PASSWD, DB_NAME

sys.path.append(OPENAPI_AUTOGEN_DIR)
from swagger_server import models

db = mysql.connect(host=DB_HOST,
                   user=DB_USER,
                   passwd=DB_PASSWD,
                   db=DB_NAME)


def get_basins():
    with db.cursor() as cs:
        cs.execute("SELECT basin_id,ename FROM basin")
        result = [models.BasinShort(basin_id, name) for basin_id, name in cs.fetchall()]
    return result

def get_basin_details(basin_id):
    with db.cursor() as cs:
        cs.execute("""
            SELECT basin_id, ename, area
            FROM basin
            WHERE basin_id=%s
            """, [basin_id])
        result = cs.fetchone()
    if result:
        basin_id, name, area = result
        return models.BasinFull(basin_id, name, area)
    else:
        abort(404)


def get_stations(basin_id):
    with db.cursor() as cs:
        cs.execute("""
            SELECT station_id, s.ename
            FROM station s
            INNER JOIN basin b ON s.basin_id=b.basin_id
            WHERE b.basin_id=%s
            """, [basin_id])
        result = [models.StationShort(station_id, name) for station_id, name in cs.fetchall()]
    return result


def get_station_details(station_id):
    return "Do something"

