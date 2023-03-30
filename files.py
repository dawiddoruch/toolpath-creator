import os
from typing import List
import ezdxf
from cnc import CNC
from cnc_operation import CNCOperation


class Files:
    # lists all DXF files in folder
    @staticmethod
    def list_files(source_path):
        files_in_dir = [x for x in os.listdir(source_path) if x.lower().endswith('.dxf')]
        return files_in_dir

    # convert file from DXF to G-CODE
    @staticmethod
    def convert_file(source_path, destination_path, file_name, cnc_operations: List[CNCOperation]):
        print("Converting file '{0}'".format(file_name))

        doc = ezdxf.readfile(source_path + file_name)
        msp = doc.modelspace()

        # Files.test_entities(msp.query("*"))
        # exit()

        last_operation_set = False
        last_operation_index = -1
        total_nonempty_operations = 0

        # iterate operations, load corresponding entities and set the last_operation flag
        for i in range(0, len(cnc_operations)):
            if not cnc_operations[i].load_entities(msp):  # skip empty operations
                continue

            total_nonempty_operations += 1

            if i == len(cnc_operations) - 1:  # check if this is the last operation and set appropriate flag
                cnc_operations[i].last_operation = True
                last_operation_set = True

            last_operation_index = i

        # skip writing anything if no entities are found for any operation
        if total_nonempty_operations == 0:
            print("No operations in file '{0}'".format(file_name))
            return 1

        # if last operation was empty the last_operation won't be set on any of operations so lets address that
        if last_operation_set is False and total_nonempty_operations != 0:
            cnc_operations[last_operation_index].last_operation = True

        # write G-code
        cnc = CNC(destination_path, file_name)
        for operation in cnc_operations:
            if operation.is_empty():
                continue
            cnc.translate(operation)
        cnc.finish()

        return 0

    @staticmethod
    def test_entities(entities):
        for e in entities:
            entity_type = e.dxftype()
            if entity_type == "LINE":
                print(entity_type)
            elif entity_type == "CIRCLE":
                print("{}, center ({}, {}), radius {}".format(entity_type, e.dxf.center.x, e.dxf.center.y,
                                                              e.dxf.radius))
            elif entity_type == "ARC":
                print("{}, center ({}, {}), radius {}".format(entity_type, e.dxf.center.x, e.dxf.center.y,
                                                              e.dxf.radius))
                print("Start: {}, {}".format(e.start_point, e.dxf.start_angle))
                print("End:   {}, {}".format(e.end_point, e.dxf.end_angle))
            elif entity_type == "INSERT":
                print(entity_type)
            elif entity_type == "LWPOLYLINE":
                print("{} points {}".format(entity_type, e.dxf.count))
                points = e.get_points()
                print(points)
            else:
                print("unknown type: {}".format(type))
