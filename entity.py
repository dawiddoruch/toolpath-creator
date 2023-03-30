from point import Point

CAD_ROUND_OFF = 5
CAD_LINE = 'LINE'
CAD_CIRCLE = 'CIRCLE'


class Entity:
    def __init__(self, name, x1, y1, x2=0, y2=0, cx=0, cy=0):
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.c = Point(cx, cy)
        self.name = name
        self.direction = "CW"  # only used for ARCs for now

    # swap points P1 and P2 - mainly for ARCs, so we don't need to lift the tool and skip to the next point
    def swap_points(self, force_direction=""):
        temp_p1 = self.p1
        self.p1 = self.p2
        self.p2 = temp_p1
        if force_direction != "":
            self.direction = force_direction
            return
        if self.direction == "CW":
            self.direction = "CCW"
        else:
            self.direction = "CW"

    # Returns Entity class for LINE or CIRCLE model entity
    @classmethod
    def create_entity(cls, model_entity):
        name = model_entity.dxftype()
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        cx = 0
        cy = 0
        entities = []

        if name == 'CIRCLE':
            x1 = round(model_entity.dxf.center.x, CAD_ROUND_OFF)
            y1 = round(model_entity.dxf.center.y, CAD_ROUND_OFF)
            entities.append(cls(name, x1, y1))
        elif name == 'LINE':
            x1 = round(model_entity.dxf.start.x, CAD_ROUND_OFF)
            y1 = round(model_entity.dxf.start.y, CAD_ROUND_OFF)
            x2 = round(model_entity.dxf.end.x, CAD_ROUND_OFF)
            y2 = round(model_entity.dxf.end.y, CAD_ROUND_OFF)
            entities.append(cls(name, x1, y1, x2, y2))
        elif name == "ARC":
            cx = round(model_entity.dxf.center.x, CAD_ROUND_OFF)
            cy = round(model_entity.dxf.center.y, CAD_ROUND_OFF)
            x1 = round(model_entity.start_point.x, CAD_ROUND_OFF)
            y1 = round(model_entity.start_point.y, CAD_ROUND_OFF)
            x2 = round(model_entity.end_point.x, CAD_ROUND_OFF)
            y2 = round(model_entity.end_point.y, CAD_ROUND_OFF)
            entities.append(cls(name, x1, y1, x2, y2, cx, cy))
        elif name == "LWPOLYLINE":
            points = model_entity.get_points()
            first = True
            prev_bulge = 0
            for p in points:
                # print(p)
                if first:
                    x2 = p[0]
                    y2 = p[1]
                    prev_bulge = p[4]
                    first = False
                    continue
                x1 = x2
                y1 = y2
                x2 = p[0]
                y2 = p[1]
                if p[4] == 0 or prev_bulge == 0:
                    entities.append(cls("LINE", x1, y1, x2, y2))
                # for now, we are skipping bulges as it involves some math I don't have time for
                prev_bulge = p[4]

        return entities

    # Entity distance from a point
    def distance(self, point: Point):
        if self.name == 'CIRCLE':
            return self.p1.distance(point)
        elif self.name in ['LINE', 'ARC']:
            return min(self.p1.distance(point), self.p2.distance(point))

    # Checks if either point p1 or p2 is within radius of point (x,y)
    def has_point(self, p: Point, radius=0.01):
        if self.p1.belongs_to(p, radius):
            return True

        if self.name == 'CIRCLE':
            return False

        if self.p2.belongs_to(p, radius):
            return True

        return False

    def print(self, txt=""):
        if self.name == 'CIRCLE':
            print("ENTITY {} ({}, {})".format(self.name, self.p1.x, self.p1.y))
        elif self.name == 'LINE':
            print("ENTITY {} ({}, {}) to ({}, {})".format(self.name, self.p1.x, self.p1.y, self.p2.x, self.p2.y))
        elif self.name == 'ARC':
            print("ENTITY ARC")
