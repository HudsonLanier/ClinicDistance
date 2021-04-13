import csv
from bing import geocoord_patient_dict

def get_travel_distance(a_candidate):
    travel_distance = a_candidate['bing_results']['travel_distance']
    return travel_distance

def get_closest_info(a_patient):
    try:
        for candidate in a_patient['candidates']:
                if candidate['closest'] == True:
                    return candidate
    except Exception:
        test_list = sorted(a_patient['candidates'], key=get_travel_distance())
        return test_list[0]


#make a final formatted list of the relevant data. Format specified by client is listed here:
# ['patient_id', 'pat_geo_cols', 'pat_geocode', 'pat_address', 'pat_postal_code',\
#  'pat_fsa', 'nearest_clinic_id', 'clinic_geo_cols', 'clinic_geocode', 'clinic_address',\
#  'clinic_postal_code' 'clinic_fsa', 'clinic_distance']
def format_data(list_of_patients):
    final_list = []
    for patient in list_of_patients:
        formatted_data_list = []
        formatted_data_list.append(patient['id'])
        formatted_data_list.append(patient['geo_cols'])
        formatted_data_list.append(patient['geo_code'])
        formatted_data_list.append(patient['address'])
        formatted_data_list.append(patient['postal_code'])
        formatted_data_list.append(patient['fsa'])

        closest_clinic = get_closest_info(patient)

        formatted_data_list.append(closest_clinic['id'])
        formatted_data_list.append(closest_clinic['geo_cols'])
        formatted_data_list.append(closest_clinic['geo_code'])
        formatted_data_list.append(closest_clinic['address'])
        formatted_data_list.append(closest_clinic['postal_code'])
        formatted_data_list.append(closest_clinic['fsa'])
        try:
            formatted_data_list.append(closest_clinic['bing_results']['travel_distance'])
        except Exception:
            formatted_data_list.append(closest_clinic['distance'])
        final_list.append(formatted_data_list)

    return final_list

final_list = format_data(geocoord_patient_dict)

#export a csv file with all of the information for every patient
with open('final_patients_list_with_clinics.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(final_list)