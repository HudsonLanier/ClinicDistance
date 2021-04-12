import heapq

from getcoords import geocoord_patient_dict, geocoord_clinic_dict
from haversine import haversine
#import pandas
from heapq import nsmallest

test_person = geocoord_patient_dict[0]
# test_person2= geocoord_patient_list[1]
# test_person3 = geocoord_patient_list[2]

# def get_candidates(person, list_of_clinics):
#     dict_of_distances = {}
#     final_candidates = {}
#
#     for clinic in list_of_clinics:
#         person_coordinates = person['geo_code']
#         clinic_coordinates = clinic['geo_code']
#         distance = haversine(person_coordinates, clinic_coordinates)
#         dict_of_distances[clinic[1]] = distance
#         candidates = nsmallest(5, dict_of_distances.values())
#
#
#     key_list = list(dict_of_distances.keys())
#     value_list = list(dict_of_distances.values())
#
#     for a_distance in candidates:
#         index_num = value_list.index(a_distance)
#         final_candidates[key_list[index_num]] = a_distance
#
#     person['candidates_list'] = final_candidates


def get_candidates(person, list_of_clinics):
    person['distance_list'] = []
    person['candidates'] = []
    for clinic in list_of_clinics:
        person_coordinates = person['geo_code']
        clinic_coordinates = clinic['geo_code']
        distance = haversine(person_coordinates, clinic_coordinates)
        clinic['distance'] = distance
        person['distance_list'].append(distance)

        #five_closest = nsmallest(5, list_of_distances)
        #five_closest = nsmallest(5, person['distance_list']['distance'])
    #list_of_distances = [item['distance'] for item in list_of_clinics]
    person['smallest_distances'] = nsmallest(5, person['distance_list'])


    for selection in list_of_clinics:
        for pick in person['smallest_distances']:
            if pick == selection['distance']:
                candidate_copy = selection.copy()
                person['candidates'].append(candidate_copy)
            else:
                pass

    #return person['candidates']










def get_everyone_candidates(people_list, clinic_list):
    for person in people_list:
        get_candidates(person, clinic_list)

get_everyone_candidates(geocoord_patient_dict, geocoord_clinic_dict)






