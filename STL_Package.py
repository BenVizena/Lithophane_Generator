######################
#
# TODO: Unit testing
#
######################

import numpy as np

class Vertex:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_vertex(self):
        return [self.x, self.y, self.z]

    def get_vertex_string(self):
        return "vertex   " + float(self.x) + " " + float(self.y) + " " + float(self.z) + "\n


class Facet:

    def __init__(self, vertex1, vertex2, vertex3):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.vertex3 = vertex3
        self.normal = self.get_normal()

    def get_normal(self):
        return np.cross(np.cross(self.vertex1, self.vertex2), self.vertex3)

    def get_normal_string(self):
        return "      " + str(self.normal[0]) + " " + str(self.normal[1]) + " " + str(self.normal[2] + "\n")

    def get_facet_string(self):
        return "  facet normal " + self.get_normal_string() +
            "    outer loop\n" +
            self.vertex1.get_vertex_string() +
            self.vertex2.get_vertex_string() +
            self.vertex3.get_vertex_string() +
            "    endloop\n" +
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

        
