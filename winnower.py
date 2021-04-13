from getcoords import geocoord_patient_dict, geocoord_clinic_dict
from haversine import haversine
from heapq import nsmallest

def get_candidates(person, list_of_clinics):
    person['distance_list'] = []
    person['candidates'] = []
    for clinic in list_of_clinics:
        person_coordinates = person['geo_code']
        clinic_coordinates = clinic['geo_code']
        distance = haversine(person_coordinates, clinic_coordinates)
        clinic['distance'] = distance
        person['distance_list'].append(distance)
    person['smallest_distances'] = nsmallest(5, person['distance_list'])

    for selection in list_of_clinics:
        for pick in person['smallest_distances']:
            if pick == selection['distance']:
                candidate_copy = selection.copy()
                person['candidates'].append(candidate_copy)
            else:
                pass


def get_everyone_candidates(people_list, clinic_list):
    for person in people_list:
        get_candidates(person, clinic_list)


get_everyone_candidates(geocoord_patient_dict, geocoord_clinic_dict)






