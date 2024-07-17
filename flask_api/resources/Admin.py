from flask_api.resources.db_scripts.db_query import postgresql_select_AllRoomsInTheBuildingAdmin, \
    postgresql_select_AllBasePointsInTheBuildingAdmin, \
    postgresql_select_AllBasePointsConnectionsAdmin, postgresql_select_Floors_by_Building_UuidAdmin
from flask_api.models.Floors_model import floor_tuple_to_dict
from flask_api.models.Connections_model import connection_tuple_to_dict
from flask_api.common.util import is_int_convertible, is_uuid
from flask_api.models.BaseNodes_model import basenode_tuple_to_dict__Admin
from flask_restful import Resource
from flask import Flask, request


class GetAdminDataByBuildingUuid(Resource):
    def __init__(self, **kwargs):
        self.cursor = kwargs['cursor']

    def get(self, building_uuid):
        print(building_uuid)
        str_building_uuid = str(building_uuid)

        self.cursor.execute(postgresql_select_Floors_by_Building_UuidAdmin, (str_building_uuid,))
        floor_record = self.cursor.fetchall()

        self.cursor.execute(postgresql_select_AllRoomsInTheBuildingAdmin, (str_building_uuid,))
        room_record = self.cursor.fetchall()

        self.cursor.execute(postgresql_select_AllBasePointsInTheBuildingAdmin, (str_building_uuid,))
        basenode_record = self.cursor.fetchall()

        self.cursor.execute(postgresql_select_AllBasePointsConnectionsAdmin, (str_building_uuid,))
        connection_record = self.cursor.fetchall()

        room_dict = {}
        basenode_dict = {}
        connection_dict = {}
        floor_dict = {}

        if floor_record != []:
            floor_dict = floor_tuple_to_dict(floor_record)

        if room_record != []:
            room_dict = floor_tuple_to_dict(room_record)

        if basenode_record != []:
            basenode_dict = basenode_tuple_to_dict__Admin(basenode_record)

        if connection_record != []:
            connection_dict = connection_tuple_to_dict(connection_record)




        result = {
        "floors": floor_dict,
        "rooms": room_dict,
        "basenodes": basenode_dict,
        "connections": connection_dict
        }

        return result

class GetAllRoomsAndBasepointsByFloorUuid(Resource):
    def __init__(self, **kwargs):
        self.cursor = kwargs['cursor']

    def get(self):
        floor_uuid = str(request.args.get('floor_uuid'))

        if not is_uuid(floor_uuid):
            return "Bad request", 400

        self.cursor.execute(postgresql_select_AllBasePointsAtTheFloor, (floor_uuid,))
        basepoints_record = self.cursor.fetchall()
        basenode_dict = basenode_tuple_to_dict(basepoints_record)

        self.cursor.execute(postgresql_select_AllRoomsAtTheFloor, (floor_uuid,))
        rooms_record = self.cursor.fetchall()
        rooms_dict = room_tuple_to_dict(rooms_record)

        return {"basenode": basenode_dict,
                "rooms": rooms_dict
                }


class GetAllRoomsAndBasepointsByBuildingUuidAndFloorNumber(Resource):
    def __init__(self, **kwargs):
        self.cursor = kwargs['cursor']

    def get(self):
        floor_number = str(request.args.get('floor_number'))
        building_uuid = str(request.args.get('building_uuid'))

        if (not is_int_convertible(building_uuid) and not is_int_convertible(floor_number)):
            return "Bad request", 400

        self.cursor.execute(postgresql_select_FloorUuidByBuildingUuidAndFloorNumber, (building_uuid, floor_number,))
        floor_uuid_record = self.cursor.fetchall()
        floor_uuid = floor_uuid_record[0][0]

        self.cursor.execute(postgresql_select_AllBasePointsAtTheFloor, (floor_uuid,))
        basepoints_record = self.cursor.fetchall()
        basenode_dict = basenode_tuple_to_dict(basepoints_record)

        self.cursor.execute(postgresql_select_AllRoomsAtTheFloor, (floor_uuid,))
        rooms_record = self.cursor.fetchall()
        rooms_dict = room_tuple_to_dict(rooms_record)

        return {"basenode": basenode_dict,
                "rooms": rooms_dict}

