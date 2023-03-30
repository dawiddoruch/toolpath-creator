class CNCTool:
    def __init__(self, tool_type="", tool_number=0, spindle_speed=4000, feed_rate=50, plunge_rate=10, plunge_z=6,
                 retract_rate=10, retract_z=7, clearance_z=-1, dust_hood=True):
        self.tool_number = tool_number
        self.spindle_speed = spindle_speed
        self.feed_rate = feed_rate
        self.plunge_rate = plunge_rate
        self.retract_rate = retract_rate
        self.tool_type = tool_type
        self.plunge_z = plunge_z
        self.retract_z = retract_z
        self.clearance_z = clearance_z
        self.canned = False
        self.dust_hood = dust_hood

        if dust_hood:
            self.hood_down = "M96"
            self.hood_up = "M97"
        else:
            self.hood_down = ""
            self.hood_up = ""

        if tool_type == "drill":
            self.canned = True

        if clearance_z == -1:
            self.clearance_z = self.retract_z
