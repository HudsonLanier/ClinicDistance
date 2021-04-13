from urllib import request
from winnower import geocoord_patient_dict
from getcoords import BingMapsAPIKey
import time

test_person = geocoord_patient_dict[0]

def make_url_ready_coords(some_coordinates):
    cleaned_up_coords = str(some_coordinates[0]) + ',' + str(some_coordinates[1])
    return cleaned_up_coords


def get_data_from_bing(starting_point, ending_point):
    start_location =  make_url_ready_coords(starting_point)
    end_location = make_url_ready_coords(ending_point)
    url_string = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0={start_location}&wp.1=" \
                 f"{end_location}&avoid=minimizeTolls&key={BingMapsAPIKey}"
    bing_info = request.urlopen(url_string)
    data = bing_info.read()
    xml = data.decode("UTF-8")
    start_travel_dist_index = xml.index('<TravelDistance>') + 16
    end_travel_dist_index = xml.index('</TravelDistance>')
    travel_distance = xml[start_travel_dist_index:end_travel_dist_index]
    travel_distance_int = float(travel_distance)
    start_travel_time_index = xml.index('<TravelDuration') +16
    end_travel_time_index = xml.index('</TravelDuration>')
    travel_time= xml[start_travel_time_index: end_travel_time_index]
    travel_time_int = float(travel_time)
    patient_hospital_dict = {'travel_distance': travel_distance_int,
                             'travel_time': travel_time_int}
    return patient_hospital_dict


def get_candidate_time_and_dist(a_patient, retries=3):
    if retries < 0:
        return
    for candidate in a_patient['candidates']:
        try:
            candidate_dict = get_data_from_bing(a_patient['geo_code'], candidate['geo_code'])
            candidate['bing_results'] = candidate_dict
        except Exception:
            candidate['bing_results'] = 'there was a problem'
            time.sleep(.1)
            return get_candidate_time_and_dist(a_patient, retries -1)


get_candidate_time_and_dist(geocoord_patient_dict[1])

def pick_closest(a_person):
    distances = []
    for candidate in a_person['candidates']:
        try:
            travel_distance = candidate['bing_results']['travel_distance']
            distances.append(travel_distance)
        except Exception:
            pass


    if len(distances) > 0:
        closest = min(*distances)
        for selection in a_person['candidates']:
            try:
                if selection['bing_results']['travel_distance'] == closest:
                    selection['closest'] = True
                else:
                    selection['closest'] = False
            except Exception:
                selection['closest'] = False

    else:
        distances = []
        for candidate in a_person['candidates']:
            distance = candidate['distance']
            distances.append(distance)


        closest = min(*distances)
        for selection in a_person['candidates']:
            try:
                if selection['distance'] == closest:
                    selection['closest'] = True
                else:
                    selection['closest'] = False
            except Exception:
                selection['closest'] = False


def give_everyone_an_answer(a_list_of_people):
    for person in a_list_of_people:
        get_candidate_time_and_dist(person)
        pick_closest(person)

give_everyone_an_answer(geocoord_patient_dict)




