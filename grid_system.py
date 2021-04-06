from getcoords import geocoord_clinic_list, geocoord_patient_list

#notes: country bounding box canada (-140.99778, 41.6751050889, -52.6480987209, 83.23324)

#sw corner is (41.6751050889, -140.99778)
#ne corner is (83.23324, -52.6480987209)

#sample data set for a 5x5 grid
list_of_points = [(0,4),
                  (1,1),
                  (2,1),
                  (3,4),
                  (0,3),
                  (4,3),
                  (3,2),
                  (.5, .5)]

def define_axis_data(min_x_value, max_x_value, x_step_value, min_y_value, max_y_value, y_step_value):
    x_axis_points = []
    y_axis_points = []
    for number in range(min_x_value, (max_x_value +1), x_step_value):
        x_axis_points.append(number)
    for a_number in range(min_y_value, (max_y_value +1), y_step_value):
        y_axis_points.append(a_number)
    grid_data = {'x_axis_points': x_axis_points,
                'y_axis_points': y_axis_points,
                 'x_step_value': x_step_value,
                 'y_step_value': y_step_value}
    return grid_data

test_grid = define_axis_data(0,4,1, 0,4,1)

def define_points(a_defined_grid):
    list_of_cells = []
    for y_value in a_defined_grid['y_axis_points']:
        for x_value in a_defined_grid['x_axis_points']:
            list_of_cells.append((y_value, x_value))
    return list_of_cells


