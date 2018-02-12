######################
#
# TODO:10 Add checking functionality to Solid to make sure that the solid is closed
# TODO:0 Add checking functionality to Solid to make sure that all normals are pointing outwards.
#
######################

import numpy as np


def get_normal(v1, v2, v3):
    non_normalized_normal = np.cross((v2 - v1), (v3 - v1))
    return non_normalized_normal / np.max(abs(non_normalized_normal))

def get_normal_string(v1, v2, v3):
    normal = get_normal(v1, v2, v3)
    return str(normal[0]) + " " + str(normal[1]) + " " + str(normal[2]) + "\n"

def get_vertex_string(x, y, z):
    return "      vertex   " + str(x) + " " + str(y) + " " + str(z) + "\n"

def get_facet_string(v1, v2, v3):
    return "  facet normal " + get_normal_string(v1, v2, v3) + \
        "    outer loop\n" + \
        get_vertex_string(v1[0], v1[1], v1[2]) + \
        get_vertex_string(v2[0], v2[1], v2[2]) + \
        get_vertex_string(v3[0], v3[1], v3[2]) + \
        "    endloop\n" + \
        "  endfacet\n"

def get_solid_header():
    return 'solid ASCII\n'

def get_solid_footer():
    return 'endsolid'

class Vertex:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_vertex(self):
        return [self.x, self.y, self.z]

    def get_vertex_string(self):
        return "      vertex   " + str(self.x) + " " + str(self.y) + " " + str(self.z) + "\n"

    def __sub__(vertex1, vertex2):
        return [vertex1.x - vertex2.x, vertex1.y - vertex2.y, vertex1.z - vertex2.z]

class Facet:

    def __init__(self, vertex1, vertex2, vertex3):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.vertex3 = vertex3
        self.normal = self.get_normal()



    def get_normal(self):
        non_normalized_normal = np.cross((self.vertex2 - self.vertex1), (self.vertex3 - self.vertex1))
        return non_normalized_normal / np.max(abs(non_normalized_normal))

    def get_normal_string(self):
        return str(self.normal[0]) + " " + str(self.normal[1]) + " " + str(self.normal[2]) + "\n"

    def get_facet_string(self):
        return "  facet normal " + self.get_normal_string() + \
            "    outer loop\n" + \
            self.vertex1.get_vertex_string() + \
            self.vertex2.get_vertex_string() + \
            self.vertex3.get_vertex_string() + \
            "    endloop\n" + \
            "  endfacet\n"

class Solid:

    def __init__(self, facet_list):
        self.facet_list = facet_list

    def get_solid_string(self):
        solid_string = "solid ASCII\n"

        for facet in self.facet_list:
            solid_string = solid_string + facet.get_facet_string()

        solid_string = solid_string + "endsolid"

        return solid_string

def test():
    v1 = Vertex(-25,5,30)
    v2 = Vertex(-25,5,0)
    v3 = Vertex(-25,15,30)
    v4 = Vertex(-25,15,0)

    v5 = Vertex(-50, 0, 0)
    v6 = Vertex(-50, 0, 30)
    v7 = Vertex(-50, 15, 0)

    f1 = Facet(v1, v2, v3)
    f2 = Facet(v3, v2, v4)
    f3 = Facet(v5, v6, v7)

    s1 = Solid((f1, f2, f3))
    print(s1.get_solid_string())
