import urllib
from urllib import request
from brute_force import geocoord_clinic_dict, geocoord_patient_dict

my_bing_key ='Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep'

test_person = geocoord_patient_dict[0]

#http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1={wayPoint1}&viaWaypoint.2={viaWaypoint2}&waypoint.3={waypoint3}&wayPoint.n={waypointN}&heading={heading}&optimize={optimize}&avoid={avoid}&distanceBeforeFirstTurn={distanceBeforeFirstTurn}&routeAttributes={routeAttributes}&timeType={timeType}&dateTime={dateTime}&maxSolutions={maxSolutions}&tolerances={tolerances}&distanceUnit={distanceUnit}&key={BingMapsKey}
#http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=london&wp.1=leeds&avoid=minimizeTolls&key=my_bing_key

# sample_coordinates1 = (51.0665226, -114.2094385)
# sample_coordinates2 = (39.16301429732479, -75.52250481727634)
#
# test_patient = ['1', '', '722 85 ST SW', 'T3H 1S6', 'T3H', 'CALGARY', 'AB', (51.0665226, -114.2094385)]
#
# patients_test = [['1', '', '722 85 ST SW', 'T3H 1S6', 'T3H', 'CALGARY', 'AB', (51.0665226, -114.2094385)],
#                         ['2', '', '1640 BLOOR ST W', 'M6P 1A7', 'M6P', 'TORONTO', 'ON', (43.6556336, -79.4564275)],
#                         ['3', '', '284 HELMCKEN RD', 'V9B 1T2', 'V9B', 'VICTORIA', 'BC', (48.4558124, -123.4411194)],
#                         ['4', '', '85 NORFOLK ST', 'N1H 4J4', 'N1H', 'GUELPH', 'ON', (-36.8553059, 174.7399914)],
#                         ['5', '', '462 BIRCHMOUNT RD', 'M1K 1N8', 'M1K', 'SCARBOROUGH', 'ON', (43.7076736, -79.2688982)]]
#
# candidate_clinic_test = [['1', 'Clinic 1', '8308 114 ST NW', 'T6G 2V2', 'T6G', 'Edmonton', 'AB', (53.5140941, -113.5259244)],
#                          ['2', 'Clinic 2', '3480 LAWRENCE AVE E', 'M1H 1A9', 'M1H', 'Scarborough', 'ON', (43.75979288235294, -79.22662067058823)],
#                          ['3', 'Clinic 3', '4715 8 Ave Se', 'T2A 3N4', 'T2A', 'Calgary', 'AB', (51.044899900000004, -113.9672190999108)],
#                          ['4', 'Clinic 4', '234 Dovedale Drive', 'L4P 0H3', 'L4P', 'Keswick', 'ON', (44.2171594, -79.4635385)],
#                          ['5', 'Clinic 5', '3968 RUE NOTRE-DAME O', 'H4C 1R1', 'H4C', 'Montreal', 'QC', (48.5159346, -2.7688328)]]

def make_url_ready_coords(some_coordinates):
    cleaned_up_coords = str(some_coordinates[0]) + ',' + str(some_coordinates[1])
    return cleaned_up_coords

# start_location = make_url_ready_coords(sample_coordinates1)
# end_location = make_url_ready_coords(sample_coordinates2)

# a working link:
#http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=london&wp.1=leeds&avoid=minimizeTolls&key=Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep

#a test
#http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=51.0665226,-114.2094385&wp.1=39.16301429732479,-75.52250481727634&avoid=minimizeTolls&key=Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep




#url_string = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0={start_location}&wp.1={end_location}&avoid=minimizeTolls&key=Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep"
#test = request.urlopen(url_string)

def get_data_from_bing(starting_point, ending_point):
    start_location =  make_url_ready_coords(starting_point)
    end_location = make_url_ready_coords(ending_point)
    url_string = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0={start_location}&wp.1={end_location}&avoid=minimizeTolls&key={my_bing_key}"
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


# def get_candidate_time_and_dist(a_patient, a_candidate_list):
#     for candidate in a_candidate_list:
#         try:
#             candidate_dict = get_data_from_bing(a_patient[7], candidate[7])
#             candidate.append(candidate_dict)
#         except Exception:
#             candidate.append('there was a problem')

# def get_candidate_time_and_dist(a_patient):
#     for candidate in a_patient:
#         try:
#             clinic_numbers = candidate[8].keys()
#             for clinic_number in clinic_numbers:
#                 index_num = geocoord_clinic_list.index(clinic_number)
#                 coordinates =
#             candidate_dict = get_data_from_bing(a_patient[7], candidate[7])
#             candidate.append(candidate_dict)
#         except Exception:
#             candidate.append('there was a problem')

def get_candidate_time_and_dist(a_patient):

    for candidate in a_patient['candidates']:
        try:

            candidate_dict = get_data_from_bing(a_patient['geo_code'], candidate['geo_code'])
            candidate['bing_results'] = candidate_dict
        except Exception:
            candidate.append('there was a problem')




resultant_list = [['1', 'Clinic 1', '8308 114 ST NW', 'T6G 2V2', 'T6G', 'Edmonton', 'AB', (53.5140941, -113.5259244), {'travel_distance': 314.295, 'travel_time': 10999}],
                  ['2', 'Clinic 2', '3480 LAWRENCE AVE E', 'M1H 1A9', 'M1H', 'Scarborough', 'ON', (43.75979288235294, -79.22662067058823), {'travel_distance': 3773.881, 'travel_time': 121021}],
                  ['3', 'Clinic 3', '4715 8 Ave Se', 'T2A 3N4', 'T2A', 'Calgary', 'AB', (51.044899900000004, -113.9672190999108), {'travel_distance': 20.623, 'travel_time': 1808}],
                  ['4', 'Clinic 4', '234 Dovedale Drive', 'L4P 0H3', 'L4P', 'Keswick', 'ON', (44.2171594, -79.4635385), {'travel_distance': 3405.878, 'travel_time': 124388}],
                  ['5', 'Clinic 5', '3968 RUE NOTRE-DAME O', 'H4C 1R1', 'H4C', 'Montreal', 'QC', (48.5159346, -2.7688328), 'there was a problem']]

# def pick_closest(a_candidate_list):
#     times = []
#     for candidate in a_candidate_list:
#         try:
#             travel_time = candidate[8]['travel_time']
#             times.append(travel_time)
#         except Exception:
#             pass
#     closest = min(times)
#     return closest

def pick_closest(a_candidate_list):
    times = []
    final_answer = ''
    for candidate in a_candidate_list:
        try:
            travel_time = candidate['bing_results']['travel_time']
            times.append(travel_time)
        except Exception:
            pass
    closest = min(times)

    for selection in a_candidate_list:
        if selection ['bing_results']['travel_time'] == closest:
            final_answer = selection
    return final_answer

def give_everyone_an_answer(a_list_of_people):
    for person in a_list_of_people:
        get_candidate_time_and_dist(person)
        pick_closest(person['candidates'])




