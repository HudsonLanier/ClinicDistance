import csv

import osmnx as ox



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


#the clinics file has 2 columns before the address starts, whereas the patients has only 1
# this function adds a a column to patients, so that the data will line up for both sets
def match_formatting(the_list_of_patients):
    for patient in the_list_of_patients:
        patient.insert(1, '')

match_formatting(list_of_patients)



#this function will not work for both patients and clinics, because both are formatted differently. CLEAN THIS UP
#SO THAT IT WILL RUN AS ONE FUNCTION
# def add_geolocation_patients(a_list_of_lists):
#     for entity in a_list_of_lists:
#         address_string = str(entity[1] + ', ' + entity[4] + ', ' + 'Canada')
#         try:
#             geolocation = ox.geocoder.geocode(address_string)
#             entity.append(geolocation)
#         except Exception:
#             entity.append('no coordinates yet')

def add_geolocation(a_list_of_lists):
    for entity in a_list_of_lists:
        address_string = str(entity[2] + ', ' + entity[5] + ', ' + 'Canada')
        try:
            geolocation = ox.geocoder.geocode(address_string)
            entity.append(geolocation)
        except Exception:
            entity.append('failed to get coordinates')


#function turns a list into a string. This is needed in the clean_up_addresses function



#make a function that gets rid of unit, apartment, suite numbers, and other types of data that are confusing the
#geocoder. If you find more words and phrases that cause a failure, simply add them to the problem_words list
def clean_up_addresses(a_list_of_lists):
    problem_words = ['UNIT', 'SUITE', 'ROOM', 'FLOOR', 'APT', 'APARTMENT', 'BUREAU', 'ETAGE']
    for entity in a_list_of_lists:
        address_string = entity[2].upper()
        if any(x in address_string for x in problem_words):
            #break the string into a list, remove from the problem word to the end, return the corrected address
            address_list = address_string.split()
            for problem_word in problem_words:
                if problem_word in address_list:
                    problem_word_index = address_list.index(problem_word)
                    new_address_list = address_list[:problem_word_index]
                    new_address_string = ' '.join(new_address_list)
                    entity[2] = new_address_string

        else:
            pass

    return a_list_of_lists

def try_geolocation_again(a_list_of_lists):
    for entity in a_list_of_lists:
        if entity[7] == 'failed to get coordinates':
            try:
                address_string = entity[2]
                geolocation = ox.geocoder.geocode(address_string)
                entity[7] = geolocation
            except Exception:
                pass
        else:
            pass

#if there was no way to get an address, assign one.
#I picked one in Toronto, because that is Canada's most populous city
#this function is only to be used for testing or in the event  that everything else fails
def guess_location(a_list_of_lists):
    for entity in a_list_of_lists:
        if entity[7] == 'failed to get coordinates':
            entity[2] = '393 Dundas St'
            entity[3] = 'M5T 1G6'
            entity[4] = 'M5T'
            entity[5] = 'Toronto'
            entity[6] = 'ON'
            entity[7] = (43.65365176827117, -79.3942239178996)
        else:
            pass


#take the list of patients and the list of clinics and return a cleaned up data set
#with coordinates for every location

#note clinic 6 is showing up in the dominican republic
def get_clean_addresses(a_list):
    add_geolocation(a_list)
    clean_up_addresses(a_list)
    try_geolocation_again(a_list)
    guess_location(a_list)
    return a_list

geocoord_patient_list = get_clean_addresses(list_of_patients)
geocoord_clinic_list = get_clean_addresses(list_of_clinics)


