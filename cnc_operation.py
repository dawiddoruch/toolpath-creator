from cnctool import CNCTool
from entity import Entity
from point import Point
from colortable import *


class CNCOperation:
    def __init__(self, entity_name, entity_color, tool: CNCTool):
        self.entity_name = entity_name
        self.entity_color = entity_color
        self.current_entity = 0
        self.entity_list = []
        self.tool = tool
        self.current_entity_index = -1
        self.last_operation = False

    def is_empty(self):
        if len(self.entity_list) == 0:
            return True
        return False

    def get_header(self):
        s = "({0}, {1}, T# {2}, Spindle {3}, Depth {4}, Retract {5})".format(
            self.entity_name, self.entity_color_name(), self.tool.tool_number, self.tool.spindle_speed,
            self.tool.plunge_z, self.tool.retract_z)
        return s

    def entity_color_name(self):
        if self.entity_color is ACAD_BLACK:
            return "BLACK"
        elif self.entity_color is ACAD_RED:
            return "RED"
        elif self.entity_color is ACAD_YELLOW:
            return "YELLOW"
        elif self.entity_color is ACAD_GREEN:
            return "GREEN"
        elif self.entity_color is ACAD_CYAN:
            return "CYAN"
        elif self.entity_color is ACAD_BLUE:
            return "BLUE"
        elif self.entity_color is ACAD_PURPLE:
            return "PURPLE"
        elif self.entity_color is ACAD_MAGENTA:
            return "MAGENTA"
        elif self.entity_color is ACAD_WHITE:
            return "WHITE"
        else:
            return "Color {0}".format(self.entity_color)

    # Finds entity that is the closest to a given point
    def find_closest_entity(self, point: Point):
        index = -1
        dst = -1

        for e in self.entity_list:
            entity_distance = e.distance(point)
            if entity_distance < dst or dst == -1:
                dst = entity_distance
                index = self.entity_list.index(e)

        if index != -1:
            self.current_entity_index = index
            return True
        return False

    # Loads entities from modelspace
    def load_entities(self, msc):
        query_entity_name = self.entity_name
        if query_entity_name == "LINE":
            query_entity_name = "LINE ARC LWPOLYLINE"

        query_string = '{0}[color=={1}]'.format(query_entity_name, self.entity_color)
        print(query_string)

        result = msc.query(query_string)
        for r in result:
            entities = Entity.create_entity(r)
            for e in entities:
                self.entity_list.append(e)

        # for x in self.entity_list:
        #    x.print()

        if 0 == len(self.entity_list):
            return False
        return True
