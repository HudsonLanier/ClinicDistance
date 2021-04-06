import csv
import networkx as nx
import osmnx as ox
import math
from haversine import haversine, Unit

import folium
import requests
import polyline
import sys


list_of_patients = []
list_of_clinics = []

#open the patient csv and store each patient as a list within the list_of_patients
with open('/home/hudsonlanier/Desktop/testpatients.csv') as patient_data:
    for line in csv.reader(patient_data):
        list_of_patients.append(line)

#open the clinic csv and store each clinic as a list within the list_of_clinics
with open('/home/hudsonlanier/Desktop/testclinics.csv') as clinic_data:
    for line in csv.reader(clinic_data):
        list_of_clinics.append(line)

#this line deletes the first line, which has the names of the fields, and not actual data about patients
del list_of_patients[0]
del list_of_clinics[0]


#this function will not work for both patients and clinics, because both are formatted differently. CLEAN THIS UP
#SO THAT IT WILL RUN AS ONE FUNCTION
def add_geolocation_patients(a_list_of_lists):
    for entity in a_list_of_lists:
        address_string = str(entity[1] + ', ' + entity[4] + ', ' + 'Canada')
        try:
            geolocation = ox.geocoder.geocode(address_string)
            entity.append(geolocation)
        except Exception:
            entity.append('no coordinates yet')

def add_geolocation_clinics(a_list_of_lists):
    for entity in a_list_of_lists:
        address_string = str(entity[2] + ', ' + entity[5] + ', ' + 'Canada')
        try:
            geolocation = ox.geocoder.geocode(address_string)
            entity.append(geolocation)
        except Exception:
            entity.append('failed to get coordinates')


#make a function that gets rid of unit, apartment, suite numbers, and other types of data that are confusing the
#geocoder. If you find more words and phrases that cause a failure, simply add them to the problem_words list
def clean_up_addresses(a_list_of_lists):
    problem_words = ['UNIT', 'SUITE', 'ROOM', 'FLOOR', 'APT', 'APARTMENT','ETAGE' 'BUREAU']
    for entity in a_list_of_lists:
        address_string = entity[1]
        if any(x in address_string for x in problem_words):
            #break the string into a list, remove from the problem word to the end, return the corrected address
            address_list = address_string.split()
            for problem_word in problem_words:
                if problem_word in address_list:
                    problem_word_index = address_list.index(problem_word)
                    new_address_list = address_list[:problem_word_index]
                    new_address_string = str(new_address_list)
                    entity[1] = new_address_string

        else:
            pass


#make a function that takes a person as an argument and
# rules out clinics that are obviously too far away for consideration
def ignore_if_too_far(a_person):
    person_postal_code_first_letter = a_person[2][0].upper()
    person_fsa_first_letter = a_person[3][0].upper()

    if person_postal_code_first_letter == 'V' or person_fsa_first_letter == 'V':
        for clinic in list_of_clinics:
            if clinic[3][0].upper() or clinic[4][0].upper == 'V' or 'T' or 'Y':
                print(clinic[0] + 'this is close enough to evaluate')
            else:
                pass
    else:
        pass





#use the haversine (installed above to get rough distances from patient to clinic
def haversine_rough_distance(person, clinic):
    person_coordinates = person[6]
    clinic_coordinates = clinic[7]
    distance = haversine(person_coordinates, clinic_coordinates)
    return distance

#get a list of the distances to the clinics as well as the clinic name for a given person
def get_distances(a_person):
    list_of_distances = []
    for clinic in list_of_clinics:
        try:
            approx_distance = haversine_rough_distance(a_person, clinic)
            clinic_name_and_distance = (clinic[1], approx_distance)
            list_of_distances.append(clinic_name_and_distance)
        except TypeError:
            return 'this did not work'
            continue
        finally:
            pass
            continue
    return list_of_distances

#take the list from the closest options function and return a list of viable candidate hospitals.
#here, the value in the second for loop is set to 70 in order to get all of the hospitals within 70km
#of the closest one by haversine distance.

def get_candidates_list(a_list_of_distances):
    distances = []
    candidates_list = []
    for value in a_list_of_distances:
        dist_value = value[1]
        distances.append(dist_value)
    closest_haversine = min(distances)


    for value in a_list_of_distances:
        if value[1] < (closest_haversine + 70):
            candidates_list.append(value)
    return candidates_list


# def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
#     loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
#     url = "http://10.22.168.65:9080/route/v1/driving/"
#     r = requests.get(url + loc)
#     if r.status_code != 200:
#         return {}
#
#     res = r.json()
#     routes = polyline.decode(res['routes'][0]['geometry'])
#     start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
#     end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
#     distance = res['routes'][0]['distance']
#
#     out = {'route': routes,
#            'start_point': start_point,
#            'end_point': end_point,
#            'distance': distance
#            }
#
#     return out
#
# pickup_lon, pickup_lat, dropoff_lon, dropoff_lat = -117.851364,33.698206,-117.838925,33.672260
# test_route = get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
# test_route


geolocation = ox.geocoder.geocode('722 85 ST SW , CALGARY, Canada')
print(geolocation)

#add_geolocation_clinics(list_of_clinics)
#add_geolocation_patients(list_of_patients)

test_person = list_of_patients[1]
test_clinic= list_of_clinics[2]