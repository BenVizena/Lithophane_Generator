import numpy as np
import math
from PIL import Image, ImageFilter
import time
import calendar
import STL_Package



def make_ground_level_vertex_list(x_scale, y_scale, z_vals_of_stl_structures):
    height, width = z_vals_of_stl_structures.shape[0] + 1, z_vals_of_stl_structures.shape[1] + 1
    ground_level_vertex_list = np.asarray([[(x, y, 0) for x in range(width)] for y in range(height)]).astype(np.float32)
    ground_level_vertex_list[:,:,0] *= x_scale
    ground_level_vertex_list[:,:,1] *= y_scale

    #vertex0 = ground_level_vertices[0][0] # top left
    #vertex1 = ground_level_vertices[0][1] # top right
    #vertex2 = ground_level_vertices[1][0] # bottom left
    #vertex3 = ground_level_vertices[1][1] # bottom right

    return ground_level_vertex_list


def scale_z_vals(z_vals_of_stl_structures, scale):
    height, width = z_vals_of_stl_structures.shape

    new_z_vals = np.zeros((int(height / scale), int(width / scale)))

    new_z_val_row = 0
    new_z_val_col = 0



    for row in range(0, height - scale - 1, scale):
        for col in range(0, width - scale - 1, scale):
            avg_height_for_this_block = 0

            for superpixel_Row in range(scale):
                for superpixel_Col in range(scale):
                    avg_height_for_this_block += z_vals_of_stl_structures[row + superpixel_Row, col + superpixel_Col]

            new_z_vals[new_z_val_row, new_z_val_col] = int(avg_height_for_this_block / (scale * scale))
            avg_height_for_this_block = 0
            new_z_val_col += 1
        new_z_val_row += 1
        new_z_val_col = 0

    return new_z_vals

def generate_lithophane(x_mm, y_mm, z_vals_of_stl_structures):
    filename = "lithophane_" + str(calendar.timegm(time.gmtime())) + ".stl"

    z_vals_of_stl_structures = scale_z_vals(z_vals_of_stl_structures, 5)

    height, width = z_vals_of_stl_structures.shape
    x_scale, y_scale = x_mm / z_vals_of_stl_structures.shape[1], y_mm / z_vals_of_stl_structures.shape[0]
    ground_level_vertices = make_ground_level_vertex_list(x_scale, y_scale, z_vals_of_stl_structures)
    # ground_level_vertices is indexed [height, width], so the top left vertex is at 0,0 and the bottom left pixel is at [max, 0]


    with open(filename, 'a') as litho_file:
        litho_file.write(STL_Package.get_solid_header())

        for row in range(height - 1):
            for col in range(width - 1):
                v0 = ground_level_vertices[row, col] # top left
                v1 = ground_level_vertices[row, col + 1] # top right
                v2 = ground_level_vertices[row + 1, col] # bottom left
                v3 = ground_level_vertices[row + 1, col + 1] # bottom right

                v4 = v0 + [0, 0, z_vals_of_stl_structures[row, col] + 2] # top left
                v5 = v1 + [0, 0, z_vals_of_stl_structures[row, col] + 2] # top right
                v6 = v2 + [0, 0, z_vals_of_stl_structures[row, col] + 2] # bottom left
                v7 = v3 + [0, 0, z_vals_of_stl_structures[row, col] + 2] # bottom right

                litho_file.write(STL_Package.get_facet_string(v0, v3, v7)) # good
                litho_file.write(STL_Package.get_facet_string(v0, v7, v4)) # good

                litho_file.write(STL_Package.get_facet_string(v1, v2, v3)) # facet 1 of face 2
                litho_file.write(STL_Package.get_facet_string(v1, v3, v0)) # etc

                litho_file.write(STL_Package.get_facet_string(v2, v1, v5))
                litho_file.write(STL_Package.get_facet_string(v2, v5, v6))


                litho_file.write(STL_Package.get_facet_string(v3, v2, v6))
                litho_file.write(STL_Package.get_facet_string(v3, v6, v7))

                litho_file.write(STL_Package.get_facet_string(v0, v4, v5))
                litho_file.write(STL_Package.get_facet_string(v0, v5, v1))

                litho_file.write(STL_Package.get_facet_string(v7, v6, v5))
    #            litho_file.write(STL_Package.get_facet_string(v7, v5, v4))
                litho_file.write(STL_Package.get_facet_string(v4, v5, v6))# was 4 5 7
            print('row: ' + str(row))

        litho_file.write(STL_Package.get_solid_footer())

        #    print(str(v1) + " " + str(v5))



    #print(ground_level_vertices[1][1])
    #print(ground_level_vertices[1][1][0])



if __name__ == '__main__':
    input_image = np.asarray(Image.open("C:/Users/benvi/Desktop/Lithophane_Generator/Lenna.png").convert('LA'))

    pixel_intensities = np.array(np.copy(input_image))
    # make the darkest parts of the image into the tallest parts of the lithophane.

    heights_of_stl_structures = (pixel_intensities[:,:,0].astype(np.int) - 255) * -1

    spoof_x_mm = 100
    spoof_y_mm = 100

    generate_lithophane(spoof_x_mm, spoof_y_mm, heights_of_stl_structures)
