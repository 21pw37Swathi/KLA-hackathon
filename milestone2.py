import re
import numpy as np
import math

def read_parameters_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    wafer_diameter_match = re.search(r'WaferDiameter:(\d+)', content)
    die_size_match = re.search(r'DieSize:(\d+)x(\d+)', content)
    die_shift_vector_match = re.search(r'DieShiftVector:\(([-\d]+),([-\d]+)\)', content)
    reference_die_match = re.search(r'ReferenceDie:\(([-\d]+),([-\d]+)\)', content)

    wafer_diameter = int(wafer_diameter_match.group(1))
    die_width, die_height = map(int, die_size_match.groups())
    die_shift_vector = tuple(map(int, die_shift_vector_match.groups()))
    reference_die = tuple(map(int, reference_die_match.groups()))

    return wafer_diameter, (die_width, die_height), die_shift_vector, reference_die

def is_point_inside_circle(point, circle_center, diameter):
    radius = diameter / 2
    distance = math.sqrt((point[0] - circle_center[0])**2 + (point[1] - circle_center[1])**2)
    return distance <= radius

def calculate_die_coordinates(wafer_diameter, die_size, die_shift_vector, reference_die, cow, shift_center):
    radius = wafer_diameter //  2
    die_coordinates = []
    for i in range(0, radius, die_size[0]):
        for j in range(0, radius, die_size[1]):
            new_i = i + (die_size[0]//2) + shift_center[0]
            new_j = j - (die_size[1]//2) + shift_center[1]
            llc_x = i + shift_center[0]
            llc_y = j + shift_center[1]
            if (is_point_inside_circle((llc_x, llc_y), cow, wafer_diameter)):
                die_index = (new_i - reference_die[0], new_j - reference_die[1])
                die_coordinates.append((die_index, (llc_x, llc_y)))
    
    for i in range(0, -1*radius, -1*die_size[0]):
        for j in range(0, -1*radius, -1*die_size[1]):
            new_i = i + (die_size[0]//2) + shift_center[0]
            new_j = j - (die_size[1]//2) + shift_center[1]
            llc_x = i + shift_center[0]
            llc_y = j + shift_center[1]
            if (is_point_inside_circle((llc_x, llc_y), cow, wafer_diameter)):
                die_index = (new_i - reference_die[0], new_j - reference_die[1])
                die_coordinates.append((die_index, (llc_x, llc_y)))
                
    return die_coordinates


            
    #die_coordinates.append((die_index, (die_x, die_y)))

def find_circle_center(diameter):
    center_x = diameter / 2
    center_y = diameter / 2
    return center_x, center_y  

file_path = 'C:\\Users\\sanji\\Desktop\\KLA\\milestone2\\Testcase1.txt'
wafer_diameter, die_size, die_shift_vector, reference_die = read_parameters_from_file(file_path)
cow = find_circle_center(wafer_diameter)
shift_center = die_shift_vector
die_coordinates = calculate_die_coordinates(wafer_diameter, die_size, die_shift_vector, reference_die, cow, shift_center)

print(die_coordinates)
with open('C:\\Users\\sanji\\Desktop\\KLA\\milestone2\\outfile.txt', 'w') as outfile:
    for die_index, coordinates in die_coordinates:
        outfile.write(f"{die_index}: {coordinates}\n")
