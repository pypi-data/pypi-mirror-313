from math import log


KEY_INDEX = 0
RECT_INDEX = 1
CONTENTS_INDEX = 2

POLYGON_KEY = b'p'
LEDGE_KEY = b'l'
NODE_KEY = b'n'
EMPTY_KEY = b'e'


def get_relevant_leaves(tree, offset, is_reversed, left, top, right, bottom):
    x0 = left - offset[0]
    y0 = top - offset[1]
    x1 = right - offset[0]
    y1 = bottom - offset[1]
    if is_reversed:
        x0, x1 = -x1, -x0

    return get_relevant_leaves_from_relative_coordinates(
        tree, offset, is_reversed, x0, y0, x1, y1)


def get_relevant_leaves_from_relative_coordinates(
        tree, offset, is_reversed, x0, y0, x1, y1):
    kind = tree[KEY_INDEX]
    if kind == EMPTY_KEY:
        return

    u0, v0, u1, v1 = tree[RECT_INDEX]
    if u0 > x1 or x0 > u1 or v0 > y1 or y0 > v1:
        return

    if kind == NODE_KEY:
        for child in tree[CONTENTS_INDEX:]:
            yield from get_relevant_leaves_from_relative_coordinates(
                child, offset, is_reversed, x0, y0, x1, y1)
    else:
        yield LeafNode(tree, offset, is_reversed)


class LeafNode(object):
    zone_boundary_polygon = False

    def __init__(self, leaf, offset, is_reversed):
        self.data = leaf
        self.offset = offset
        self.reversed = is_reversed

    def is_ledge(self):
        return self.data[KEY_INDEX] == LEDGE_KEY

    def get_edges(self):
        points = list(self.get_points())
        if len(points) < 2:
            return

        x0, y0 = x1, y1 = points[0]
        for x2, y2 in points[1:]:
            if (x2, y2) == (x1, y1):
                continue
            yield (x1, y1, x2, y2)
            x1, y1 = x2, y2

        if self.data[KEY_INDEX] == POLYGON_KEY:
            # Close the loop
            yield (x2, y2, x0, y0)

    def data_point_to_world(self, point):
        y = self.offset[1] + point[1]
        if self.reversed:
            x = self.offset[0] - point[0]
        else:
            x = self.offset[0] + point[0]
        return (x, y)

    def get_points(self):
        if self.reversed:
            for point in self.data[:CONTENTS_INDEX - 1:-1]:
                yield self.data_point_to_world(point)
        else:
            for point in self.data[CONTENTS_INDEX:]:
                yield self.data_point_to_world(point)


class ZonePolygon(object):
    zone_boundary_polygon = True

    def __init__(self, zone_def):
        self.zone_def = zone_def

        from trosnoth.model.map import MapLayout
        zone_width = MapLayout.zoneBodyWidth + 2 * MapLayout.zoneInterfaceWidth
        self.x0 = zone_def.pos[0] - zone_width // 2
        self.x1 = zone_def.pos[0] - MapLayout.zoneBodyWidth // 2
        self.x2 = zone_def.pos[0] + MapLayout.zoneBodyWidth // 2
        self.x3 = zone_def.pos[0] + zone_width // 2
        self.y0 = zone_def.pos[1] - MapLayout.halfZoneHeight
        self.y1 = zone_def.pos[1]
        self.y2 = zone_def.pos[1] + MapLayout.halfZoneHeight

    def is_ledge(self):
        return False

    def might_overlap_rect(self, x0, y0, x1, y1):
        if x1 < self.x0 or x0 > self.x3 or y1 < self.y0 or y0 > self.y2:
            return False
        return True

    def get_edges(self):
        points = self.get_points()
        x0, y0 = points.pop(0)
        points.append((x0, y0))
        for x1, y1 in points:
            yield x0, y0, x1, y1
            x0 = x1
            y0 = y1

    def get_points(self):
        return [
            (self.x0, self.y1),
            (self.x1, self.y0),
            (self.x2, self.y0),
            (self.x3, self.y1),
            (self.x2, self.y2),
            (self.x1, self.y2),
        ]


def build_map_tree(polygons, oneWayPlatforms):
    '''
    Builds a map tree data structure from the given set of convex polygonal
    obstacles and one-way platforms
    '''
    things = [build_polygon(p) for p in polygons]
    things += [build_one_way_platform(l) for l in oneWayPlatforms]
    return build_binary_tree_from_leaves(things)


def build_binary_tree_from_leaves(things):
    if len(things) < 1:
        return build_empty_node()
    if len(things) == 1:
        return things[0]
    if len(things) == 2:
        return build_tree_node(things)

    # Find the best place to divide the nodes
    # Try dividing on x-axis
    xThings = sorted(
        things, key=lambda thing: rect_centre(thing[RECT_INDEX])[0])
    bestX = None
    bestXCost = None
    for i in range(1, len(things)):
        side1 = build_tree_node(xThings[:i])
        side2 = build_tree_node(xThings[i:])
        cost = rect_area(side1[RECT_INDEX]) * log(i) + rect_area(
            side2[RECT_INDEX]) * log(len(things) - i)
        if bestXCost is None or cost < bestXCost:
            bestXCost = cost
            bestX = i

    # Try dividing on x-axis
    yThings = sorted(
        things, key=lambda thing: rect_centre(thing[RECT_INDEX])[1])
    bestY = None
    bestYCost = None
    for i in range(1, len(things)):
        side1 = build_tree_node(yThings[:i])
        side2 = build_tree_node(yThings[i:])
        cost = rect_area(side1[RECT_INDEX]) * log(i) + rect_area(
            side2[RECT_INDEX]) * log(len(things) - i)
        if bestYCost is None or cost < bestYCost:
            bestYCost = cost
            bestY = i

    # Decide which way to split
    if bestXCost < bestYCost:
        return build_tree_node([
            build_binary_tree_from_leaves(xThings[:bestX]),
            build_binary_tree_from_leaves(xThings[bestX:])])
    return build_tree_node([
        build_binary_tree_from_leaves(yThings[:bestY]),
        build_binary_tree_from_leaves(yThings[bestY:])])


def build_polygon(points):
    return (POLYGON_KEY, bounding_rect_of_points(points)) + tuple(points)


def build_one_way_platform(points):
    return (LEDGE_KEY, bounding_rect_of_points(points)) + tuple(points)


def bounding_rect_of_points(points):
    x0, y0 = x1, y1 = points[0]
    for x, y in points[1:]:
        x0 = min(x0, x)
        y0 = min(y0, y)
        x1 = max(x1, x)
        y1 = max(y1, y)
    return (x0, y0, x1, y1)


def rect_union(rects):
    points = []
    for x0, y0, x1, y1 in rects:
        points.append((x0, y0))
        points.append((x1, y1))
    return bounding_rect_of_points(points)


def rect_centre(rect):
    x0, y0, x1, y1 = rect
    return ((x0 + x1) / 2, (y0 + y1) / 2)


def rect_area(rect):
    x0, y0, x1, y1 = rect
    return (x1 - x0) * (y1 - y0)


def build_tree_node(children):
    children = [child for child in children if child[KEY_INDEX] != EMPTY_KEY]
    if not children:
        return build_empty_node()
    if len(children) == 1:
        return children[0]

    boundingRect = rect_union(child[RECT_INDEX] for child in children)
    return (NODE_KEY, boundingRect) + tuple(children)


def build_empty_node():
    return (EMPTY_KEY,)


BLOCK_TYPE = b't'
SYMMETRICAL = b's'
BLOCKED = b'b'
CONTENTS = b'c'

def pack_block(blockType, symmetrical, blocked, tree):
    return {
        BLOCK_TYPE: blockType,
        SYMMETRICAL: symmetrical,
        BLOCKED: blocked,
        CONTENTS: tree,
    }


class BlockLayout(object):
    def __init__(self, data):
        self.blockType = data[BLOCK_TYPE]
        self.symmetrical = data[SYMMETRICAL]
        self.blocked = data[BLOCKED]
        self.tree = data[CONTENTS]
