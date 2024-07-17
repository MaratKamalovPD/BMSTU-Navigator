def connection_tuple_to_dict(tuple):
    array = []
    for i in range(len(tuple)):
        connection = {
        "basepoint_1_uuid": tuple[i][0],
        "basepoint_2_uuid": tuple[i][1],
        "weight": tuple[i][2],
        "floor_number": tuple[i][3],
        }
        array.append(connection)
    return array