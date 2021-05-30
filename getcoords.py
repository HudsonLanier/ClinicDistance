import csv
import osmnx as ox
import geocoder
import time

#PROGRAM USER: PUT YOUR BING API KEY HERE
BingMapsAPIKey = ''
#PROGRAM USER: PUT YOUR PATIENT CSV FILE PATH HERE
patient_file_path = ''
#PROGRAM USER: PUT YOUR CLINIC FILE PATH HERE
clinic_file_path = ''

list_of_patients = []
list_of_clinics = []

#open the patient csv and store each patient as a list within the list_of_patients
with open(patient_file_path) as patient_data:
    for line in csv.reader(patient_data):
        list_of_patients.append(line)

#open the clinic csv and store each clinic as a list within the list_of_clinics
with open(clinic_file_path) as clinic_data:
    for line in csv.reader(clinic_data):
        list_of_clinics.append(line)

#this line deletes the first line, which has the names of the fields, and not actual data about patients
del list_of_patients[0]
del list_of_clinics[0]

#the clinics file has 2 columns before the address starts, whereas the patients has only 1
# this function adds a a column to patients, so that the data will line up for both sets
def match_formatting(the_list_of_patients):
    for patient in the_list_of_patients:
        patient.insert(1, '')

match_formatting(list_of_patients)

#puts the values into a dictionary for each clinic or patient

def make_dictionaries(a_list):
    new_list = []
    i = 0
    while i < len(a_list):
        dict_name = 'patient{}'.format(i)
        dict_name = {}
        dict_name['id'] = a_list[i][0]
        dict_name['geo_cols'] = str(a_list[i][2] + ' ' + a_list[i][5] + ' ' + 'Canada' )
        dict_name['geo_code'] = ''
        dict_name['address'] = a_list[i][2]
        dict_name['postal_code'] = a_list[i][3]
        dict_name['fsa'] = a_list[i][4]
        dict_name['nearest_clinic_id'] = ''
        dict_name['distance'] = ''
        dict_name['city'] = a_list[i][5]
        dict_name['provence'] = a_list[i][6]
        new_list.append(dict_name)
        i +=1
    return  new_list

patient_dictionary = make_dictionaries(list_of_patients)
clinic_dictionary = make_dictionaries(list_of_clinics)

def add_clinic_value(dictionary_of_clinics):
    for item in dictionary_of_clinics:
        item['is_clinic'] = True
        item['is_patient'] = False

def add_patient_value(dictionary_of_patients):
    for item in dictionary_of_patients:
        item['is_patient'] = True
        item['is_clinic'] = False

add_clinic_value(clinic_dictionary)
add_patient_value(patient_dictionary)


def add_geolocation(a_list_of_lists):
    for entity in a_list_of_lists:
        address_string = entity['geo_cols']
        try:
            geolocation = ox.geocoder.geocode(address_string)
            entity['geo_code'] = geolocation
        except Exception:
            entity['geo_code'] = 'failed to get coordinates'


# make a function that gets rid of unit, apartment, suite numbers, and other types of data that are confusing the
# geocoder. If you find more words and phrases that cause a failure, simply add them to the problem_words list

def clean_up_addresses(a_list_of_lists):
    problem_words = ['UNIT', 'SUITE', 'ROOM', 'FLOOR', 'APT', 'APARTMENT', 'BUREAU', 'ETAGE']
    for entity in a_list_of_lists:
        address_string = entity['address'].upper()
        if any(x in address_string for x in problem_words):
            #break the string into a list, remove from the problem word to the end, return the corrected address
            address_list = address_string.split()
            for problem_word in problem_words:
                if problem_word in address_list:
                    problem_word_index = address_list.index(problem_word)
                    new_address_list = address_list[:problem_word_index]
                    new_address_string = ' '.join(new_address_list)
                    entity['cleaned_up_address'] = new_address_string
                    entity['geo_cols'] = str(entity['cleaned_up_address']+ ' ' + entity['city'] + ' ' + 'Canada')

        else:
            pass

    return a_list_of_lists


#run the geocoder again with the cleaned up address line
def try_geolocation_again(a_list_of_lists):
    for entity in a_list_of_lists:
        if entity['geo_code'] == 'failed to get coordinates':
            try:
                address_string = entity['geo_cols']
                geolocation = ox.geocoder.geocode(address_string)
                entity['geo_code'] = geolocation

            except Exception:
                pass
        else:
            pass

#this will retry 3 times in the event that the API call is unsuccessful for any reason
def bing_coords_first_attempt(a_list, retries=2):
    if retries <0:
        return
    try:
        for item in a_list:
            if item['geo_code'] == 'failed to get coordinates':
                location = str( item['address'] + item['city'] + item[
                    'postal_code'])
                item['geo_cols'] = location
                geocode = geocoder.bing( location , key =BingMapsAPIKey)
                latitude = geocode.geojson['features'][0]['properties']['lat']
                longitude = geocode.geojson['features'][0]['properties']['lng']
                item['geo_code'] = (latitude, longitude)

            else:
                pass

    except Exception:
        time.sleep(.1)
        return bing_coords_first_attempt(a_list, retries - 1)


def bing_coords_second_attempt(a_list):
    try:
        for item in a_list:
            if item['geo_code'] == 'failed to get coordinates':
                location = str(item['city'] + item['postal_code'])
                item['geo_cols'] = location
                geocode = geocoder.bing( location , key =BingMapsAPIKey)
                latitude = geocode.geojson['features'][0]['properties']['lat']
                longitude = geocode.geojson['features'][0]['properties']['lng']
                item['geo_code'] = (latitude, longitude)

            else:
                pass
    except Exception:
        pass


def bing_coords_third_attempt(a_list):
    try:
        for item in a_list:
            if item['geo_code'] == 'failed to get coordinates':
                location = str(item['fsa'] + item['city'] + item['province'])
                item['geo_cols'] = location
                geocode = geocoder.bing(location, key=BingMapsAPIKey)
                latitude = geocode.geojson['features'][0]['properties']['lat']
                longitude = geocode.geojson['features'][0]['properties']['lng']
                item['geo_code'] = (latitude, longitude)

            else:
                pass
    except Exception:
        pass


def bing_coords_fourth_attempt(a_list):
    try:
        for item in a_list:
            if item['geo_code'] == 'failed to get coordinates':
                location = str(item['city'] + item['province'])
                item['geo_cols'] = location
                geocode = geocoder.bing(location, key=BingMapsAPIKey)
                latitude = geocode.geojson['features'][0]['properties']['lat']
                longitude = geocode.geojson['features'][0]['properties']['lng']
                item['geo_code'] = (latitude, longitude)

            else:
                pass
    except Exception:
        pass


def bing_get_coords(a_list):
    bing_coords_first_attempt(a_list)
    bing_coords_second_attempt(a_list)
    bing_coords_third_attempt(a_list)
    bing_coords_fourth_attempt(a_list)

# #if there was no way to get an address, assign one.
# #I picked one in Toronto for patients, because that is Canada's most populous city
#this keeps the program running in the event that there was an entry with no usable information in it.
#for clinics with no usable information, I used a location in the middle of the ocean so as
#not to direct patients there

def guess_location(a_list_of_lists):
    for entity in a_list_of_lists:
        if entity['geo_code'] == 'failed to get coordinates' and entity['is_patient'] == True:
            entity['geo_code'] = (43.65365176827117, -79.3942239178996)
            entity['warning'] = 'did not find the geocode'

        elif entity['geo_code'] == 'failed to get coordinates' and entity['clinic'] == True:
            entity['geo_code'] = (18.521837397421635, 169.1714771092401)
            entity['warning'] = 'did not find the geocode'
        else:
            pass

#
# #take the list of patients and the list of clinics and return a cleaned up data set
# #with coordinates for every location

def get_clean_addresses(a_list):
    add_geolocation(a_list)
    clean_up_addresses(a_list)
    try_geolocation_again(a_list)
    bing_get_coords(a_list)
    guess_location(a_list)
    return a_list

geocoord_patient_dict = get_clean_addresses(patient_dictionary)
geocoord_clinic_dict = get_clean_addresses(clinic_dictionary)


