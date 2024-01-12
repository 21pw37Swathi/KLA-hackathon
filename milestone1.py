import re
import math

test1 = "C:\\Users\\sanji\\Desktop\\KLA\\Testcase3.txt"  
with open(test1, 'r') as file:
    data = file.read()

def generate_points(wafer_diameter, num_points, angle_deg):
    inclination_angle = math.radians(angle_deg)

    points = []
    for i in range(num_points):
    
        x = i * wafer_diameter / (num_points - 1) - wafer_diameter / 2
        y = 0

        rotated_x = x * math.cos(inclination_angle) - y * math.sin(inclination_angle)
        rotated_y = x * math.sin(inclination_angle) + y * math.cos(inclination_angle)

        points.append(( rotated_x, rotated_y))

    return points

wafer_diameter = int(re.search(r'WaferDiameter:(\d+)', data).group(1))
radius = wafer_diameter / 2
num_points = int(re.search(r'NumberOfPoints:(\d+)', data).group(1))
angle = int(re.search(r'Angle:(\d+)', data).group(1))

result = generate_points(wafer_diameter, num_points, angle)

for point in result:
    print(f"({point[0]}, {point[1]})")

outfile = "C:\\Users\\sanji\\Desktop\\KLA\\output3.txt"

with open(outfile, "w") as output_file:
    for point in result:
        output_file.write(f"({point[0]}, {point[1]})\n")