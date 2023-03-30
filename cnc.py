from cnc_operation import CNCOperation
from point import Point
from cnctool import CNCTool
from entity import Entity


class CNC:
    def __init__(self, output_path: str, output_file: str):
        nc_filename = output_file.replace(".dxf", ".nc")
        self.program_name = nc_filename.replace(".nc", "")
        self.file_handle = open(output_path + nc_filename, "w")
        self.tool = CNCTool()
        self.position = Point(210, 0)
        self.first_point_after_tool_change = True
        self.write_header()
        self.home_position = Point(200, 80)

    def translate(self, operation: CNCOperation):
        self.write("(----------------------------------------)")
        self.write(operation.get_header())
        self.change_tool(operation.tool)

        while operation.find_closest_entity(self.position):
            e: Entity = operation.entity_list.pop(operation.current_entity_index)

            if operation.entity_name == "CIRCLE":
                self.drill(e)

            elif operation.entity_name in ["LINE", "ARC"]:
                self.rout(e)

        self.operation_finished(operation.last_operation)
        return

    def finish(self):
        self.write_footer()
        self.file_handle.close()

    # After tool change the current position is reset to right bottom edge of the table
    def reset_position(self, x=210, y=0):
        self.position.x = x
        self.position.y = y

    # NC file header
    def write_header(self):
        self.write("%")
        self.write("O0001 ({0})".format(self.program_name))
        self.write("G00 G91 G28 Z0.")
        self.write("G17 G20 G40 G49 G55")
        self.write("G64 G69 G80 G90 G94")
        return

    # NC file footer
    def write_footer(self):
        self.write("%")
        return

    # G code for finished operation
    def operation_finished(self, last_operation=False):
        # cancel canned cycles (for drilling)
        if self.tool.canned:
            self.write("G80")

        # raise retract_z for operations other than drilling
        if self.tool.tool_type != "drill":
            self.write("Z{0} F{1}".format(self.tool.retract_z + 0.25, self.tool.retract_rate))

        self.write("G05.1 Q0")
        self.write("G49")
        self.write("M05")
        self.write(self.tool.hood_up)
        self.write("G00 G91 G28 Z0.")
        self.write("G90")

        # last operation ends with M30
        if last_operation:
            self.write("G00 X{0} Y{1} Z{2}".format(self.home_position.x, self.home_position.y, self.home_position.z))
            self.write("M30")
        else:
            self.write("M01")

    # if spindle speed is 0 then push M05 "spindle stop" command. Otherwise, it's M03 "spindle start"
    def get_spindle_on_command(self):
        if self.tool.spindle_speed == 0:
            return "M05 S{0}".format(self.tool.spindle_speed)
        return "M03 S{0}".format(self.tool.spindle_speed)

    # Change tool and write appropriate g-code to file
    def change_tool(self, tool: CNCTool):
        # tool_change = False
        # if self.tool.tool_number != tool.tool_number:
        #    tool_change = True
        #    self.first_point_after_tool_change = True

        # tool_changed = False
        if self.tool.tool_number != tool.tool_number:
            self.reset_position()
            # tool_changed = True

        self.first_point_after_tool_change = True
        self.tool = tool

        # if tool_change:
        self.write("M06 T{0}".format(self.tool.tool_number))
        self.write("G17 G20 G40 G49 G55")
        self.write("G64 G69 G80 G90 G94")
        self.write("G05.1 Q1 R5")
        self.write("G55")
        self.write(self.get_spindle_on_command())

        return

    # Drill commands for entity
    def drill(self, e: Entity):
        if self.first_point_after_tool_change:
            self.write("G00 X{0} Y{1} {2}".format(e.p1.x, e.p1.y, self.get_spindle_on_command()))

            # return to clearance height between drilling cycles
            if self.tool.clearance_z > self.tool.retract_z:
                self.write("G43 H{0} Z{1} {2}".format(self.tool.tool_number, self.tool.clearance_z, self.tool.hood_down))
                self.write(
                    "G98 G81 Z{0} R{1} F{2}".format(self.tool.plunge_z, self.tool.retract_z, self.tool.plunge_rate))
            # return to retract height between drilling cycles
            else:
                self.write("G43 H{0} Z{1} {2}".format(self.tool.tool_number, self.tool.retract_z, self.tool.hood_down))
                self.write(
                    "G99 G81 Z{0} R{1} F{2}".format(self.tool.plunge_z, self.tool.retract_z, self.tool.plunge_rate))

            self.first_point_after_tool_change = False
        else:
            self.write("X{0} Y{1}".format(e.p1.x, e.p1.y))

        self.position = e.p1
        return

    # Commands for routing/cutting the entity
    def rout(self, e: Entity):
        p1 = e.p1
        p2 = e.p2

        if e.has_point(self.position):
            retract = False
            if not e.p1.belongs_to(self.position):
                p1 = e.p2
                p2 = e.p1
                if e.name == 'ARC':
                    e.swap_points()
        else:
            retract = True
            dst1 = e.p1.distance(self.position)
            dst2 = e.p2.distance(self.position)
            if dst2 < dst1:
                p1 = e.p2
                p2 = e.p1
                if e.name == 'ARC':
                    e.swap_points()

        if self.first_point_after_tool_change:
            self.write("G00 X{0} Y{1} {2}".format(p1.x, p1.y, self.get_spindle_on_command()))
            self.write("G43 H{0} Z{1} {2}".format(self.tool.tool_number, self.tool.retract_z, self.tool.hood_down))
            self.write("G17 G01 Z{0} F{1}".format(self.tool.plunge_z, self.tool.plunge_rate))
            self.first_point_after_tool_change = False
        else:
            if retract:
                self.write("Z{0} F{1}".format(self.tool.retract_z, self.tool.retract_rate))
                self.write("G00 Z{0}".format(self.tool.retract_z + 0.25))
                self.write("X{0} Y{1}".format(p1.x, p1.y))
                self.write("G01 Z{0} F{1}".format(self.tool.plunge_z, self.tool.plunge_rate))

        if e.name == 'LINE':
            self.write("G01 X{0} Y{1} F{2}".format(p2.x, p2.y, self.tool.feed_rate))
        elif e.name == 'ARC':
            command = 'G03'
            i_pos = e.c.x - p1.x
            j_pos = e.c.y - p1.y
            if e.direction == 'CCW':
                command = 'G02'

            self.write("{} X{} Y{} I{} J{} F{}".format(command, p2.x, p2.y, i_pos, j_pos, self.tool.feed_rate))

        self.position = p2
        return

    def retract(self):
        # print('Retract to {0}'.format(self.retract_z))
        return

    def plunge(self):
        # print('Lower to {0}'.format(self.operational_z))
        return

    def write(self, s: str):
        # sprint(s)
        self.file_handle.write(s + "\n")
        return
